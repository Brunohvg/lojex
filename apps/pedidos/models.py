# pedidos/models.py
from django.db import models
from apps.lojas.models import Loja
from apps.entregas.models import Entrega

class Pedido(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="pedidos")
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, null=True, blank=True, related_name="pedido")
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pendente")  # Ex.: Pendente, Em processamento, Concluído, Cancelado

    def __str__(self):
        return f"Pedido #{self.id} - {self.loja.nome}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']