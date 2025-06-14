# Generated by Django 5.2 on 2025-06-11 23:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_usuario_groups_usuario_is_active_usuario_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='correo_personal',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='sexo',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')]),
        ),
    ]
