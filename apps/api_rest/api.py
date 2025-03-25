# apps/api_rest/api.py
from ninja import NinjaAPI
from apps.usuarios.routers import router as usuarios_router

api = NinjaAPI(title="Sistema API", version="1.0.0")

# Adicione os routers com prefixos
api.add_router("/usuarios/", usuarios_router)
