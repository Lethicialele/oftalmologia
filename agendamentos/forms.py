from django import forms
from .models import Agendamentos

class CadastrarAgendamentos(forms.ModelForm):
    class Meta:
        model = Agendamentos
        fields = ('id_paciente', 'id_procedimento', 'id_medico', 'numero_de_olhos', 'olho_agendado', 'data_agendada', 'diagnostico')

class AtualizarAgendamentos(forms.ModelForm):
    id = forms.IntegerField()
    status = forms.ChoiceField(choices=[('não confirmado', 'Não confirmado'), ('confirmado', 'Confirmado'), ('remarcar', 'Remarcar'), ('cancelado', 'Cancelado')], initial= 'não confirmado')
    observacao = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Agendamentos
        fields = ('id', 'status', 'observacao')
