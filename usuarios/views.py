from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

class LoginUsuarioAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            rol_nombre = user.rol.nombre if user.rol else None
            token, created = Token.objects.get_or_create(user=user)
            return Response({'mensaje': 'Login exitoso', 'usuario': username, 'rol': rol_nombre, 'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
from .serializers import RegistroUsuarioSerializer, RolSerializer
from .models import Rol

class ListRolesAPIView(APIView):
    def get(self, request):
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)

class RegistroUsuarioAPIView(APIView):
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
