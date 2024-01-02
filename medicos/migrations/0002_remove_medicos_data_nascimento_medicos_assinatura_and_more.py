# Generated by Django 4.2.2 on 2024-01-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicos',
            name='data_nascimento',
        ),
        migrations.AddField(
            model_name='medicos',
            name='assinatura',
            field=models.ImageField(blank=True, null=True, upload_to='assinaturas/'),
        ),
        migrations.AddField(
            model_name='medicos',
            name='crm',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
