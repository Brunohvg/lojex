from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:id>/', views.edita_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', views.elimina_usuario, name='eliminar_usuario'),
    path('detalhes/<int:id>/', views.detalle_usuario, name='detalhes_usuario'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('recuperar-senha/', views.recupera_senha, name='recuperar_senha'),
]
