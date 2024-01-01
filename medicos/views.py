from django.contrib.auth import login
from django.shortcuts import render, redirect
from medicos.models import Medicos
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroMedicos
from django.contrib import messages

# Create your views here.
def cadastrarMedicos(request):
    if request.method == "POST":
        form = CadastroMedicos(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
            messages.success(request, 'Médico cadastrado com sucesso!')
        else:
            form = CadastroMedicos()                        
    return render(request, 'cadastrarMedicos.html', {})

def mostrarMedicos(request):
    return Medicos.objects.all()

def loginMedicos(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirecione para a página inicial após o login
    else:
        form = AuthenticationForm()
    return render(request, 'loginMedicos.html', {'form': form})