from django.shortcuts import render
from django.http import HttpResponse
from .forms import CadastroAgendamentos

# Create your views here.

def cadastrarAgendamentos(request):
    if request.method == "GET":
       return render(request, 'cadastrarAgendamentos.html', {})
    elif request.method == "POST":
        print(request.POST)
        form = CadastroAgendamentos(request.POST)
        
        if form.is_valid():
            return render(request, 'cadastrarAgendamentos.html', {})
            #return render(request, 'consultarAgendamentos.html', {})

        #dados = request.POST
        #nome = request.POST.get('nome')
        #print(dados)
        print('AGENDAMENTO CADASTRADO')
        #return render(request, 'consultarAgendamentos.html', {'form':form})
