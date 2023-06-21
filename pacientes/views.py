from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CadastroPacientes

# Create your views here.
def cadastrarPacientes(request):
    if request.method == "GET":
       return render(request, 'cadastrarPacientes.html', {})
    elif request.method == "POST":
        form = CadastroPacientes(request.POST)
        if form.is_valid():
            form
            paciente = form.save()
            return redirect('/pacientes/cadastrarPacientes.html')

        #dados = request.POST
        #nome = request.POST.get('nome')
        #print(dados)
        print('PACIENTE CADASTRADO')
        return render(request, 'cadastrarPacientes.html', {'form':form})

def verPacientes(request):
    return HttpResponse('VER PACIENTES')