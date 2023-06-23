from django import forms
from .models import Agendamentos

class CadastroAgendamentos(forms.ModelForm):
    olho_agendado = forms.ChoiceField(choices=[('esquerdo', 'Esquerdo'), ('direito', 'Direito'), ('ambos', 'Ambos')], initial='ambos')
    class Meta:
        model =  Agendamentos
        fields = ('id_paciente', 'id_procedimento','numero_de_olhos', 'olho_agendado', 'data_agendada', 'diagnostico')