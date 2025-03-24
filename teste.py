import os
import django

# Defina o módulo de configurações
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def enviar_email(assunto, corpo, destinatarios):
    try:
        send_mail(
            assunto,
            corpo,
            settings.DEFAULT_FROM_EMAIL,
            destinatarios,
            fail_silently=False,
        )
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

# Exemplo de uso
enviar_email(
    'Assunto do Email',
    'Aqui está o corpo do email.',
    ['destinatario@example.com']
)
