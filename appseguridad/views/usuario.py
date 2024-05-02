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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from openpyxl import Workbook
from django.http.response import HttpResponse
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

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

# Descargar un archivo Excel
@login_required
def descargar_excel_usuarios(request):
    # Crear un libro de trabajo
    wb = Workbook()
    ws = wb.active
    ws.title = "Credenciales de Usuarios"

    # Encabezado general en negrita y centrado
    ws['A1'] = 'CREDENCIALES DE USUARIOS'
    ws.merge_cells('A1:D1')
    ws['A1'].font = Font(bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Encabezados del archivo Excel en negrita y centrados
    columns = ['ID', 'NOMBRE Y APELLIDOS', 'USERNAME', 'PASSWORD']
    ws.append(columns)
    for cell in ws[2]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Obtener datos de usuarios
    users = User.objects.all()
    for user in users:      
        # La contraseña se muestra como está en la base de datos (HASH)
        row = [
            user.id,
            f"{user.first_name} {user.last_name}",
            user.username,
            user.password 
        ]
        ws.append(row)

    # Aplicar bordes a toda la tabla
    max_row = ws.max_row
    max_column = ws.max_column
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    for row in ws.iter_rows(min_row=1, max_col=max_column, max_row=max_row):
        for cell in row:
            cell.border = thin_border

   # Ajustar el ancho de las columnas automáticamente
    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except TypeError:
                pass
        adjusted_width = (max_length + 2) * 1.2
        column_letter = get_column_letter(column[0].column)
        ws.column_dimensions[column_letter].width = adjusted_width



    # Establecer el nombre del archivo
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=credenciales_usuarios.xlsx'

    # Guardar el libro de trabajo en la respuesta
    wb.save(response)
    return response

#-----------------------------------------------------------------------------------------


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