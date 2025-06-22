from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    # Puedes añadir más campos personalizados aquí en el futuro
    # por ejemplo: foto_perfil, numero_telefono, etc.

    def __str__(self):
        if self.rol:
            return f'{self.username} - {self.rol.nombre}'
        return self.username