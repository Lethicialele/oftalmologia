from datetime import date, datetime, timedelta
from django.utils import timezone
from locale import setlocale, LC_TIME, LC_ALL
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from medicos.models import Medicos
from medicos.views import mostrarMedicos
from .forms import AtualizarCadastroAgendamentos, CadastrarAgendamentos, AtualizarAgendamentos
from django.contrib import messages
from .models import Agendamentos
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models.functions import Now
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas


def cadastrarAgendamentos(request):
    if request.method == "POST":
        print(request.POST['numero_de_olhos'])
        form = CadastrarAgendamentos(request.POST)
        if form.is_valid():
            # Salvando os dados mesmo que alguns campos estejam vazios
            agendamento = form.save(commit=False)
            agendamento.nome_mae = form.cleaned_data['nome_mae']
            agendamento.enfermaria = form.cleaned_data['enfermaria']
            agendamento.clinica = form.cleaned_data['clinica']
            agendamento.leito = form.cleaned_data['leito']
            data_atual = timezone.localtime(
                timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
            historico_entry = f"Cadastro ( em {data_atual} por {request.user}): {agendamento.nome_mae} - Clínica: {agendamento.clinica} - Enfermaria: {agendamento.enfermaria} - Leito: {agendamento.leito} - Email: {agendamento.email} - Telefone: {agendamento.telefone} - Número de Olhos: {agendamento.numero_de_olhos} - Olho agendado: {agendamento.olho_agendado} - Diagnóstico: {agendamento.diagnostico} - Nível de Prioridade: {agendamento.nivel_prioridade}\n"
            agendamento.historico += historico_entry
            agendamento.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            _, error = next(iter(form.errors.items()))
            messages.error(request, error)
    else:
        form = CadastrarAgendamentos()

    return render(request, 'cadastrarAgendamentos.html', {'usuario': request.user, 'form': form})


def confirmarAgendamentos(request, data_agendada=None):
    setlocale(LC_ALL, 'pt_BR.utf-8')

    if data_agendada is None or data_agendada == "":
        if request.method == "POST":
            print("post")
            post_data = request.POST.copy()
            total_items = len(post_data.getlist('id_agendamento'))
            data = request.POST.get('data_selecionada')
            data_parseada = datetime.strptime(data, '%d de %B de %Y')
            data_selecionada = datetime.strftime(data_parseada, '%Y-%m-%d')
            print(data_selecionada)
            for contador in range(0, total_items):
                agendamento_id = post_data.getlist('id_agendamento')[contador]
                status = post_data.getlist('status')[contador]
                observacao = post_data.getlist('observacao')[contador]
                try:
                    agendamento = Agendamentos.objects.get(id=agendamento_id)
                    form = AtualizarAgendamentos(
                        {'id': agendamento_id, 'status': status, 'observacao': observacao}, instance=agendamento)
                    if form.is_valid():
                        agendamento.status = status
                        agendamento.observacao = observacao
                        data_atual = timezone.localtime(
                            timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
                        historico_entry = f"Confirmação de Agendamento (em {data_atual} por {request.user}): Data Agendada: {agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
                        agendamento.historico += historico_entry
                        agendamento.numero_atualizacoes += 1
                        form.save()
                        agendamento.save()
                    else:
                        messages.error(request, '')
                except Agendamentos.DoesNotExist:
                    # Lidar com o caso em que o agendamento correspondente não existe
                    pass
            messages.success(request, 'Agendamentos atualizados com sucesso!')

        elif request.method == "GET":
            # Para o filtrar por data e acesso pelo navbar
            data_selecionada = request.GET.get('data_selecionada')
            print(data_selecionada)
            print("elif get")
            if data_selecionada is None:
                print("if prox dia")
                proximo_dia_com_agendamentos = Agendamentos.objects.filter(data_agendada__gte=(
                    date.today())).order_by('data_agendada').values('data_agendada').first()
                if proximo_dia_com_agendamentos:
                    data_selecionada = proximo_dia_com_agendamentos['data_agendada']
                else:
                    # Se não houver agendamentos futuros, defina a data como hoje
                    data_selecionada = date.today()
    else:
        # Quando é chamada por gerarAgenda
        data_selecionada = data_agendada

    # Aplique a condição do status ao filtro
    agendamentos = Agendamentos.objects.filter(
        data_agendada=data_selecionada, status__in=['não confirmado', 'cancelado'])
    print(data_agendada)
    print(data_selecionada)

    try:
        # Para o filtrar por data
        data_parseada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        print(data_parseada)
        print("entrou try")
    except:
        data_parseada = data_selecionada
        print(data_parseada)
        print("entrou except")

    return render(request, 'confirmarAgendamentos.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data_selecionada': data_parseada})


def confirmarAtendimentos(request):
    setlocale(LC_ALL, 'pt_BR.utf-8')

    agendamentos = None  # Declare a variável aqui para garantir visibilidade

    if request.method == "POST":
        data = request.POST.get('data_selecionada')
        data_parseada = datetime.strptime(data, '%d de %B de %Y')
        data_selecionada = datetime.strftime(data_parseada, '%Y-%m-%d')
        post_data = request.POST.copy()
        data_atual = timezone.localtime(
            timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
        atendidos_ids = post_data.get('agendamento_ids').split(',')
        if atendidos_ids[0] != '':
            agendamentos = Agendamentos.objects.filter(id__in=atendidos_ids)

            for contador, agendamento in enumerate(agendamentos):
                if agendamento.ultima_atualizacao == data_selecionada:
                    break
                agendamento.numero_atualizacoes += 1
                agendamento.atendido += 1
                agendamento.aplicacao_atual += 1
                historico_entry = f"Atendido! (em {data_atual} por {request.user}): Data Agendada: {agendamento.data_agendada} - Status: {agendamento.status} - Aplicação: {agendamento.aplicacao_atual}/{agendamento.quantidade_aplicacoes_necessarias}\n"
                agendamento.historico += historico_entry
                agendamento.ultimo_atendimento = data_selecionada
                agendamento.ultima_atualizacao = data_selecionada
                agendamento.status = 'não confirmado'
                agendamento.data_agendada = None
                if agendamento.quantidade_aplicacoes_necessarias - agendamento.atendido == 1:
                    agendamento.oct = True
                    agendamento.observacao = ''
                elif agendamento.quantidade_aplicacoes_necessarias - agendamento.atendido == 0:
                    agendamento.status = 'concluido'
                else:
                    agendamento.status = 'não confirmado'
                    agendamento.observacao = ''
                agendamento.save()
        else:
            atendidos_ids = []
        agendamentos = Agendamentos.objects.filter(
            data_agendada=data_selecionada).exclude(id__in=atendidos_ids)

        for contador, agendamento in enumerate(agendamentos):
            if agendamento.ultima_atualizacao == data_selecionada:
                break
            historico_entry = f"FALTOU no atendimento (em {data_atual} por {request.user}): Data Agendada: {agendamento.data_agendada} - Status: {agendamento.status} - Aplicação: {agendamento.aplicacao_atual}/{agendamento.quantidade_aplicacoes_necessarias}\n"
            agendamento.historico += historico_entry
            agendamento.status = 'não confirmado'
            agendamento.ultima_atualizacao = data_selecionada
            agendamento.observacao = ''
            agendamento.data_agendada = None
            agendamento.faltas += 1
            agendamento.save()

        agendamentos = Agendamentos.objects.filter(
            data_agendada=data_selecionada)
        agendamentos = agendamentos.order_by(
            '-nivel_prioridade', 'data_cadastro', '-aplicacao_atual', '-numero_de_olhos')
        messages.success(request, ('Atendimentos confirmados com sucesso!'))
        return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data})

    return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data_selecionada})


