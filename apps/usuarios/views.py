
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, LoginForm, EsqueciSenhaForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

def registrar_usuario(request):
    # Se o método for POST, então o formulário foi submetido
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona após o registro
    else:
        form = RegistroUsuarioForm()

    # Se o método for GET, então o formulário será exibido
    return render(request, 'usuarios/registrar_usuario.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            usuario = authenticate(request, username=email, password=senha)  # Autentica pelo email

            if usuario is not None:
                login(request, usuario)
                return redirect("pagina_inicial")  # Altere para a página correta
            else:
                form.add_error("email", "Email ou senha incorretos.")  # Adiciona erro no campo de email
                form.add_error("senha", "")  # Mantém erro vazio no campo de senha para forçar exibição

    else:
        form = LoginForm()

    return render(request, "usuarios/teste.html", {"form": form})


def lista_usuarios(request):

    return render(request, 'usuarios/lista_usuarios.html')

def edita_usuario(request, id):
    return render(request, 'usuarios/edita_usuario.html')

def elimina_usuario(request, id):
    return render(request, 'usuarios/elimina_usuario.html')

def detalle_usuario(request, id):
    return render(request, 'usuarios/detalle_usuario.html')

def logout_user(request, id):
    return render(request, 'usuarios/login_usuario.html')

def recupera_senha(request):
    if request.method == 'POST':
        form = EsqueciSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Enviar email com link de redefinição de senha
            try:
                usuario = Usuario.objects.get(email=email)  # Usando Usuario em vez de User
                token = default_token_generator.make_token(usuario)
                uid = usuario.pk
                reset_url = f"{get_current_site(request).domain}/resetar-senha/{uid}/{token}/"

                # Enviar o e-mail
                send_mail(
                    'Redefinição de Senha',
                    f'Clique no link para redefinir sua senha: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('login')
            except Usuario.DoesNotExist:  # Usando Usuario em vez de User
                form.add_error('email', 'Este email não está registrado.')

    else:
        form = EsqueciSenhaForm()

    return render(request, 'auth/esqueceu_senha.html', {'form': form})    



