from django.urls import path
from appevaluacion.views import postulante

urlpatterns = [
    path('', postulante.listar_postulantes,name="listar_postulantes"),
    path('create/',postulante.crear_postulante ,name="crear_postulante"),
    path('edit/<int:pk>/',postulante.actualizar_postulante ,name="actualizar_postulante"),
   
]