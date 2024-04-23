
from django.urls import path
from appevaluacion.views import evaluador

urlpatterns = [
    path('', evaluador.listar_evaluadores,name="listar_evaluadores"),
    path('create/',evaluador.crear_evaluador ,name="crear_evaluador"),
   
   

   
]