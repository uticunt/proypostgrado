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
from appseguridad.forms import CrearUserForm,EditarUserForm, PerfilrUserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from openpyxl import Workbook
from django.http.response import HttpResponse
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os
import openpyxl
from openpyxl import Workbook

#---------------------------------------------Listar usuarios---------------------------------------------
@login_required(login_url='login')
def listar_usuarios(request):
    return render(request, 'usuario/listar.html')

@login_required(login_url='login')
def listar_usuarios_json(request):    
    filtro_status = request.GET.get('estado')
    if filtro_status == "activo":
        usuarios = list(User.objects.filter(is_active=True).values())
    elif filtro_status == "inactivo":
        usuarios = list(User.objects.filter(is_active=False).values())
    else:
        usuarios = list(User.objects.values())
    data = {'usuarios':usuarios}
    return JsonResponse(data)

# Actualiza estado del Usuario
@csrf_exempt
def update_user_status(request):
    user_id = request.POST.get('user_id')
    is_active = request.POST.get('is_active') == 'true'  
    try:
        user = User.objects.get(id=user_id)
        user.is_active = is_active
        user.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    
#---------------------------------------------------------------------------------------------------------

#------------------------------------------Crer USuario --------------------------------------------------
@login_required(login_url='login')
def creacion_usuario(request):
    if request.method == 'POST':
        form = CrearUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            save_password(username,password)
            form.save()
            messages.success(request, f'Usuario {username} creado exitosamente.')
            return redirect('listar_usuarios')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = CrearUserForm()
    return render(request, 'usuario/agregar.html', {'form': form})

#Guardar en un archivo excel las credenciales
def save_password(username, password):
    # Ruta del archivo Excel
    excel_file = 'C:/wamp64/www/proypostgrado/appseguridad/templates/usuario/credenciales_usuarios.xlsx'
    
    # Si el archivo no existe, crearlo y añadir cabeceras
    if not os.path.exists(excel_file):
        workbook = Workbook()
        sheet = workbook.active
        sheet['A1'] = 'Username'
        sheet['B1'] = 'Password'
        workbook.save(filename=excel_file)
    
    # Abrir el archivo existente y agregar una nueva entrada
    workbook = openpyxl.load_workbook(filename=excel_file)
    sheet = workbook.active
    max_row = sheet.max_row + 1
    sheet.cell(row=max_row, column=1).value = username
    sheet.cell(row=max_row, column=2).value = password
    workbook.save(filename=excel_file)

#Descargar Credenciales en excel
def download_excel(request):   
    # Ruta al archivo Excel en el directorio de medios
    excel_path = 'C:/wamp64/www/proypostgrado/appseguridad/templates/usuario/credenciales_usuarios.xlsx'
    # Respuesta de descarga del archivo Excel
    with open(excel_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=credenciales_usuarios.xlsx'
        return response

#---------------------------------------------------------------------------------------------------------

#------------------------------------------Editar USuario ------------------------------------------------
@login_required(login_url='login')
def actualizar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = EditarUserForm(request.POST, instance=usuario)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request, f'Usuario {username} actualizado exitosamente.')
           return redirect('listar_usuarios')
        else:
           messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EditarUserForm(instance=usuario)
    return render(request, 'usuario/editar.html', {'form': form})

#---------------------------------------------------------------------------------------------------------

#------------------------------------------Eliminar USuario ------------------------------------------------
@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)   
    if request.user.is_superuser:  
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('listar_usuarios') 

#---------------------------------------------------------------------------------------------------------

#------------------------------------------Editar Perfil USuario ------------------------------------------------
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilrUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('home')
    else:
        form = PerfilrUserForm(instance=request.user)

    return render(request, 'usuario/perfil.html', {'form': form})

#---------------------------------------------------------------------------------------------------------
