# Generated by Django 5.2.3 on 2025-06-29 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_usuario_nombre_de_usuario_alter_usuario_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='nombre_de_usuario',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
