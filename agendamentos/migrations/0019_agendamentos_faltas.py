# Generated by Django 4.2.2 on 2024-01-08 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0018_alter_agendamentos_ultimo_atendimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentos',
            name='faltas',
            field=models.PositiveIntegerField(default=0),
        ),
    ]