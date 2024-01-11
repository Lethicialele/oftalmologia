from django.db import models
from django.db import models
from pacientes.models import Pacientes
from procedimentos.models import Procedimentos
from django.contrib.auth.models import User 


class Agendamentos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True, null=True)
    nome_mae = models.CharField(max_length=100, default="", null=True)
    cartao_sus = models.CharField(max_length=100, default="")
    clinica = models.CharField(max_length=100, default="", null=True)
    enfermaria = models.CharField(max_length=100, default="", null=True)
    leito = models.CharField(max_length=100, default="", null=True)
    telefone = models.CharField(max_length=15)
    prontuario = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    data_nascimento = models.DateField(null=True)
    numero_de_olhos = models.IntegerField(choices=[(1, '1'), (2, '2')])
    olho_agendado = models.CharField(max_length=10, choices=[('esquerdo', 'Esquerdo'), ('direito', 'Direito'), ('ambos', 'Ambos')], default="Ambos")
    oct = models.BooleanField(default=False)
    data_agendada = models.DateField(null=True)
    ultimo_atendimento = models.DateField(null=True)
    diagnostico = models.CharField(max_length=500, null=True)
    observacao = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, default='não confirmado')
    atendido = models.PositiveIntegerField(default=0)
    faltas = models.PositiveIntegerField(default=0)
    aplicacao_atual = models.IntegerField(null= True, default=0)
    quantidade_aplicacoes_necessarias = models.IntegerField(default=3)
    historico = models.TextField(default='')
    numero_atualizacoes = models.PositiveIntegerField(default=0)

