# Generated by Django 5.1.7 on 2025-03-25 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojas', '0001_initial'),
        ('usuarios', '0002_rename_ativo_usuario_is_active_remove_usuario_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='loja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lojas.loja'),
        ),
    ]
