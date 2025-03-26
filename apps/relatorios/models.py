# relatorios/models.py
from django.db import models
from apps.lojas.models import Loja

class Relatorio(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_entregas = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório da loja {self.loja.nome} de {self.data_inicio} a {self.data_fim}"

    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'
        ordering = ['-criado_em']