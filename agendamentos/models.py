from django.db import models
from django.db import models
from medicos.models import Medicos
from pacientes.models import Pacientes
from procedimentos.models import Procedimentos


class Agendamentos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    id_paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    id_procedimento = models.ForeignKey(Procedimentos, on_delete=models.CASCADE)
    id_medico = models.ForeignKey(Medicos, on_delete=models.CASCADE)
    numero_de_olhos = models.IntegerField(choices=[(1, '1'), (2, '2')])
    olho_agendado = models.CharField(max_length=10, choices=[('esquerdo', 'Esquerdo'), ('direito', 'Direito'), ('ambos', 'Ambos')], default="Ambos")
    oct = models.BooleanField(default=False)
    data_agendada = models.DateField()
    diagnostico = models.CharField(max_length=500, null=True)
    observacao = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    atendido = models.BooleanField(default=False)
    aplicacao_atual = models.IntegerField(null= True, default=0)
    quantidade_aplicacoes_necessarias = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            procedimento = self.id_procedimento
            self.quantidade_aplicacoes_necessarias = procedimento.quantidade_aplicacoes

        super().save(*args, **kwargs)
