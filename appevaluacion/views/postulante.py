from django.db.models import Q 
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from appevaluacion.forms import *
from appevaluacion.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from xhtml2pdf import pisa

@login_required(login_url='login')
def listar_postulantes(request):   
    queryset = request.GET.get("buscar")
    unidad_filtro = request.GET.get("unidad", "")
    modalidad_filtro = request.GET.get("modalidad", "")
    datos = Postulante.objects.all()

    if queryset:
        datos = datos.filter(Q(codigo__icontains=queryset)).distinct()            
    if unidad_filtro and unidad_filtro != "Todos":
        datos = datos.filter(unidad__idUnidad__icontains=unidad_filtro)   
    if modalidad_filtro and modalidad_filtro != "Todos":
        datos = datos.filter(modalidad__idModalidad__icontains=modalidad_filtro)

    conteo = datos.count()
    datos = datos.order_by('idPostulante')    
    paginator = Paginator(datos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    modalidades = Modalidad.objects.all()
    unidades = Unidad.objects.all()

    return render(request, 'postulante/listar.html', {'page_obj': page_obj, 'modalidades': modalidades, 'unidades': unidades, 'conteo': conteo})

@login_required(login_url='login')
def crear_postulante(request):    
    if request.method == 'POST':
        form = PostulanteForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Postulante añadido.")
                return redirect('listar_postulantes')        
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija los errores e inténtelo de nuevo.")
    else:
        form = PostulanteForm()        
    return render(request, 'postulante/agregar.html', {'form': form})

@login_required(login_url='login')
def actualizar_postulante(request, pk):
    postulante = get_object_or_404(Postulante, pk=pk)
    is_doctorado = postulante.doctorado 
    if request.method == 'POST':
        form = PostulanteForm(request.POST, instance=postulante)
        if form.is_valid():
           form.save()
           messages.success(request, "Postulante actualizado.")
           return redirect('listar_postulantes')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija los errores e inténtelo de nuevo.")
    else:
        form = PostulanteForm(instance=postulante)
    return render(request, 'postulante/editar.html', {'form': form,'is_doctorado': form})