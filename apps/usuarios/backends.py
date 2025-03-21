from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailBackend(ModelBackend):
    """
    Autentica um usuário pelo e-mail e senha.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(email=username)  # Usa email no lugar de username
        except Usuario.DoesNotExist:
            return None
        
        if usuario.check_password(password):  # Valida a senha
            return usuario
        return None

    def get_user(self, user_id):
        """
        Busca o usuário pelo ID.
        """
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
