# Generated by Django 4.2.2 on 2024-02-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0026_agendamentos_ultima_atualizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamentos',
            name='nome',
            field=models.CharField(max_length=180),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='nome_mae',
            field=models.CharField(default='', max_length=185, null=True),
        ),
    ]
