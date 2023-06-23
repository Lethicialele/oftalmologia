from django.shortcuts import render, redirect
from django.http import HttpResponse
from pacientes.models import Pacientes
from .forms import CadastroPacientes
from django.contrib import messages

# Create your views here.
def cadastrarPacientes(request):

    if request.method == "POST":
        form = CadastroPacientes(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
            
    return render(request, 'cadastrarPacientes.html', {})

def mostrarPacientes(request):
    return Pacientes.objects.all()