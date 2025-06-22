from django.db import models
from django.conf import settings

class Asistencia(models.Model):
    TIPO_ASISTENCIA = [
        ('E', 'Entrada'),
        ('SD', 'Salida a Descanso'),
        ('VD', 'Volver de Descanso'),
        ('S', 'Salida'),
    ]
    TIPO_ASISTENCIA_DICT = dict(TIPO_ASISTENCIA)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=2, choices=TIPO_ASISTENCIA)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    mapa_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.get_tipo_display()} - {self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")}'

    def save(self, *args, **kwargs):
        if self.latitud and self.longitud and not self.mapa_url:
            # Generamos un enlace a Google Maps con las coordenadas
            self.mapa_url = f"https://www.google.com/maps?q={self.latitud},{self.longitud}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

# Create your models here.
