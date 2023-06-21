from django.db import models
from pacientes.models import Pacientes
from procedimentos.models import Procedimentos


class Agendamentos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    id_paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    id_procedimento = models.ForeignKey(Procedimentos, on_delete=models.CASCADE)
    numero_de_olhos = models.IntegerField(choices=[(1, '1'), (2, '2')])
    olho_agendado = models.CharField(max_length=10, choices=[('esquerdo', 'Esquerdo'), ('direito', 'Direito'), ('ambos', 'Ambos')])
    oct = models.BooleanField()
    data_agendada = models.DateField()
    diagnostico = models.CharField(max_length=500)
