from datetime import date, datetime, timedelta
from django.shortcuts import render
from medicos.views import mostrarMedicos
from pacientes.views import mostrarPacientes
from .forms import CadastrarAgendamentos, AtualizarAgendamentos
from procedimentos.views import mostrarProcedimentos
from django.contrib import messages
from .models import Agendamentos

# Create your views here.

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
        agendamentos = Agendamentos.objects.filter(data_agendada=data, status__isnull=True)
        form = AtualizarAgendamentos(request.POST)
        if form.is_valid():
            post_data = request.POST.copy()  # Copiar os dados do POST para manipulação
            total_items = len(post_data.getlist('id_agendamento'))

            for contador in range(1, total_items + 1):
                agendamento_id = post_data.getlist('id_agendamento')[contador - 1]
                status = post_data.getlist('status')[contador - 1]
                observacao = post_data.getlist('observacao')[contador - 1]

                try:
                    agendamento = Agendamentos.objects.get(id=agendamento_id)
                    agendamento.status = status
                    agendamento.observacao = observacao
                    agendamento.save()
                except Agendamentos.DoesNotExist:
                    # Lidar com o caso em que o agendamento correspondente não existe
                    pass

            messages.success(request, 'Agendamentos atualizados com sucesso!')

        else:
            messages.error(request, '')
    else:
        agendamentos = Agendamentos.objects.filter(data_agendada=(date.today() + timedelta(days=1)), status__isnull=True)
        form = AtualizarAgendamentos(request.POST)

    return render(request, 'confirmarAgendamentos.html', {'agendamentos': agendamentos, 'form': form, "data":data})

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

def consultarAgendaDia(request, data=date.today()+timedelta(days=1)):
    agendamentos = Agendamentos.objects.filter(data_agendada=data)
    return render(request, 'consultarAgendaDia.html', {'agendamentos':agendamentos})

