from rest_framework import serializers
from .models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'rol']

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name']