# Generated by Django 4.2.2 on 2024-01-07 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0015_agendamentos_cartao_sus_agendamentos_clinica_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agendamentos',
            name='id_procedimento',
        ),
    ]
