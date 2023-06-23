# Generated by Django 4.2.2 on 2023-06-20 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='idade',
        ),
        migrations.AddField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paciente',
            name='data_nascimento',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='prontuario',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='telefone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]