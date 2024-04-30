"""
URL configuration for proypostgrado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from appseguridad.views.views import home, acceder, salir

from appevaluacion.views import evaluacion,evaluador
from appseguridad.views import usuario

urlpatterns = [
    #Borrar
    path('admin/', admin.site.urls),
    
    path('', acceder, name='login'),
    path('home/', home, name='home'),
    path('logout/',salir ,name="logout"),

    # Usuarios
    path('usuarios/',include('appseguridad.routes.usuario'),name="usuarios"),
    path('update-status-user/',usuario.update_user_status,name="update-status-user"),


    # Evaluaciones
    path('evaluacion/',include('appevaluacion.routes.evaluacion'),name="evaluacion"),
    path('filtrar/', evaluacion.filtrar_postulantes_evaluadores, name='filtrar_postulantes_evaluadores'),
    
    # Postulantes
    path('postulante/',include('appevaluacion.routes.postulante'),name="postulante"),

   # Evaluadores
    path('evaluador/',include('appevaluacion.routes.evaluador'),name="evaluador"),
    path('create-user/',evaluador.crear_usuario ,name="crear_usuario"), 
    path('update-user/', evaluador.obtener_usuarios, name='obtener_usuarios'),

    path('docs/', include_docs_urls(title='Api Documentation')),   
]
