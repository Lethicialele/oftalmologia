from django.db import models

class Medicos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.CharField(max_length=100, default="NÃO INFORMADO")
    data_nascimento = models.DateField(null=True)
