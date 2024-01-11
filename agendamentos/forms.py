from django import forms
from .models import Agendamentos

class CadastrarAgendamentos(forms.ModelForm):
    class Meta:
        model = Agendamentos
        fields = ('numero_de_olhos', 'olho_agendado', 'diagnostico', 'nome', 'cpf', 'telefone', 'prontuario', 'email', 'data_nascimento', 'cartao_sus')

    nome_mae = forms.CharField(required=False)
    enfermaria = forms.CharField(required=False)
    clinica = forms.CharField(required=False)
    leito = forms.CharField(required=False)

    def clean_nome_mae(self):
        nome_mae = self.cleaned_data['nome_mae']
        return nome_mae.strip() if nome_mae else None

    def clean_enfermaria(self):
        enfermaria = self.cleaned_data['enfermaria']
        return enfermaria.strip() if enfermaria else None

    def clean_clinica(self):
        clinica = self.cleaned_data['clinica']
        return clinica.strip() if clinica else None

    def clean_leito(self):
        leito = self.cleaned_data['leito']
        return leito.strip() if leito else None

class AtualizarAgendamentos(forms.ModelForm):
    id = forms.IntegerField()
    status = forms.ChoiceField(choices=[('não confirmado', 'Não confirmado'), ('confirmado', 'Confirmado'), ('remarcar', 'Remarcar'), ('cancelado', 'Cancelado')], initial= 'não confirmado')
    observacao = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Agendamentos
        fields = ('id', 'status', 'observacao')

class AtualizarCadastroAgendamentos(forms.ModelForm):
    id = forms.IntegerField()
    nome_mae = forms.CharField(required=False)
    enfermaria = forms.CharField(required=False)
    clinica = forms.CharField(required=False)
    leito = forms.CharField(required=False)
    class Meta:
        model = Agendamentos
        fields = ('id','numero_de_olhos', 'olho_agendado', 'diagnostico', 'telefone', 'email', 'nome_mae', 'enfermaria','clinica', 'leito' )