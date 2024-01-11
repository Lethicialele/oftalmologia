from datetime import date, datetime, timedelta
from locale import setlocale, LC_TIME
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from medicos.views import mostrarMedicos
from .forms import AtualizarCadastroAgendamentos, CadastrarAgendamentos, AtualizarAgendamentos
from django.contrib import messages
from .models import Agendamentos
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import F, ExpressionWrapper, fields, Value
from django.db.models.functions import Now


def cadastrarAgendamentos(request):
    if request.method == "POST":
        form = CadastrarAgendamentos(request.POST)
        if form.is_valid():
            # Salvando os dados mesmo que alguns campos estejam vazios
            agendamento = form.save(commit=False)
            agendamento.nome_mae = form.cleaned_data['nome_mae']
            agendamento.enfermaria = form.cleaned_data['enfermaria']
            agendamento.clinica = form.cleaned_data['clinica']
            agendamento.leito = form.cleaned_data['leito']
            agendamento.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            _, error = next(iter(form.errors.items()))
            messages.error(request, error)
    else:
        form = CadastrarAgendamentos()

    return render(request, 'cadastrarAgendamentos.html', {'usuario': request.user, 'form': form})

def confirmarAgendamentos(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        total_items = len(post_data.getlist('id_agendamento'))
        
        for contador in range(0, total_items):
            agendamento_id = post_data.getlist('id_agendamento')[contador]
            status = post_data.getlist('status')[contador]
            print(status)
            observacao = post_data.getlist('observacao')[contador]
            try:
                agendamento = Agendamentos.objects.get(id=agendamento_id)
                form = AtualizarAgendamentos({'id': agendamento_id, 'status': status, 'observacao': observacao}, instance=agendamento)
                if form.is_valid():                    
                    if status == 'não confirmado':
                        agendamento.observacao = observacao
                        historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
                        agendamento.historico += historico_entry
                        agendamento.numero_atualizacoes += 1                        
                        form.save()
                    elif status == 'confirmado':
                        agendamento.numero_atualizacoes += 1
                        if agendamento.atendido == 3:
                            agendamento.oct = True
                            agendamento.status = 'concluido'
                            historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
                            agendamento.historico += historico_entry
                            agendamento.observacao = observacao
                        else:
                            historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
                            agendamento.historico += historico_entry
                            agendamento.status = 'confirmado'
                            agendamento.observacao = observacao
                    elif status == 'cancelado':
                        historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
                        agendamento.historico += historico_entry
                        agendamento.status = 'cancelado'
                        agendamento.observacao = observacao
                        agendamento.numero_atualizacoes += 1

                    agendamento.save()
                else:
                    messages.error(request, '')
            except Agendamentos.DoesNotExist:
                # Lidar com o caso em que o agendamento correspondente não existe
                pass

        messages.success(request, 'Agendamentos atualizados com sucesso!')
    data_selecionada = request.GET.get('data_selecionada')
    if data_selecionada is None:
        data_selecionada = f'{(date.today() + timedelta(days=1))}'
    data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()

    print(data_selecionada)

    # Aplique a condição do status ao filtro
    agendamentos = Agendamentos.objects.filter(data_agendada=data_selecionada, status__in=['não confirmado', 'cancelado'])

    form = AtualizarAgendamentos(request.POST)
    status = ''
       
    return render(request, 'confirmarAgendamentos.html', {'usuario': request.user, 'agendamentos': agendamentos, 'form': form, 'data_selecionada': data_selecionada, 'status': status })

def confirmarAtendimentos(request):
    setlocale(LC_TIME, 'pt_BR.utf-8')

    agendamentos = None  # Declare a variável aqui para garantir visibilidade

    if request.method == "POST":
        data_selecionada = request.POST.get('data_selecionada')
        data_parseada = datetime.strptime(data_selecionada, '%d de %B de %Y')
        data_selecionada = data_parseada.strftime('%Y-%m-%d')
        post_data = request.POST.copy()
        print("Dados Template")
        print(post_data)
        atendidos_ids = post_data.get('atendidos_id').split(',')
        print(atendidos_ids)
        agendamentos = Agendamentos.objects.filter(id__in=atendidos_ids)

        for contador, agendamento in enumerate(agendamentos):
            agendamento.numero_atualizacoes += 1
            agendamento.atendido += 1
            agendamento.aplicacao_atual +=1
            print(agendamento.atendido)

            if agendamento.atendido == 3:
                agendamento.oct = True
                agendamento.status = 'concluido'
            else:
                agendamento.status = ''
                agendamento.observacao = ''
                agendamento.faltas = 0

            historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: {agendamento.observacao}\n"
            agendamento.historico += historico_entry
            agendamento.ultimo_atendimento = data_selecionada
            agendamento.data_agendada = None
            agendamento.save()

        agendamentos = Agendamentos.objects.filter(data_agendada=data_selecionada)
        
        for contador, agendamento in enumerate(agendamentos):
            historico_entry = f"{agendamento.data_agendada} - Status: {agendamento.status}, Observação: FALTOU\n"
            agendamento.historico += historico_entry
            agendamento.status = ''
            agendamento.observacao = ''
            agendamento.data_agendada = None
            agendamento.faltas += 1
            if(agendamento.faltas >=3):
                agendamento.status = 'cancelado'
            
            agendamento.save()
            
        agendamentos = Agendamentos.objects.filter(data_agendada=data_selecionada)
        messages.success(request, 'Agendamentos atualizados com sucesso!')
        return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data_parseada})  

    return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data_selecionada})

