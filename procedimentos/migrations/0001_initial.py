# Generated by Django 4.2.2 on 2023-06-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Procedimento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=40)),
                ('quantidade_aplicacoes', models.IntegerField(null=True)),
                ('intervalo_aplicacoes_dias', models.IntegerField(null=True)),
            ],
        ),
    ]
