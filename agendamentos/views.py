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

def filtrarAgendamentos(request):
    if request.method == "POST":
        filtro_data = request.POST.get('filtro_data')
        if filtro_data:
            data = datetime.strptime(filtro_data, '%Y-%m-%d').date()
        else:
            data = date.today()
    else:
        data = date.today()
    return confirmarAgendamentos(request, data)

def confirmarAgendamentos(request, data=None):
    if request.method == "POST":
        post_data = request.POST.copy()
        total_items = len(post_data.getlist('id_agendamento'))

        for contador in range(0, total_items):
            agendamento_id = post_data.getlist('id_agendamento')[contador]
            status = post_data.getlist('status')[contador]
            observacao = post_data.getlist('observacao')[contador]
            if(status == 'não confirmado') :continue
            try:
                agendamento = Agendamentos.objects.get(id=agendamento_id)               
                form = AtualizarAgendamentos({'id': agendamento_id, 'status': status, 
                                              'observacao': observacao}, instance=agendamento)
                
                if form.is_valid():
                    form.save()
                else:
                    messages.error(request, '')
            except Agendamentos.DoesNotExist:
                # Lidar com o caso em que o agendamento correspondente não existe
                pass
        print(data)
        agendamentos = Agendamentos.objects.filter(data_agendada=data, status="não confirmado")
        messages.success(request, 'Agendamentos atualizados com sucesso!')
    else:
        data = request.GET.get('data')
        if(data == None) :
            data = date.today() + timedelta(days=1)
        else :
            data = date.fromisoformat(data)
        agendamentos = Agendamentos.objects.filter(data_agendada=data, status="não confirmado")       
    
    # Ordenar agendamentos pelo nome do paciente em ordem alfabética
    agendamentos = agendamentos.order_by('id_paciente_id__nome')

    form = AtualizarAgendamentos(request.POST)

    return render(request, 'confirmarAgendamentos.html', {'agendamentos': agendamentos, 'form': form, 'data': data})


def filtrarAgendamentosAgendaDia(request):
    if request.method == "POST":
        filtro_data = request.POST.get('filtro_data')
        if filtro_data:
            data = datetime.strptime(filtro_data, '%Y-%m-%d').date()
        else:
            data = date.today()
    else:
        data = date.today()
    return consultarAgendaDia(request, data)

def consultarAgendaDia(request, data=date.today() + timedelta(days=1)):
    agendamentos = Agendamentos.objects.filter(data_agendada=data).order_by('id_paciente_id__nome')
    return render(request, 'consultarAgendaDia.html', {'agendamentos': agendamentos})

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

def default_link_callback(uri, req):
    # Converte links de HTML para caminhos de sistema de arquivos
    if uri.startswith('http://') or uri.startswith('https://'):
        return uri
    return os.path.join(settings.MEDIA_ROOT, uri)