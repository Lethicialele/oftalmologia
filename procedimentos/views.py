from django.shortcuts import render
from django.http import HttpResponse
from .forms import CadastroProcedimentos
from .models import Procedimentos
from django.contrib import messages
# Create your views here.


def cadastrarProcedimentos(request):
   if request.method == "POST":
        form = CadastroProcedimentos(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos!')
   return render(request, 'cadastrarProcedimentos.html', {})
         
def mostrarProcedimentos(request):
    return Procedimentos.objects.all()
