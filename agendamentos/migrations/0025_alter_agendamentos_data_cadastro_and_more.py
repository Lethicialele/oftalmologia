# Generated by Django 4.2.2 on 2024-01-23 22:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0024_agendamentos_data_cadastro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamentos',
            name='data_cadastro',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='nivel_prioridade',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
