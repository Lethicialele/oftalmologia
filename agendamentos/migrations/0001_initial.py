# Generated by Django 4.2.2 on 2023-06-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_paciente', models.IntegerField()),
                ('id_procedimento', models.IntegerField()),
                ('numero_de_olhos', models.IntegerField(choices=[(1, '1'), (2, '2')])),
                ('olho_agendado', models.CharField(choices=[('esquerdo', 'Esquerdo'), ('direito', 'Direito'), ('ambos', 'Ambos')], max_length=10)),
                ('oct', models.BooleanField()),
                ('data_agendada', models.DateField()),
                ('diagnostico', models.CharField(max_length=500)),
            ],
        ),
    ]
