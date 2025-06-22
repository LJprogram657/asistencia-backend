from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Añadimos el campo 'rol' al list_display para que se vea en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'rol')
    # Añadimos el campo 'rol' a los fieldsets para poder editarlo en el formulario de usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('rol',)}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Rol)
