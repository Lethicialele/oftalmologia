# Generated by Django 4.2.2 on 2023-12-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0010_agendamentos_aplicacao_atual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamentos',
            name='atendido',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='status',
            field=models.CharField(default='não confirmado', max_length=20),
        ),
    ]