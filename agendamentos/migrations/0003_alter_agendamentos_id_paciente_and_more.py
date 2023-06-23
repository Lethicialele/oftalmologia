# Generated by Django 4.2.2 on 2023-06-21 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_alter_pacientes_id'),
        ('procedimentos', '0002_procedimentos_delete_procedimento'),
        ('agendamentos', '0002_agendamentos_delete_agendamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamentos',
            name='id_paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.pacientes'),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='id_procedimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procedimentos.procedimentos'),
        ),
    ]