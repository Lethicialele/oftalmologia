from django import forms
from .models import Procedimentos

class CadastroProcedimentos(forms.ModelForm):

    class Meta:
        model =  Procedimentos
        fields = ('nome', 'quantidade_aplicacoes', 'intervalo_aplicacoes_dias')