# notificacoes/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.lojas.models import Loja
from apps.motoboys.models import Motoboy

User = get_user_model()  # Obtém o modelo de usuário personalizado

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes')
    motoboy = models.ForeignKey(Motoboy, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes')
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.usuario} - {self.mensagem[:20]}..."

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']