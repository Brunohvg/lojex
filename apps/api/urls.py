"""# apps/api/urls.py
from ninja import NinjaAPI
from apps.usuarios.routers import router as usuarios_router

api = NinjaAPI()

# Adiciona os routers específicos de cada app
api.add_router("/usuarios/", usuarios_router)

# Exibe todas as rotas da API
urlpatterns = api.urls
"""