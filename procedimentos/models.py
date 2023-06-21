from django.db import models

class Procedimentos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=40)
    quantidade_aplicacoes = models.IntegerField(null=True)
    intervalo_aplicacoes_dias = models.IntegerField(null=True)
