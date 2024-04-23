from django.db.models import Q 
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from appevaluacion.forms import EvaluacionForm, DetalleEvaluacionForm
from appevaluacion.models import Evaluacion, DetalleEvaluacion, Unidad, Postulante, Evaluador
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from xhtml2pdf import pisa

@login_required(login_url='login')
@login_required(login_url='login')
def listar_evaluaciones(request):
    # Inicializar la variable evaluador como None
    evaluador = None
    
    # Verificar si el usuario es administrador
    if request.user.is_superuser:
        # Si el usuario es administrador, obtener todas las evaluaciones sin filtrar por evaluador
        datos = Evaluacion.objects.all()
    else:
        try:
            # Obtener el evaluador asociado al usuario
            evaluador = request.user.evaluador
            # Filtrar las evaluaciones por el evaluador
            datos = Evaluacion.objects.filter(evaluador=evaluador)
        except ObjectDoesNotExist:
            # Si el usuario no tiene un evaluador asociado, puedes manejar este caso como prefieras
            # Por ejemplo, puedes redirigir a una página de error o mostrar un mensaje en la plantilla
            return render(request, 'home.html')

    unidades = Unidad.objects.all()

    # Aplicar filtro de estado de evaluación si se proporciona
    estado_evaluacion = request.GET.get('estado_evaluacion', '')
    if estado_evaluacion:
        if estado_evaluacion == 'evaluado':
            datos = datos.filter(estado_evaluacion=True)
        elif estado_evaluacion == 'no_evaluado':
            datos = datos.filter(estado_evaluacion=False)

    # Aplicar filtro de búsqueda si se proporciona
    queryset = request.GET.get('buscar', '')
    if queryset:
        datos = datos.filter(Q(codigo_evaluacion__icontains=queryset)).distinct().order_by('idEvaluacion')

    # Ordenar las evaluaciones por ID
    datos = datos.order_by('idEvaluacion')

    # Paginar los resultados
    paginator = Paginator(datos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con los datos y el estado actual
    return render(request, 'evaluacion/listar.html', {'page_obj': page_obj, 'estado_actual': estado_evaluacion, 'unidades': unidades})


@login_required(login_url='login')
def crear_evaluacion(request):
    unidades = Unidad.objects.all()
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
           # unidad_id = form.cleaned_data.get('idUnidad')
           # if unidad_id:
                form.save()
                messages.success(request, "Evaluación asignada.")
                return redirect('listar_evaluacion')
            #else:
              #  messages.error(request, "Debes seleccionar una unidad.")
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija los errores e inténtelo de nuevo.")
    else:
        form = EvaluacionForm()        
    return render(request, 'evaluacion/agregar.html', {'form': form, 'unidades':unidades})

@login_required(login_url='login')
def filtrar_postulantes_evaluadores(request):
    unidad_id = request.GET.get('unidad_id')
    postulantes_asignados = Evaluacion.objects.values_list('postulante', flat=True)
   
    # Filtrar postulantes y evaluadores por unidad seleccionada    
    postulantes=Postulante.objects.filter(unidad_id=unidad_id).exclude(idPostulante__in=postulantes_asignados)
    evaluadores = Evaluador.objects.filter(unidad_id=unidad_id)
    
    # Convertir los objetos a opciones de select
    postulantes_options = [{'value': p.idPostulante, 'label': f'{p.nombres} {p.ap_paterno} {p.ap_materno}'} for p in postulantes]
    evaluadores_options = [{'value': e.idEvaluador, 'label': f'{e.nombres} {e.apellidos}'} for e in evaluadores]
    
    data = {
        'postulantes': postulantes_options,
        'evaluadores': evaluadores_options
    }
    return JsonResponse(data)

@login_required(login_url='login')
def actualizar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
           form.save()
           messages.success(request, "Evaluación actualizada.")
           return redirect('listar_evaluacion', pk=pk)
    else:
        form = EvaluacionForm(instance=evaluacion)
    return render(request, 'evaluacion/editar.html', {'form': form})

@login_required(login_url='login')
def eliminar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, idEvaluacion=pk)    
    evaluacion.delete()
    messages.success(request, "Evaluación eliminada.")
    return redirect('listar_evaluacion')     

