'''from django.contrib.auth.models import User
from django.db import models

class Permiso(models.Model):
    nombre = models.CharField(max_length=100)

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permiso)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)


def configurar_roles_y_permisos():
    # Verificar si los permisos y roles ya existen
    if Permiso.objects.exists() or Rol.objects.exists():
        return  # No es necesario configurar nuevamente

    # Crear permisos
    permiso_lectura = Permiso.objects.create(nombre='Lectura')
    permiso_escritura = Permiso.objects.create(nombre='Escritura')

    # Crear roles
    rol_administrador = Rol.objects.create(nombre='Administrador')
    rol_administrador.permisos.add(permiso_lectura, permiso_escritura)

    rol_evaluador = Rol.objects.create(nombre='Evaluador')
    rol_evaluador.permisos.add(permiso_lectura)

# Llamar a la función de configuración al iniciar la aplicación
configurar_roles_y_permisos()

'''