from django.urls import path
from . import views    

app_name = 'dashboard'

urlpatterns = [
    # Rota para o painel administrativo do Django
    path('', views.dashboard, name='index'),   
]