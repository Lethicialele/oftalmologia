# Generated by Django 4.2.2 on 2024-02-13 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0025_alter_agendamentos_data_cadastro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentos',
            name='ultima_atualizacao',
            field=models.DateField(null=True),
        ),
    ]