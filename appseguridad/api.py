'''from appevaluacion.models import *
from rest_framework import viewsets
from appseguridad.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import login
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''

from rest_framework.decorators import api_view
from rest_framework.response import Response
from appseguridad.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


'''@api_view(['POST'])
def login(request):
    print(request.data)

    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data(['password'])):
        return Response({"error":"Contraseña invalida"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token":token.key, "user": serializer.data},status=status.HTTP_200_OK)'''

@api_view(['POST'])
@csrf_exempt
def login(request):
    # Obtener datos de la solicitud
    username = request.data.get('username')
    password = request.data.get('password')

    # Verificar si se proporcionan nombre de usuario y contraseña
    if not username or not password:
        return Response({"error": "Se requiere nombre de usuario y contraseña"}, status=status.HTTP_400_BAD_REQUEST)

    # Buscar al usuario por nombre de usuario
    user = get_object_or_404(User, username=username)

    # Verificar la contraseña
    if not user.check_password(password):
        return Response({"error": "Contraseña inválida"}, status=status.HTTP_400_BAD_REQUEST)

    # Generar o recuperar el token de autenticación
    token, created = Token.objects.get_or_create(user=user)

    # Serializar los datos del usuario
    serializer = UserSerializer(user)

    # Devolver el token y los datos del usuario
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)