from rest_framework import permissions

class EsAdministradorOEmpleadoRol(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and hasattr(user, 'rol') and user.rol and user.rol.nombre in ['Administrador', 'Empleado']
        )