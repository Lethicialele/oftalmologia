from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from medicos.models import Medicos
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import AtualizarCadastroMedico, CadastroMedicos
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

def atualizarCadastrorMedicos(request):
    medico = request.user
    medico_id = medico.id
    medico = Medicos.objects.filter(id=medico_id).first()

    if request.method == "POST":
        form = AtualizarCadastroMedico(request.POST, instance=medico)
        password_form = PasswordChangeForm(medico, request.POST)
        print(request.POST)

        if 'nova_senha' in request.POST:
            # Se a solicitação for para alterar a senha
            if password_form.is_valid():
                medico = password_form.save(commit=False)
                medico.save()
                update_session_auth_hash(request, medico)  # Atualiza a sessão para evitar logout
                messages.success(request, 'Senha atualizada com sucesso!')
                return render(request, 'perfil.html', {'usuario': request.user, 'medico': medico, 'form': form, 'password_form': password_form})
            else:
                messages.error(request, 'Algo errado com a senha.')

        elif form.is_valid():
            form.save()
            messages.success(request, 'Dados do paciente atualizados com sucesso!')
            return render(request, 'perfil.html', {'usuario': request.user, 'medico': medico, 'form': form, 'password_form': password_form})
        else:
            _, error = next(iter(form.errors.items()))
            messages.error(request, error)

    else:
        form = AtualizarCadastroMedico(instance=medico)
        password_form = PasswordChangeForm(medico)

    return render(request, 'perfil.html', {'usuario': request.user, 'medico': medico, 'form': form, 'password_form': password_form})

def sair(request): 
    logout(request)
    return redirect('/medicos/loginMedicos/')