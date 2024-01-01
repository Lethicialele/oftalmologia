from django import forms
from .models import Medicos

class CadastroMedicos(forms.ModelForm):
    class Meta:
        model =  Medicos
        fields = ('crm', 'nome', 'especialidade', 'email', 'telefone', 'assinatura')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicione classes CSS ou atributos personalizados conforme necessário
        self.fields['assinatura'].widget.attrs['class'] = 'form-control-file'
