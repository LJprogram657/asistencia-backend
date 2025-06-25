from rest_framework import serializers
from .models import Usuario, Rol
from django.contrib.auth.hashers import make_password

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol = serializers.SlugRelatedField(
        queryset=Rol.objects.all(),
        slug_field='nombre'
    )

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'rol']

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.password = make_password(password)
        usuario.save()
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name']