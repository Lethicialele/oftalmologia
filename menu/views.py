from django.shortcuts import render
from pacientes.views import cadastrarPacientes
from agendamentos.views import *

def home(request):
    return render(request, 'home.html')
