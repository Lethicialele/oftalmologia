from django.db import models
from django.contrib.auth.models import User 

class Medicos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    crm = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.CharField(max_length=100, default="NÃO INFORMADO")
    assinatura = models.ImageField(upload_to='assinaturas/', blank=True, null=True)

    def __str__(self):
        return self.nome
