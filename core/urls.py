from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.api import routers  # As rotas da API são importadas aqui.

urlpatterns = [
    # Rota para o painel administrativo do Django
    path('admin/', admin.site.urls),
    
    # Rota principal que direciona para as URLs do app 'usuarios'
    path('', include('apps.usuarios.urls')),  # Aqui você inclui as rotas do app 'usuarios'

    # Inclui as rotas da API Ninja
    #path('api/', include('apps.api.urls')),  # As rotas da API Ninja devem ser incluídas desta forma
]

# Se estiver no modo DEBUG, adiciona as rotas para os arquivos estáticos e de mídia
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
