from django.contrib import admin
from .models import Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'fecha_hora', 'latitud', 'longitud', 'mapa_url')
    list_filter = ('tipo', 'fecha_hora', 'usuario')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