def consultarAgendaDia(request, filtro_agenda = None):
    if request.method == "POST":
        filtro_data = request.POST.get('filtro_data')
        if filtro_data:
            data = datetime.strptime(filtro_data, '%Y-%m-%d').date()
        else:
            data = date.today() + timedelta(days=1)
    else:
        data = datetime.strptime(filtro_agenda, '%Y-%m-%d').date() if filtro_agenda else date.today() + timedelta(days=1)
    agendamentos = Agendamentos.objects.filter(data_agendada=data, status__in=['não confirmado', 'confirmado'])
    print(data)
    print(agendamentos)
    return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data})

def gerarAgenda(request):
    if request.method == 'POST':
        # Processar o formulário de geração de agenda
        data_agendada = request.POST.get('data_agendada')
        quantidade_pacientes = int(request.POST.get('quantidade_pacientes', 0))

        if not data_agendada or quantidade_pacientes <= 0:
            # Lógica de validação, redirecione ou retorne uma resposta de erro conforme necessário
            return HttpResponse('Dados inválidos para geração de agenda', status=400)
       
        agendamentos = Agendamentos.objects.raw('''
            SELECT *
            FROM agendamentos_agendamentos
            WHERE status not in ('concluido', 'cancelado') and data_agendada is null
            HAVING (datediff(now(), ultimo_atendimento) >= 30 and data_agendada < now()) or (datediff(now(), ultimo_atendimento) IS NULL)
                ORDER BY data_nascimento desc, aplicacao_atual desc
            LIMIT %s
        ''', [quantidade_pacientes])

        for agendamento in agendamentos:
            agendamento.data_agendada = data_agendada
            agendamento.status = 'não confirmado'
            agendamento.save()

        data_agendada = datetime.strptime(data_agendada, '%Y-%m-%d').date()
        return render(request, 'consultarAgendaDia.html', {'usuario': request.user, 'agendamentos': agendamentos, 'data': data_agendada})

    # Renderize a página de geração de agenda (substitua com o caminho real do seu template)
    return render(request, 'gerarAgenda.html', {'usuario': request.user})

def gerarRelatorio(request):
   # Recupere os dados necessários para o relatório
    agendamentos = Agendamentos.objects.all()  # Substitua isso pela lógica de obtenção de dados desejada

    # Carregue o template HTML
    template_path = 'relatorioTemplate.html'  # Substitua pelo caminho do seu template HTML
    template = get_template(template_path)
    context = {'agendamentos': agendamentos}

    # Renderize o template HTML
    html = template.render(context)

    # Crie um objeto de resposta HttpResponse com o cabeçalho de PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio.pdf"'

    # Crie o PDF real usando o HTML renderizado
    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='utf-8',
        link_callback=lambda uri, _: default_link_callback(uri, request)
    )

    # Se o PDF foi criado com sucesso, retorne-o na resposta
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o relatório em PDF', status=500)
    return response

