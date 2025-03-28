# Generated by Django 5.1.7 on 2025-03-25 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lojas', '0002_loja_telefone_alter_loja_cnpj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateTimeField()),
                ('data_fim', models.DateTimeField()),
                ('total_vendas', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_entregas', models.IntegerField(default=0)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lojas.loja')),
            ],
            options={
                'verbose_name': 'Relatório',
                'verbose_name_plural': 'Relatórios',
                'ordering': ['-criado_em'],
            },
        ),
    ]
