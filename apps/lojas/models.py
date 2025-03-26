# apps/lojas/models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_cnpj(value):
    """ Valida um CNPJ no formato XX.XXX.XXX/XXXX-XX ou sem formatação. """
    cnpj = re.sub(r'\D', '', value)  # Remove tudo que não for número
    
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        raise ValidationError('CNPJ inválido')

    def calcula_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    # Cálculo dos dígitos verificadores
    if calcula_digito(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) != cnpj[12] or \
       calcula_digito(cnpj[:13], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) != cnpj[13]:
        raise ValidationError('CNPJ inválido')

def validate_telefone(value):
    """ Valida um telefone no formato nacional com ou sem DDD. """
    if not value.isdigit():
        raise ValidationError('Telefone deve conter apenas números')
    if len(value) not in [10, 11]:  # 10 dígitos (fixo) ou 11 (celular)
        raise ValidationError('Telefone deve conter entre 10 e 11 dígitos')

class Loja(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    endereco = models.TextField()
    telefone = models.CharField(max_length=11, validators=[validate_telefone])
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['nome']