from django import forms
from .models import Agendamentos

class CadastrarAgendamentos(forms.ModelForm):
    class Meta:
        model = Agendamentos
        fields = ('id_paciente', 'id_procedimento', 'id_medico', 'numero_de_olhos', 'olho_agendado', 'data_agendada', 'diagnostico')

class AtualizarAgendamentos(forms.ModelForm):
    status = forms.ChoiceField(choices=[('confirmado', 'Confirmado'), ('remarcar', 'Remarcar'), ('cancelado', 'Cancelado')])
    observacao = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Agendamentos
        fields = ('status', 'observacao')
