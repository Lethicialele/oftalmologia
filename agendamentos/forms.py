from django import forms
from .models import Agendamentos

class CadastroAgendamentos(forms.ModelForm):

    class Meta:
        model =  Agendamentos
        fields = ('numero_de_olhos','olho_agendado', 'oct', 'data_agendada', 'diagnostico')