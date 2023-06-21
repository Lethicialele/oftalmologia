from django import forms
from .models import Pacientes

class CadastroPacientes(forms.ModelForm):

    class Meta:
        model =  Pacientes
        fields = ('nome', 'cpf', 'telefone', 'prontuario', 'data_nascimento')