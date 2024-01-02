from django.contrib.auth import login
from django.shortcuts import render, redirect
from medicos.models import Medicos
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroMedicos
from django.contrib import messages
from django.contrib.auth.models import User 

# Create your views here.
def cadastrarMedicos(request):
    if request.method == "POST":
        form_medico = CadastroMedicos(request.POST)
        if form_medico.is_valid():
            usuario_nome = request.POST['nome']
            usuario_senha = request.POST['senha']
            usuario_email = request.POST['email']
            usuario = User.objects.create_user(usuario_nome, usuario_email, usuario_senha)
            usuario.save()
            
            medico = form_medico.save(commit=False)
            medico.usuario = usuario
            medico.save()
            messages.success(request, 'Médico cadastrado com sucesso!')
            return redirect('loginMedicos')
    else:
        form_medico = CadastroMedicos()

    return render(request, 'cadastrarMedicos.html', {'form_medico': form_medico})
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