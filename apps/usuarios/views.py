import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .forms import RegistroUsuarioForm, LoginForm, EsqueciSenhaForm, NovaSenhaForm
from .models import Usuario

# Configuração do logger específico para o app 'usuarios'
logger = logging.getLogger(None)


def login_user(request):
    """
    Realiza a autenticação do usuário.
    
    Se o método for POST, valida os dados do formulário de login.
    Caso as credenciais estejam corretas, efetua o login e redireciona
    para a página inicial; caso contrário, adiciona erros ao formulário.
    Em requisições GET, exibe o formulário de login.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            usuario = authenticate(request, username=email, password=senha)
            if usuario is not None:
                login(request, usuario)
                logger.info(f"Usuário {email} logado com sucesso.")
                return redirect("dashboard:index")  # Inclua o namespace antes do nome da view
            else:
                logger.warning(f"Tentativa de login falha para {email}. Credenciais incorretas.")
                form.add_error("email", "Email ou senha incorretos.")
                form.add_error("senha", "")
    else:
        form = LoginForm()
    
    return render(request, "usuarios/base.html", {"form": form})


def registrar_usuario(request):
    """
    Registra um novo usuário.
    
    Em requisições POST, valida os dados enviados pelo formulário e,
    se estiverem corretos, salva o novo usuário e redireciona para a página
    de login. Em caso de dados inválidos, exibe o formulário com os erros.
    Para requisições GET, apenas exibe o formulário de registro.
    """
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            logger.info(f"Novo usuário registrado: {usuario.email}")
            return redirect('usuarios:login')  # Redireciona para a página de login após o registro
        else:
            logger.warning("Falha ao registrar usuário. Dados inválidos.")
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/base.html', {'form': form})


def lista_usuarios(request):
    """
    Exibe uma lista de todos os usuários cadastrados.
    """
    usuarios = Usuario.objects.all()
    logger.info("Lista de usuários acessada.")
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def edita_usuario(request, id):
    """
    Exibe a página de edição de um usuário específico.
    
    Busca o usuário pelo ID e, se encontrado, renderiza o template
    de edição com os dados do usuário.
    """
    usuario = get_object_or_404(Usuario, pk=id)
    logger.info(f"Usuário {usuario.email} acessou a página de edição.")
    return render(request, 'usuarios/edita_usuario.html', {'usuario': usuario})


def elimina_usuario(request, id):
    """
    Remove um usuário do sistema.
    
    Se a requisição for POST, deleta o usuário e redireciona para a lista de usuários.
    Caso contrário, renderiza um template de confirmação para exclusão.
    """
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        usuario.delete()
        logger.info(f"Usuário {usuario.email} foi excluído.")
        return redirect('usuarios:lista_usuarios')
    
    return render(request, 'usuarios/elimina_usuario.html', {'usuario': usuario})


def detalle_usuario(request, id):
    """
    Exibe os detalhes de um usuário específico.
    
    Busca o usuário pelo ID e renderiza o template com as informações detalhadas.
    """
    usuario = get_object_or_404(Usuario, pk=id)
    logger.info(f"Detalhes do usuário {usuario.email} acessados.")
    return render(request, 'usuarios/detalhe_usuario.html', {'usuario': usuario})


def logout_user(request):
    """
    Efetua o logout do usuário autenticado.
    
    Após deslogar, redireciona para a página de login.
    """
    logger.info(f"Usuário {request.user.email} fez logout.")
    logout(request)
    return redirect('usuarios:login')


def recupera_senha(request):
    """
    Inicia o processo de recuperação de senha.
    
    Em requisições POST, valida o formulário de recuperação de senha.
    Se o email informado corresponder a um usuário cadastrado, gera um token e
    envia um email com as instruções para redefinir a senha. Caso o email não esteja
    registrado, adiciona um erro no formulário.
    Em requisições GET, exibe o formulário de recuperação de senha.
    """
    if request.method == 'POST':
        form = EsqueciSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(email=email)
                token = default_token_generator.make_token(usuario)
                uid = usuario.pk
                reset_url = f"http://{get_current_site(request).domain}/resetar-senha/{uid}/{token}/"
                
                # Renderiza o template HTML do email com o link para redefinir a senha
                html_message = render_to_string('usuarios/redefinir_senha_email.html', {
                    'reset_url': reset_url,
                    'client_name': usuario.nome,  # Exibe o nome do usuário, se disponível
                    'year': 2025
                })
                
                # Configura e envia o email com conteúdo HTML
                email_message = EmailMessage(
                    'Redefinição de Senha',
                    html_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                email_message.content_subtype = "html"  # Define o conteúdo como HTML
                email_message.send(fail_silently=False)
                
                logger.info(f"E-mail de recuperação de senha enviado para {email}.")
                return redirect('usuarios:login')
            
            except Usuario.DoesNotExist:
                logger.warning(f"Tentativa de recuperação de senha para e-mail não registrado: {email}.")
                form.add_error('email', 'Este email não está registrado.')
    else:
        form = EsqueciSenhaForm()
    
    return render(request, 'usuarios/base.html', {'form': form})


def redefinir_senha(request, uidb64, token):
    """
    Permite a redefinição da senha do usuário através de um link enviado por email.
    
    Verifica se o token é válido e, em caso positivo, permite que o usuário
    informe uma nova senha. Em caso de token inválido ou usuário inexistente,
    redireciona para a página de login.
    """
    try:
        usuario = Usuario.objects.get(pk=uidb64)  # Se necessário, decodifique uidb64
    except Usuario.DoesNotExist:
        logger.warning("Usuário não encontrado para redefinição de senha.")
        return redirect('usuarios:login')
    
    # Verifica se o token é válido para o usuário
    if not default_token_generator.check_token(usuario, token):
        logger.warning(f"Token inválido para o usuário {usuario.email}.")
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        form = NovaSenhaForm(request.POST)
        if form.is_valid():
            nova_senha = form.cleaned_data['nova_senha']
            usuario.set_password(nova_senha)
            usuario.save()
            logger.info(f"Senha redefinida com sucesso para o usuário {usuario.email}.")
            return redirect('usuarios:login')
    else:
        form = NovaSenhaForm()
    
    return render(request, 'usuarios/base.html', {'form': form})


def config_conta(request):
    user = request.user
    print(user)
    return render(request, 'dashboard/base.html')