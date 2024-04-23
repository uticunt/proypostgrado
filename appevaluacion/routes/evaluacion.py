
from django.urls import path
from appevaluacion.views import evaluacion

urlpatterns = [
    path('', evaluacion.listar_evaluaciones,name="listar_evaluacion"),
    path('create/',evaluacion.crear_evaluacion ,name="crear_evaluacion"),
   

    #path('edit/<int:pk>/',evaluacion.actualizar_evaluacion ,name="editar_evaluacion"),
    path('delete/<int:pk>/',evaluacion.eliminar_evaluacion,name="eliminar_evaluacion"), 
    path('evaluar/<int:pk>/',evaluacion.evaluar_curriculum ,name="evaluar_curriculum"),
    path('reporte_pdf/<int:pk>/', evaluacion.reporte_postulacion_pdf, name='reporte_postulacion_pdf'),
]