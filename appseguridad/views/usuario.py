from django.db.models import Q 
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from appevaluacion.forms import *
from appevaluacion.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import is_password_usable
from django.conf import settings
from appseguridad.forms import UserForm

@login_required(login_url='login')
def listar_usuarios(request):   
    queryset = request.GET.get("buscar")
    datos = User.objects.all()    
    # Conteo
    conteo = datos.count()   

    datos = datos.order_by('id')    
    paginator = Paginator(datos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    

    return render(request, 'usuario/listar.html', {'page_obj': page_obj, 'conteo': conteo})


@login_required(login_url='login')
def creacion_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Si necesitas hacer algo más con el usuario antes de guardarlo, puedes hacerlo aquí
            user.save()
            return redirect('listar_usuarios')  # Redirige a la página del perfil del usuario, cambia esto según tu aplicación
    else:
        form = UserForm()
    return render(request, 'usuario/agregar.html', {'form': form})

