from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('edita_usuario/<int:id>/', views.edita_usuario, name='edita_usuario'),
    path('elimina_usuario/<int:id>/', views.elimina_usuario, name='elimina_usuario'),
    path('detalle_usuario/<int:id>/', views.detalle_usuario, name='detalle_usuario'),
    path('login/', views.login_user, name='login'),
    path('logout_user/<int:id>/', views.logout, name='logout'),
    path('recupera_senha/', views.recupera_senha, name='recupera_senha'),
]

