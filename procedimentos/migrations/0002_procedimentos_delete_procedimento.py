# Generated by Django 4.2.2 on 2023-06-21 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedimentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Procedimentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=40)),
                ('quantidade_aplicacoes', models.IntegerField(null=True)),
                ('intervalo_aplicacoes_dias', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Procedimento',
        ),
    ]
