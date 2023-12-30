from datetime import date, datetime, timedelta
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from medicos.views import mostrarMedicos
from pacientes.views import mostrarPacientes
from .forms import CadastrarAgendamentos, AtualizarAgendamentos
from procedimentos.views import mostrarProcedimentos
from django.contrib import messages
from .models import Agendamentos
from django.template.loader import get_template
from xhtml2pdf import pisa

def cadastrarAgendamentos(request):
    if request.method == "POST":
        form = CadastrarAgendamentos(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)            
            agendamento.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
    else:
        form = CadastrarAgendamentos()

    pacientes = mostrarPacientes(request).order_by('nome')  # Ordena os pacientes pelo campo 'nome'
    procedimentos = mostrarProcedimentos(request).order_by('nome')  # Ordena os procedimentos pelo campo 'nome'
    medicos = mostrarMedicos(request).order_by('nome')  # Ordena os médicos pelo campo 'nome'

    return render(request, 'cadastrarAgendamentos.html', {'form': form, 'pacientes': pacientes, 'procedimentos': procedimentos, 'medicos': medicos})

def confirmarAgendamentos(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        total_items = len(post_data.getlist('id_agendamento'))
        status_filtrar = request.POST.get('status_filtrar')  # Adicione esta linha

        for contador in range(0, total_items):
            agendamento_id = post_data.getlist('id_agendamento')[contador]
            status = post_data.getlist('status')[contador]
            observacao = post_data.getlist('observacao')[contador]
            if status == 'não confirmado':
                continue

            try:
                agendamento = Agendamentos.objects.get(id=agendamento_id)
                form = AtualizarAgendamentos({'id': agendamento_id, 'status': status, 'observacao': observacao}, instance=agendamento)

                if form.is_valid():
                    form.save()

                    # Atualize o oct e calcule a próxima data útil
                    agendamento.oct += 1
                    agendamento.data_agendada = calcular_proximo_dia_util(agendamento.data_agendada)
                    agendamento.save()

                else:
                    messages.error(request, '')
            except Agendamentos.DoesNotExist:
                # Lidar com o caso em que o agendamento correspondente não existe
                pass

        messages.success(request, 'Agendamentos atualizados com sucesso!')

    data_selecionada = request.POST.get('data_selecionada')
    if data_selecionada is None:
        data_selecionada = date.today() + timedelta(days=1)
    else:
        data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()

    print(data_selecionada)

    data_selecionada_formatada = data_selecionada.strftime('%Y-%m-%d')

    print(data_selecionada_formatada)

    # Aplique a condição do status ao filtro
    agendamentos = Agendamentos.objects.filter(data_agendada=data_selecionada, status=status_filtrar).order_by(
        'id_paciente_id__nome')

    form = AtualizarAgendamentos(request.POST)

    return render(request, 'confirmarAgendamentos.html', {'agendamentos': agendamentos, 'form': form, 'data_selecionada': data_selecionada_formatada, 'status_filtrar': status_filtrar})

def consultarAgendaDia(request):
    if request.method == "POST":
        filtro_data = request.POST.get('filtro_data')
        if filtro_data:
            data = datetime.strptime(filtro_data, '%Y-%m-%d').date()
        else:
            data = proximo_dia_util_apos(date.today())
    else:
        data = proximo_dia_util_apos(date.today())

    agendamentos = Agendamentos.objects.filter(data_agendada=data).order_by('id_paciente_id__nome')
    return render(request, 'consultarAgendaDia.html', {'agendamentos': agendamentos, 'data': data})

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
        data_atual = datetime.now()
        data_selecionada = proximo_dia_util_apos(data_atual.date())

    if request.method == 'POST':
        # Obtenha a lista de IDs dos agendamentos selecionados
        agendamento_ids = request.POST.get('agendamento_ids', '').split(',')

        # Obtenha os agendamentos correspondentes aos IDs selecionados
        agendamentos = Agendamentos.objects.filter(id__in=agendamento_ids, data_agendada=data_selecionada)

    # Crie o contexto com os dados a serem passados para o modelo
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

def calcular_proxima_data(data_inicial):
    # Lógica para calcular a próxima data útil
    um_dia = timedelta(days=1)
    dias_uteis = 0

    while dias_uteis < 30:
        data_inicial += um_dia
        if data_inicial.weekday() < 5:  # Verifica se é um dia útil (segunda a sexta)
            dias_uteis += 1

    return data_inicial

def proximo_dia_util_apos(data):
    um_dia = timedelta(days=1)
    while data.weekday() in [5, 6]:  # 5 é sábado, 6 é domingo
        data += um_dia
    return data