def consultarAgendaDia(request, filtro_agenda=None):
    if request.method == "POST":
        filtro_data = request.POST.get('filtro_data')
        if filtro_data:
            data = datetime.strptime(filtro_data, '%Y-%m-%d').date()
        elif filtro_agenda:
            data = filtro_agenda
        else:
            proximo_dia_com_agendamentos = Agendamentos.objects.filter(data_agendada__gte=(
                date.today())).order_by('data_agendada').values('data_agendada').first()
            if proximo_dia_com_agendamentos:
                data = proximo_dia_com_agendamentos['data_agendada']
            else:
                # Se não houver agendamentos futuros, defina a data como hoje
                data = date.today()
    else:
        if filtro_agenda:
            data = datetime.strptime(filtro_agenda, '%Y-%m-%d').date()
        else:
            proximo_dia_com_agendamentos = Agendamentos.objects.filter(data_agendada__gte=(
                date.today())).order_by('data_agendada').values('data_agendada').first()
            if proximo_dia_com_agendamentos:
                data = proximo_dia_com_agendamentos['data_agendada']
            else:
                # Se não houver agendamentos futuros, defina a data como hoje
                data = date.today()
    agendamentos = Agendamentos.objects.filter(data_agendada=data, status__in=[
                                               'não confirmado', 'confirmado'])
    agendamentos = agendamentos.order_by(
        '-nivel_prioridade', 'data_cadastro', '-numero_de_olhos')

    return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data})


