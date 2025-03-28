# Generated by Django 5.1.7 on 2025-03-25 23:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojas', '0002_loja_telefone_alter_loja_cnpj'),
        ('usuarios', '0003_usuario_loja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='loja',
        ),
        migrations.CreateModel(
            name='UsuarioLoja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=50)),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_associados', to='lojas.loja')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lojas_associadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'loja')},
            },
        ),
    ]
