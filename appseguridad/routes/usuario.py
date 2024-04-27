from django.urls import path
from appseguridad.views import usuario

urlpatterns = [
    path('', usuario.listar_usuarios,name="listar_usuarios"), 
   
]