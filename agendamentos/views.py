from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
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
            form.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
    return render(request, 'cadastrarAgendamentos.html', {'pacientes': mostrarPacientes(request), 'procedimentos': mostrarProcedimentos(request)})

def consultarAgendaDia(request):
    agendamentos = Agendamentos.objects.filter(data_agendada=date.today())
    return render(request, 'consultarAgendaDia.html', {'agendamentos':agendamentos})

def confirmarAgendamentos(request):
    agendamentos = Agendamentos.objects.filter(data_agendada=date.today())
    return render(request, 'confirmarAgendamentos.html', {'agendamentos':agendamentos})
