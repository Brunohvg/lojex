from django.contrib import admin
from apps.usuarios.models import Usuario, UsuarioLoja

"""@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('nome', 'email')
"""
# Ou, se preferir, apenas:
admin.site.register(Usuario)
admin.site.register(UsuarioLoja)