def gerarAgenda(request):
    pacientes = consultarFilaEsperaPacientes(request, 'gerar_agenda')

    if request.method == 'POST':
        data_agendada = request.POST.get('data_agendada')
        quantidade_olhos = int(request.POST.get('quantidade_olhos', 0))
        max_faltas = int(request.POST.get('max_faltas'))

        if not data_agendada or quantidade_olhos <= 0:
            return HttpResponse('Dados inválidos para geração de agenda', status=400)

        # Consulta para buscar os agendamentos que atendem aos critérios
        agendamentos = Agendamentos.objects.raw('''
            SELECT * FROM agendamentos_agendamentos
            WHERE status NOT IN ('concluido', 'cancelado', 'desinteressado')
            AND data_agendada IS NULL AND faltas <= %s
            ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        ''', [max_faltas])

        numero_de_olhos_agendados = 0
        agendamentos_selecionados = []

        for agendamento in agendamentos:
            # Verifica se ainda há espaço para mais olhos
            if numero_de_olhos_agendados >= quantidade_olhos:
                break

            # Verifica se o número de olhos do agendamento atual cabe no restante das vagas
            if numero_de_olhos_agendados + agendamento.numero_de_olhos <= quantidade_olhos:
                # Se couber, adiciona o agendamento à lista de agendamentos selecionados
                agendamentos_selecionados.append(agendamento)
                numero_de_olhos_agendados += agendamento.numero_de_olhos

        # Atualiza os agendamentos selecionados
        for agendamento in agendamentos_selecionados:
            agendamento.data_agendada = data_agendada
            agendamento.status = 'não confirmado'
            data_atual = timezone.localtime(
                timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
            historico_entry = f"Agendamento Padrão (em {data_atual} por {request.user}): {agendamento.data_agendada}\n"
            agendamento.historico += historico_entry
            agendamento.save()

        # Retorna a página de confirmação de agendamentos
        data_agendada = datetime.strptime(data_agendada, '%Y-%m-%d').date()
        return confirmarAgendamentos(request, data_agendada)

    # Renderize a página de geração de agenda (substitua com o caminho real do seu template)
    return render(request, 'gerarAgenda.html', {'usuario': request.user, 'pacientes': pacientes})


def gerarRelatorio(request):
    agendamentos = None  # Inicialize com None para o caso de não haver agendamentos
    medico = request.user
    medico = Medicos.objects.filter(usuario=medico).first()

    if request.method == 'POST':
        print(request.POST)
        documentos = (request.POST.get("documentos")) == 'on'
        receitas = (request.POST.get("receitas")) == 'on'
        relatorios = (request.POST.get("relatorios")) == 'on'

        # Obtenha a lista de IDs dos agendamentos selecionados
        agendamento_ids = request.POST.get(
            'agendamento_documentos_ids', '').split(',')

        # Obtenha os agendamentos correspondentes aos IDs selecionados
        agendamentos = Agendamentos.objects.filter(id__in=agendamento_ids)

    # Se houver agendamentos, redirecione para a página 'relatorio.html' com os dados dos agendamentos
    for agendamento in agendamentos:
        if agendamento.olho_agendado == 'esquerdo':
            agendamento.olho_agendado = 'OLHO ESQUERDO'
        elif agendamento.olho_agendado == 'direito':
            agendamento.olho_agendado = 'OLHO DIREITO'
        else:
            agendamento.olho_agendado = 'OLHO ESQUERDO E DIREITO'

    if agendamentos:
        return render(request, 'relatorio.html', {'usuario': request.user, 'agendamentos': agendamentos, 'medico': medico,
                                                  'documentos': documentos, 'receitas': receitas, 'relatorios': relatorios
                                                  })

    # Se não houver agendamentos, retorne apenas o render do template sem contexto
    return render(request, 'relatorio.html', {'usuario': request.user, 'medico': medico, 'selecionados_ids': agendamento_ids})


def imprimirAgenda(request, data_selecionada):
    if data_selecionada is None:
        # Se a data não foi fornecida, definir como o próximo dia útil
        data_selecionada = f'{(date.today() + timedelta(days=1))}'

    if request.method == 'POST':
        # Obtenha a lista de IDs dos agendamentos selecionados
        agendamento_ids = request.POST.get('agendamento_ids', '').split(',')

        # Obtenha os agendamentos correspondentes aos IDs selecionados
        agendamentos = Agendamentos.objects.filter(
            id__in=agendamento_ids, data_agendada=data_selecionada)

    # Crie o contexto com os dados a serem passados para o modelo
    data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
    context = {'agendamentos': agendamentos,
               'data_selecionada': data_selecionada}

    # Renderize o modelo
    template_path = 'imprimirAgenda.html'  # Atualize com o caminho correto
    template = get_template(template_path)
    html = template.render(context)

    # Crie um objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'

    # Converta o HTML para PDF
    pisa_status = pisa.CreatePDF(html, dest=response, orientation='Landscape')

    # Se a conversão falhar, retorne um erro
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response


def default_link_callback(uri, req):
    if uri.startswith('http://') or uri.startswith('https://'):
        return uri
    return os.path.join(settings.MEDIA_ROOT, uri)


def consultarFilaEsperaPacientes(request, chamada=None):
    if chamada == None:
        chamada = request.GET.get('chamada')
        if chamada == 'gerar_agenda':
            consulta_sql = '''
            SELECT *
            FROM agendamentos_agendamentos
            WHERE status NOT IN ('concluido', 'cancelado', 'desinteressado')
            AND data_agendada IS NULL
            AND DATEDIFF(CURRENT_DATE, ultimo_atendimento) > 30
            ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        '''
            agendamentos = Agendamentos.objects.raw(consulta_sql)
            return agendamentos

        elif chamada == 'fila_espera':
            consulta_sql = '''
            SELECT *
            FROM agendamentos_agendamentos
            WHERE status NOT IN ('concluido', 'cancelado', 'desinteressado') and data_agendada IS NULL
            ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        '''
            agendamentos = Agendamentos.objects.raw(consulta_sql)
            return render(request, 'pacientesFilaEspera.html', {'usuario': request.user, 'pacientes': agendamentos})
        else:
            consulta_sql = '''
            SELECT *
            FROM agendamentos_agendamentos
            WHERE status NOT IN ('concluido', 'cancelado', 'desinteressado') and data_agendada IS NULL
            AND DATEDIFF(CURRENT_DATE, ultimo_atendimento) > 30
            ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        '''
            agendamentos = Agendamentos.objects.raw(consulta_sql)
            return render(request, 'pacientesFilaEspera.html', {'usuario': request.user, 'pacientes': agendamentos})
    else:
        print(chamada)
        consulta_sql = '''
        SELECT *
        FROM agendamentos_agendamentos
        WHERE status NOT IN ('concluido', 'cancelado', 'desinteressado') and data_agendada IS NULL
        ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
    '''
        agendamentos = Agendamentos.objects.raw(consulta_sql)
    return agendamentos


def listarPacientesFinalizados(request):
    consulta_sql = '''
        SELECT *
        FROM agendamentos_agendamentos
        WHERE status IN ('concluido')
        ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        '''
    agendamentos = Agendamentos.objects.raw(consulta_sql)
    return render(request, 'pacientesFinalizados.html', {'usuario': request.user, 'pacientes': agendamentos})


def reiniciarPacienteFinalizado(request):
    paciente_id = request.POST.get('paciente_id')
    agendamento = Agendamentos.objects.filter(id=paciente_id).first()
    agendamento.status = 'não confirmado'
    agendamento.observacao = ''
    agendamento.quantidade_aplicacoes_necessarias += 3
    agendamento.save()

    messages.success(
        request, 'Paciente movido para lista de espera com sucesso!')

    return redirect('listarPacientesFinalizados')


def listarPacientesDesinteressados(request):
    consulta_sql = '''
        SELECT *
        FROM agendamentos_agendamentos
        WHERE status IN ('desinteressado')
        ORDER BY nivel_prioridade DESC, data_cadastro ASC, numero_de_olhos DESC
        '''
    agendamentos = Agendamentos.objects.raw(consulta_sql)
    return render(request, 'pacientesDesinteressados.html', {'usuario': request.user, 'pacientes': agendamentos})


def deletarPaciente(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        agendamento = get_object_or_404(Agendamentos, id=paciente_id)
        agendamento.delete()

        messages.success(request, 'Paciente deletado com sucesso!')

    return HttpResponse(status=204)


def moverParaDesinteressados(request):
    paciente_id = request.POST.get('paciente_id')
    motivo = request.POST.get('motivo')
    agendamento = Agendamentos.objects.filter(id=paciente_id).first()
    agendamento.status = 'desinteressado'

    # Adicionando o motivo ao registro de histórico
    data_atual = timezone.localtime(
        timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    historico_entry = f"Movido para inativos (em {data_atual} por {request.user}): Status: {agendamento.status} Motivo: {motivo} \n"
    agendamento.historico += historico_entry

    agendamento.save()

    messages.success(
        request, 'Paciente movido para lista de inativos com sucesso!')

    return redirect('listarPacientesDesinteressados')


def agendarPaciente(request):

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        data_agendada = request.POST.get("data_agendada")
        agendamento = Agendamentos.objects.filter(id=paciente_id).first()

        # Atualize o objeto agendamento com a nova data_agendada
        agendamento.data_agendada = data_agendada
        agendamento.status = 'não confirmado'
        if agendamento.quantidade_aplicacoes_necessarias == agendamento.aplicacao_atual:
            agendamento.quantidade_aplicacoes_necessarias += 3
        data_atual = timezone.localtime(
            timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        historico_entry = f"Agendamento Manual (em {data_atual} por {request.user}): Data agendada: {agendamento.data_agendada}\n"
        agendamento.historico += historico_entry
        agendamento.save()

        # Adicione mensagens de sucesso, se necessário
        messages.success(request, 'Paciente agendado com sucesso!')

        # Redirecionar para a página consultarAgendaDia com a data_agendada escolhida
        return redirect('consultarAgendaDiaFiltro', filtro_agenda=data_agendada)

    paciente_id = request.GET.get('paciente_id')

    agendamento = Agendamentos.objects.filter(id=paciente_id)

    return render(request, 'agendarPaciente.html', {'agendamento': agendamento.first(), 'usuario': request.user})


def atualizarCadastroAgendamento(request):
    agendamento_id = None
    if request.method == "POST":
        agendamento_id = request.POST.get('id')
        agendamento = Agendamentos.objects.filter(id=agendamento_id).first()
        form = AtualizarCadastroAgendamentos(
            request.POST, instance=agendamento)
        if form.is_valid():
            data_atual = timezone.localtime(
                timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
            historico_entry = f"Atualização Cadastral (em {data_atual} por {request.user}): Mãe: {agendamento.nome_mae} - Clínica: {agendamento.clinica} - Enfermaria: {agendamento.enfermaria} - Leito: {agendamento.leito} - Email: {agendamento.email} - Telefone: {agendamento.telefone} - Número de Olhos: {agendamento.numero_de_olhos} - Olho agendado: {agendamento.olho_agendado} - Diagnóstico: {agendamento.diagnostico} - Nível de Prioridade: {agendamento.nivel_prioridade}\n"
            agendamento.historico += historico_entry
            form.save()
            messages.success(
                request, 'Dados do paciente atualizados com sucesso!')
        else:
            _, error = next(iter(form.errors.items()))
            messages.error(request, error)
    else:
        agendamento_id = request.GET.get('agendamento_id')

    agendamento = Agendamentos.objects.filter(id=agendamento_id).first()

    return render(request, 'atualizarCadastroAgendamento.html', {'usuario': request.user, 'agendamento': agendamento})


def removerPacienteAgenda(request):
    data = None
    if request.method == "POST":
        agendamento_id = request.POST.get('agendamento_id')
        agendamento = Agendamentos.objects.filter(id=agendamento_id).first()
        data = agendamento.data_agendada
        agendamento.data_agendada = None
        agendamento.status = None
        agendamento.observacao = None
        data_atual = timezone.localtime(
            timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        historico_entry = f"Paciente Removido da agenda (em {data_atual} por {request.user})\n"
        agendamento.historico += historico_entry
        agendamento.save()
    else:
        agendamento_id = request.GET.get('agendamento_id')
    return consultarAgendaDia(request=request, filtro_agenda=data)


def removerPacienteConfirmarAgenda(request):
    data = None
    if request.method == "POST":
        agendamento_id = request.POST.get('agendamento_id')
        print(agendamento_id)
        agendamento = Agendamentos.objects.filter(id=agendamento_id).first()
        data = agendamento.data_agendada
        agendamento.data_agendada = None
        agendamento.status = None
        agendamento.observacao = None
        data_atual = timezone.localtime(
            timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
        historico_entry = f"Paciente Removido da agenda (em {data_atual} por {request.user})\n"
        agendamento.historico += historico_entry
        agendamento.save()
    else:
        agendamento_id = request.GET.get('agendamento_id')
    return confirmarAgendamentos(request=request, data_agendada=data)
