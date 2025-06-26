from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asistencia
import datetime
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import openpyxl
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Asistencia
from .serializers import AsistenciaSerializer
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class UserStatusAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'is_staff': request.user.is_staff})

@method_decorator(csrf_exempt, name='dispatch')
class UserListAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class AsistenciaAPIView(generics.ListAPIView):
    serializer_class = AsistenciaSerializer
    authentication_classes = [SessionAuthentication]
    # Cambiamos el permiso para que solo los administradores (staff) puedan acceder.
    # Esta es la forma más limpia y segura de restringir el acceso.
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """
        Este método ahora solo se ejecutará si el usuario es un administrador,
        gracias a la validación de 'permission_classes'.
        La lógica de filtrado se mantiene intacta para los administradores.
        """
        queryset = Asistencia.objects.select_related('usuario').all()
        user_id = self.request.query_params.get('user_id') or self.request.query_params.get('usuario')
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')

        if user_id:
            queryset = queryset.filter(usuario__id=user_id)
        if fecha_inicio:
            queryset = queryset.filter(fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_hora__date__lte=fecha_fin)

        return queryset.order_by('-fecha_hora')


@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        # Validamos que el tipo sea uno de los permitidos
        if tipo in ['E', 'S', 'SD', 'VD']:
            today = datetime.date.today()
            # La validación de asistencia existente puede ser más compleja ahora.
            # Por ahora, mantenemos la validación simple para Entrada y Salida.
            asistencia_existente = Asistencia.objects.filter(
                usuario=request.user, 
                fecha_hora__date=today, 
                tipo=tipo
            ).exists()

            if tipo in ['E', 'S'] and asistencia_existente:
                messages.warning(request, f'Ya ha registrado su {Asistencia.TIPO_ASISTENCIA_DICT[tipo]} el día de hoy.')
            else:
                Asistencia.objects.create(
                    usuario=request.user, 
                    tipo=tipo,
                    latitud=latitud if latitud else None,
                    longitud=longitud if longitud else None
                )
                messages.success(request, f'Se ha registrado su {Asistencia.TIPO_ASISTENCIA_DICT[tipo]} correctamente.')
        else:
            messages.error(request, 'Tipo de asistencia no válido.')
        
        return redirect('asistencia:historial_asistencias')

    return render(request, 'asistencia/registrar.html')

@login_required
def historial_asistencias(request):
    # Esta vista ahora solo renderiza el template. Los datos se cargan por API.
    return render(request, 'asistencia/historial.html', {'is_staff': request.user.is_staff})


@login_required
def exportar_asistencias_excel(request):
    # Solo los administradores pueden exportar
    if not request.user.is_staff:
        return redirect('asistencia:historial_asistencias')

    # Reutilizamos la misma lógica de filtrado que en la API
    usuario_id = request.GET.get('user_id', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    queryset = Asistencia.objects.select_related('usuario').all()

    if usuario_id:
        queryset = queryset.filter(usuario__id=usuario_id)

    if fecha_inicio:
        queryset = queryset.filter(fecha_hora__date__gte=fecha_inicio)
    
    if fecha_fin:
        queryset = queryset.filter(fecha_hora__date__lte=fecha_fin)

    # Crear el libro de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial de Asistencias"

    # Añadir cabeceras
    ws.append(['Usuario', 'Nombre Completo', 'Fecha y Hora', 'Tipo', 'Latitud', 'Longitud', 'URL Mapa'])

    # Añadir datos
    for asistencia in queryset.order_by('usuario__username', 'fecha_hora'):
        ws.append([
            asistencia.usuario.username,
            asistencia.usuario.get_full_name(),
            asistencia.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            asistencia.get_tipo_display(),
            asistencia.latitud,
            asistencia.longitud,
            asistencia.mapa_url
        ])

    # Crear la respuesta HTTP con el archivo de Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=historial_asistencias.xlsx'
    wb.save(response)

    return response


class AsistenciaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
