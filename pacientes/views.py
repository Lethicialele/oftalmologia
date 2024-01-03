from django.shortcuts import render, redirect
from django.http import HttpResponse
from pacientes.models import Pacientes
from .forms import CadastroPacientes
from django.contrib import messages

# Create your views here.


def cadastrarPacientes(request):
    if request.method == "POST":
        form = CadastroPacientes(request.POST)

        # Validar o CPF antes de salvar
        cpf = form['cpf'].value()
        if not validarCpf(cpf):
            messages.error(request, 'CPF inválido! Verifique o CPF e tente novamente.')
            return render(request, 'cadastrarPacientes.html', {'form': form})

        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            messages.error(request, 'Dados inválidos! Verifique os dados ou se o paciente já é cadastrado')

    else:
        form = CadastroPacientes()

    return render(request, 'cadastrarPacientes.html', {'form': form})

def mostrarPacientes(request):
    return Pacientes.objects.all()

def validarCpf(cpf):
    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula os dígitos verificadores
    total = 0
    multiplicador = 10

    for i in range(9):
        total += int(cpf[i]) * multiplicador
        multiplicador -= 1

    resto = total % 11
    digito1 = 11 - resto if resto >= 2 else 0

    total = 0
    multiplicador = 11

    for i in range(10):
        total += int(cpf[i]) * multiplicador
        multiplicador -= 1

    resto = total % 11
    digito2 = 11 - resto if resto >= 2 else 0

    # Verifica se os dígitos verificadores estão corretos
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
