from django.urls import path
from . import views

app_name = 'asistencia'  # Esto nos ayuda a organizar las URLs

urlpatterns = [
    # URLs de la API
    path('api/usuario/estado/', views.UserStatusAPIView.as_view(), name='api_user_status'),
    path('api/usuarios/', views.UserListAPIView.as_view(), name='api_user_list'),
    path('api/historial/', views.AsistenciaAPIView.as_view(), name='api_historial'),

    # URL para la página que muestra los botones de entrada/salida
    path('registrar/', views.registrar_asistencia, name='registrar_asistencia'),
    
    # URL para la página que muestra la tabla con el historial
    path('ver-historial/', views.historial_asistencias, name='historial_asistencias'),
    path('exportar/', views.exportar_asistencias_excel, name='exportar_asistencias_excel'),
]