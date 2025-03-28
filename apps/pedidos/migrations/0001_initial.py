# Generated by Django 5.1.7 on 2025-03-25 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entregas', '0001_initial'),
        ('lojas', '0002_loja_telefone_alter_loja_cnpj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pendente', max_length=50)),
                ('entrega', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedido', to='entregas.entrega')),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='lojas.loja')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-data_pedido'],
            },
        ),
    ]