@login_required(login_url='login')
def evaluar_curriculum(request, pk):
    # Obtener la instancia de la evaluación correspondiente
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    # Obtener la instancia de Postulante asociada a la evaluación
    postulante = evaluacion.postulante    
    # Crear un diccionario con los datos del postulante
    postulante_data = {
        'ap_paterno': postulante.ap_paterno,
        'ap_materno': postulante.ap_materno,
        'nombres': postulante.nombres,
        'dni' : postulante.dni,
        'telefono' : postulante.celular,        
        'email' : postulante.email,
        'pdf_curriculum' : postulante.pdf_curriculum,
        'modalidad' : postulante.modalidad,
        'maestria' : postulante.maestria,
        'doctorado' : postulante.doctorado,
        'unidad' : postulante.unidad,
    }

    if request.method == 'POST':
        # Si la solicitud es POST, crea el formulario con los datos enviados
        form = DetalleEvaluacionForm(request.POST)
        #status_eva = evaluacion.estado_evaluacion
        if form.is_valid():          
            # Si el formulario es válido, guarda los datos en la base de datos
            detalle_evaluacion = form.save(commit=False)
            detalle_evaluacion.evaluacion = evaluacion
            evaluacion.estado_evaluacion = True
            detalle_evaluacion.save()
            evaluacion.save()
            # Redirige a alguna página de éxito o muestra un mensaje de éxito
            messages.success(request, "Evaluación completada")
            return redirect('listar_evaluacion')  # Reemplaza 'pagina_de_exito' con la URL adecuada
    else:
        # Si la solicitud no es POST, crea un nuevo formulario vacío
        form = DetalleEvaluacionForm(initial={'evaluacion': evaluacion})
        print('form no valido')
    # Renderiza el formulario en la plantilla
    return render(request, "evaluacion/detalle_evaluar.html", {'form': form, 'evaluacion': evaluacion, 'postulante': postulante_data})

@login_required(login_url='login')
def reporte_postulacion_pdf(request, pk):
   
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    
    postulante = evaluacion.postulante   
    detalles_evaluacion = DetalleEvaluacion.objects.filter(evaluacion=evaluacion)
    resultados_detalle = [] 

    for detalle in detalles_evaluacion:
        resultado = {
            'puntaje_promedioP': detalle.puntaje_promedioP,
            'puntaje_cursosEva': detalle.puntaje_cursosEva,
            'puntaje_partCientifica': detalle.puntaje_partCientifica,
            'puntaje_docenciaUni': detalle.puntaje_docenciaUni,
            'puntaje_idiomaExt': detalle.puntaje_idiomaExt,
            'puntaje_capacitacion': detalle.puntaje_capacitacion,
            'puntaje_libroInscritos': detalle.puntaje_libroInscritos,
            'puntaje_publicaciones': detalle.puntaje_publicaciones,         
            'puntaje_produccionCien': detalle.puntaje_produccionCien,
            'puntajeFinal': detalle.puntajeFinal,
        }       
        
    resultados_postulante = {
        'ap_paterno': postulante.ap_paterno,
        'ap_materno': postulante.ap_materno,
        'nombres': postulante.nombres,
        'dni' : postulante.dni,
        'telefono' : postulante.celular,            
        'email' : postulante.email,
        'pdf_curriculum' : postulante.pdf_curriculum,
        'modalidad' : postulante.modalidad,
        'maestria' : postulante.maestria,
        'doctorado' : postulante.doctorado,
        'unidad' : postulante.unidad,
        
    }
   
    if postulante.maestria is not None:
        mencion= str(postulante.maestria)
    else:
        mencion = str(postulante.doctorado)

    # Renderizar la plantilla HTML con los datos del postulante y los resultados de evaluación
    html_string = render_to_string('evaluacion/reportes/pdf_evaluacion.html', {'evaluacion': evaluacion, 'resultados_postulante': resultados_postulante, 'resultados_detalle' :resultado, 'mencion':mencion})
    
    # Crear una respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    nombre_archivo = f'{postulante.ap_paterno}{postulante.ap_materno}_{postulante.dni}'
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}.pdf"'

    try:
        pisa_status = pisa.CreatePDF(
            html_string,
            dest=response,
            
        )
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)
    except Exception as e:
        return HttpResponse('Error al generar el PDF: %s' % str(e))

    return response

