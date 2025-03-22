import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, LoginForm, EsqueciSenhaForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings

# Configuração do logger
logger = logging.getLogger('usuarios')

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            usuario = authenticate(request, username=email, password=senha)

            if usuario is not None:
                login(request, usuario)
                logger.info(f"Usuário {email} logado com sucesso.")
                return redirect("pagina_inicial")  # Altere para a página correta
            else:
                logger.warning(f"Tentativa de login falha para {email}. Credenciais incorretas.")
                form.add_error("email", "Email ou senha incorretos.")
                form.add_error("senha", "")

    else:
        form = LoginForm()

    return render(request, "usuarios/base.html", {"form": form})

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            logger.info(f"Novo usuário registrado: {usuario.email}")
            return redirect('usuarios:login')  # Redireciona após o registro
        else:
            logger.warning("Falha ao registrar usuário. Dados inválidos.")

    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/base.html', {'form': form})

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    logger.info("Lista de usuários acessada.")
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

def edita_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    logger.info(f"Usuário {usuario.email} acessou a página de edição.")
    return render(request, 'usuarios/edita_usuario.html', {'usuario': usuario})

def elimina_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        usuario.delete()
        logger.info(f"Usuário {usuario.email} foi excluído.")
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/elimina_usuario.html', {'usuario': usuario})

def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    logger.info(f"Detalhes do usuário {usuario.email} acessados.")
    return render(request, 'usuarios/detalhe_usuario.html', {'usuario': usuario})

def logout_user(request):
    logger.info(f"Usuário {request.user.email} fez logout.")
    logout(request)
    return redirect('usuarios:login')

def recupera_senha(request):
    if request.method == 'POST':
        form = EsqueciSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(email=email)
                token = default_token_generator.make_token(usuario)
                uid = usuario.pk
                reset_url = f"{get_current_site(request).domain}/resetar-senha/{uid}/{token}/"

                send_mail(
                    'Redefinição de Senha',
                    f'Clique no link para redefinir sua senha: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                logger.info(f"E-mail de recuperação de senha enviado para {email}.")
                return redirect('usuarios:login')

            except Usuario.DoesNotExist:
                logger.warning(f"Tentativa de recuperação de senha para e-mail não registrado: {email}.")
                form.add_error('email', 'Este email não está registrado.')

    else:
        form = EsqueciSenhaForm()

    return render(request, 'usuarios/base.html', {'form': form})
