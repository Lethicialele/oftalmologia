from django import forms
from django.contrib.auth.forms import UserCreationForm
from medicos.models import Medicos

class CadastroMedicos(forms.ModelForm):
    class Meta:
        model = Medicos
        fields = ['crm', 'nome', 'especialidade', 'telefone', 'email', 'assinatura']

class AtualizarCadastroMedico(forms.ModelForm):
    class Meta:
        model = Medicos
        fields = ['crm', 'nome', 'especialidade', 'telefone', 'email', 'assinatura']