def imprimirAgenda(request, data_selecionada):
    if data_selecionada is None:
        # Se a data não foi fornecida, definir como o próximo dia útil
        data_selecionada = f'{(date.today() + timedelta(days=1))}'

    if request.method == 'POST':
        # Obtenha a lista de IDs dos agendamentos selecionados
        agendamento_ids = request.POST.get('agendamento_ids', '').split(',')

        # Obtenha os agendamentos correspondentes aos IDs selecionados
        agendamentos = Agendamentos.objects.filter(id__in=agendamento_ids, data_agendada=data_selecionada)

    # Crie o contexto com os dados a serem passados para o modelo
    data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
    context = {'agendamentos': agendamentos, 'data_selecionada': data_selecionada}

    # Renderize o modelo
    template_path = 'imprimirAgenda.html'  # Atualize com o caminho correto
    template = get_template(template_path)
    html = template.render(context)

    # Crie um objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'

    # Converta o HTML para PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Se a conversão falhar, retorne um erro
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response

def default_link_callback(uri, req):
    if uri.startswith('http://') or uri.startswith('https://'):
        return uri
    return os.path.join(settings.MEDIA_ROOT, uri)

def consultarFilaEsperaPacientes(request):
    # Remova a parte do LIMIT para obter todos os pacientes
    consulta_sql = '''
        SELECT *
        FROM agendamentos_agendamentos
        WHERE status NOT IN ('concluido', 'cancelado') and data_agendada IS NULL

        ORDER BY data_nascimento DESC, aplicacao_atual DESC
    '''

    # Execute a consulta SQL
    agendamentos = Agendamentos.objects.raw(consulta_sql)

    # Renderize a página html com os resultados
    return render(request, 'consultarFilaEsperaPacientes.html', {'agendamentos': agendamentos, 'usuario': request.user})

def deletarPaciente(request):
    paciente_id = request.POST.get('paciente_id')
    agendamento = Agendamentos.objects.filter(id=paciente_id).first()
    agendamento.delete()

    messages.success(request, 'Paciente deletado com sucesso!')
    
    return redirect('consultarFilaEsperaPacientes')

def agendarPaciente(request):

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        data_agendada = request.POST.get("data_agendada")
        agendamento = Agendamentos.objects.filter(id=paciente_id).first()
    
        # Atualize o objeto agendamento com a nova data_agendada
        agendamento.data_agendada = data_agendada
        agendamento.status = 'não confirmado'
        agendamento.save()

        # Adicione mensagens de sucesso, se necessário
        messages.success(request, 'Paciente agendado com sucesso!')

        # Redirecionar para a página consultarAgendaDia com a data_agendada escolhida
        return redirect('consultarAgendaDiaFiltro', filtro_agenda=data_agendada)

    paciente_id = request.GET.get('paciente_id')

    agendamento = Agendamentos.objects.filter(id=paciente_id)

    return render(request, 'agendarPaciente.html', {'agendamento': agendamento.first(), 'usuario': request.user })

def atualizarCadastroAgendamento(request):
    agendamento_id = None
    # r = request.POST
    # print(r)
    # agendamento_id = request.POST.get('agendamento_id')
    # print(agendamento_id)
    # agendamento = Agendamentos.objects.filter(id=agendamento_id).first()
    # print(agendamento)
    if request.method == "POST":
        agendamento_id = request.POST.get('id')
        agendamento = Agendamentos.objects.filter(id=agendamento_id).first()
        form = AtualizarCadastroAgendamentos(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do paciente atualizados com sucesso!')
        else:            
            _, error = next(iter(form.errors.items()))
            messages.error(request, error)
    else:
        agendamento_id = request.GET.get('agendamento_id')

    agendamento = Agendamentos.objects.filter(id=agendamento_id).first()

    return render(request, 'atualizarCadastroAgendamento.html', {'usuario': request.user, 'agendamento':agendamento})