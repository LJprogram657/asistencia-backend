from django.urls import path
from .views import RegistroUsuarioAPIView, LoginUsuarioAPIView, ListRolesAPIView

urlpatterns = [
    path('register/', RegistroUsuarioAPIView.as_view(), name='registro-usuario'),
    path('login/', LoginUsuarioAPIView.as_view(), name='login-usuario'),
    path('roles/', ListRolesAPIView.as_view(), name='listar-roles'),
]