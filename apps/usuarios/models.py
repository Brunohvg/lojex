# usuarios/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.lojas.models import Loja

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nome=nome, **extra_fields)
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nome, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, nome, senha, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):  # Agora herda de PermissionsMixin
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self):
        return self.nome

    # O método has_module_perms já é herdado de PermissionsMixin, então não é necessário implementar.
    # Caso precise de um comportamento customizado, adicione-o aqui.

    # O método has_perm também pode ser herdado de PermissionsMixin.
    # Caso queira customizar, adicione um comportamento semelhante ao de 'has_module_perms'.

class UsuarioLoja(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='lojas_associadas')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='usuarios_associados')
    cargo = models.CharField(max_length=50)  # Ex.: Gerente, Motoboy, etc.

    class Meta:
        unique_together = ('usuario', 'loja')

    def __str__(self):
        return f"{self.usuario.nome} - {self.loja.nome} ({self.cargo})"
