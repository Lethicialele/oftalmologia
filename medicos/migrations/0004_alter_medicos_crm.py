# Generated by Django 4.2.2 on 2024-01-12 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0003_medicos_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicos',
            name='crm',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]