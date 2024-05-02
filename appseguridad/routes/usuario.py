from django.urls import path
from appseguridad.views import usuario

urlpatterns = [
    path('', usuario.listar_usuarios,name="listar_usuarios"),
    path('listar_usuarios_json', usuario.listar_usuarios_json,name="listar_usuarios_json"), 
    
    path('create/',usuario.creacion_usuario ,name="creacion_usuario"),

    #path('reporte_credenciales/',usuario.descargar_excel_usuarios,name="descargar_excel_usuarios"),
   
]