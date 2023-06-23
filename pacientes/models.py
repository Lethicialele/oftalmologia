from django.db import models

class Pacientes(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    prontuario = models.IntegerField(null=True)
    email = models.CharField(max_length=100, default="NÃO INFORMADO")
    data_nascimento = models.DateField(null=True)
