from datetime import date
from django.shortcuts import render
from pacientes.views import mostrarPacientes
from .forms import CadastroAgendamentos
from procedimentos.views import mostrarProcedimentos
from django.contrib import messages
from .models import Agendamentos

# Create your views here.

def cadastrarAgendamentos(request):
    if request.method == "POST":
        form = CadastroAgendamentos(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
    else:
        form = CadastroAgendamentos()

    return render(request, 'cadastrarAgendamentos.html', {'form': form, 'pacientes': mostrarPacientes(request), 'procedimentos': mostrarProcedimentos(request)})


def confirmarAgendamentos(request):
    if request.method == "POST":
        agendamento_id = request.POST.get('agendamento_id')
        observacao = request.POST.get('observacao')
        status = request.POST.get('status')

        try:
            agendamento = Agendamentos.objects.get(id=agendamento_id)
            agendamento.observacao = observacao
            agendamento.status = status
            agendamento.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
        except Agendamentos.DoesNotExist:
            messages.error(request, 'Agendamento não encontrado.')

    agendamentos = Agendamentos.objects.filter(data_agendada=date.today())
    return render(request, 'confirmarAgendamentos.html', {'agendamentos': agendamentos})


def consultarAgendaDia(request):
    agendamentos = Agendamentos.objects.filter(data_agendada=date.today())
    return render(request, 'consultarAgendaDia.html', {'agendamentos':agendamentos})

