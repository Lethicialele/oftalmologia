from django.shortcuts import render
from django.http import HttpResponse
from .forms import CadastroProcedimentos

# Create your views here.

def cadastrarProcedimentos(request):
    if request.method == "GET":
       return render(request, 'cadastrarProcedimentos.html', {})
    elif request.method == "POST":
        print(request.POST)
        form = CadastroProcedimentos(request.POST)
        
        if form.is_valid():
            return render(request, 'cadastrarProcedimentos.html', {})
            #return render(request, 'cadastrarProcedimentos.html', {})

        #dados = request.POST
        #nome = request.POST.get('nome')
        #print(dados)
        print('PROCEDIMENTO CADASTRADO')
        #return render(request, 'cadastrarProcedimentos.html', {'form':form})
