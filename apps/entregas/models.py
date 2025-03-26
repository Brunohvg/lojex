# entregas/models.py
from django.db import models
from apps.lojas.models import Loja
from apps.motoboys.models import Motoboy
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_data_entrega(value):
    """ Valida a data de entrega para não permitir datas passadas. """
    if value < timezone.now():
        raise ValidationError("A data de entrega não pode ser no passado.")

class Entrega(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="entregas")
    motoboy = models.ForeignKey(Motoboy, on_delete=models.SET_NULL, null=True, blank=True, related_name="entregas")
    descricao = models.TextField()
    endereco = models.CharField(max_length=255)
    data_entrega = models.DateTimeField(validators=[validate_data_entrega])
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    entregue = models.BooleanField(default=False)

    def __str__(self):
        return f"Entrega para {self.loja.nome} - {self.descricao}"

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['data_entrega']