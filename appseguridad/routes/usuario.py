from django.urls import path
from appseguridad.views import usuario

urlpatterns = [
    path('', usuario.listar_usuarios,name="listar_usuarios"),
    path('listar_usuarios_json', usuario.listar_usuarios_json,name="listar_usuarios_json"),     
    path('create/',usuario.creacion_usuario ,name="creacion_usuario"),
    path('edit/<int:id>/',usuario.actualizar_usuario ,name="actualizar_usuario"),
    path('delete/<int:id>/',usuario.eliminar_usuario ,name="eliminar_usuario"),
    path('edit-perfil/',usuario.editar_perfil ,name="editar_perfil"),   
]