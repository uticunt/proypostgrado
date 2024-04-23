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
def listar_evaluadores(request):   
    queryset = request.GET.get("buscar")
    unidad_filtro = request.GET.get("unidad", "")    
    datos = Evaluador.objects.all()

    if queryset:
        datos = datos.filter(Q(codigo__icontains=queryset)).distinct()            
    if unidad_filtro and unidad_filtro != "Todos":
        datos = datos.filter(unidad__idUnidad__icontains=unidad_filtro)   
   

    conteo = datos.count()
    datos = datos.order_by('idEvaluador')    
    paginator = Paginator(datos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

   
    unidades = Unidad.objects.all()

    return render(request, 'evaluador/listar.html', {'page_obj': page_obj, 'unidades': unidades, 'conteo': conteo})

@login_required(login_url='login')
def crear_evaluador(request):
    if request.method == 'GET':
        form = EvaluadorForm() 
        return render(request, 'evaluador/agregar.html', {'form': form})
    
    elif request.method == 'POST':
        form = EvaluadorForm(request.POST)
        if form.is_valid():
            evaluador = form.save()
            data = {
                'id': evaluador.idEvaluador,
                'codigo_evaluador': evaluador.codigo_evaluador,
                'nombres': evaluador.nombres,
                'apellidos': evaluador.apellidos,
                'dni': evaluador.dni,
                'email': evaluador.email,
                'activo': evaluador.activo,
                'cargo': evaluador.get_cargo_display(),  # Así se obtiene el valor 'display' de un choice field
            }
            return JsonResponse({'data': data}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": "Solo solicitudes POST"}, status=400)

@login_required(login_url='login')
def crear_usuario(request):
    if request.method == 'POST':
        # Procesar los datos del formulario y crear un nuevo usuario
        username = request.POST.get('username')        
        password = request.POST.get('password')
        # Aquí puedes agregar más campos según sea necesario

        try:
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'mensaje': 'Usuario creado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'evaluador/agregar.html')  # Renderiza el template que contiene el botón y el modal

@login_required(login_url='login')
def obtener_usuarios(request):
    usuarios_disponibles = User.objects.exclude(evaluador__isnull=False).values('id', 'username')  # Filtrar solo los necesarios
    return JsonResponse(list(usuarios_disponibles), safe=False)