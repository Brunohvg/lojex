# motoboys/models.py
import re
from django.db import models
from apps.lojas.models import Loja
from django.core.exceptions import ValidationError

def validate_telefone(value):
    """ Valida o telefone para garantir que tenha 11 dígitos. """
    if not re.match(r'^\d{11}$', value):
        raise ValidationError("O número de telefone deve ter 11 dígitos.")

class Motoboy(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="motoboys")
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=11, validators=[validate_telefone])
    email = models.EmailField(unique=True)
    placa_moto = models.CharField(max_length=7, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Motoboy'
        verbose_name_plural = 'Motoboys'
        ordering = ['nome']