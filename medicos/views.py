from django.shortcuts import render
from medicos.models import Medicos
from .forms import CadastroMedicos
from django.contrib import messages

# Create your views here.
def cadastrarMedicos(request):

    if request.method == "POST":
        form = CadastroMedicos(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
            
    return render(request, 'cadastrarMedicos.html', {})

def mostrarMedicos(request):
    return Medicos.objects.all()