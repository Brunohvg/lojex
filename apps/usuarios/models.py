from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    """
    Gerenciador customizado para o modelo Usuario.
    
    Contém métodos para criação de usuários e superusuários, garantindo que
    o email seja normalizado e que a senha seja devidamente criptografada.
    """
    
    def create_user(self, email, nome, senha=None, **extra_fields):
        """
        Cria e salva um usuário com o email e nome fornecidos.
        
        :param email: Email do usuário (obrigatório).
        :param nome: Nome do usuário.
        :param senha: Senha do usuário.
        :param extra_fields: Campos adicionais para o modelo.
        :raises ValueError: Se o email não for fornecido.
        :return: Instância do usuário criado.
        """
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nome=nome, **extra_fields)
        usuario.set_password(senha)  # Criptografa a senha
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nome, senha=None, **extra_fields):
        """
        Cria e salva um superusuário com privilégios administrativos.
        
        Define os campos obrigatórios para um superusuário: is_staff, is_superuser e is_active.
        
        :param email: Email do superusuário.
        :param nome: Nome do superusuário.
        :param senha: Senha do superusuário.
        :param extra_fields: Campos adicionais para o modelo.
        :return: Instância do superusuário criado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Garante que o superusuário está ativo
        return self.create_user(email, nome, senha, **extra_fields)


class Usuario(AbstractBaseUser):
    """
    Modelo de usuário customizado.
    
    Utiliza o email como identificador único (USERNAME_FIELD) e
    inclui informações básicas como nome e datas de criação e atualização.
    """
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Define o campo usado para autenticação e os campos obrigatórios adicionais
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    # Define o gerenciador customizado para o modelo
    objects = UsuarioManager()

    def __str__(self):
        """
        Retorna uma representação legível do objeto.
        """
        return self.nome
