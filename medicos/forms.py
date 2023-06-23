from django import forms
from .models import Medicos

class CadastroMedicos(forms.ModelForm):

    class Meta:
        model =  Medicos
        fields = ('nome', 'especialidade', 'email', 'telefone', 'data_nascimento')