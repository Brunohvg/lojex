from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, LoginForm, EsqueciSenhaForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            usuario = authenticate(request, username=email, password=senha)

            if usuario is not None:
                login(request, usuario)
                return redirect("pagina_inicial")  # Altere para a página correta
            else:
                form.add_error("email", "Email ou senha incorretos.")
                form.add_error("senha", "")

    else:
        form = LoginForm()

    return render(request, "usuarios/base.html", {"form": form})

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios:login')  # Redireciona após o registro
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/base.html', {'form': form})

def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtém todos os usuários
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

def edita_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)  # Obtém o usuário ou retorna 404
    # Aqui você pode adicionar lógica para editar o usuário
    return render(request, 'usuarios/edita_usuario.html', {'usuario': usuario})

def elimina_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)  # Obtém o usuário ou retorna 404
    if request.method == 'POST':
        usuario.delete()  # Exclui o usuário
        return redirect('usuarios:lista_usuarios')  # Redireciona após a exclusão
    return render(request, 'usuarios/elimina_usuario.html', {'usuario': usuario})

def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)  # Obtém o usuário ou retorna 404
    return render(request, 'usuarios/detalhe_usuario.html', {'usuario': usuario})

def logout_user(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('usuarios:login')  # Redireciona para a página de login

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
                return redirect('usuarios:login')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Este email não está registrado.')

    else:
        form = EsqueciSenhaForm()

    return render(request, 'usuarios/base.html', {'form': form})
