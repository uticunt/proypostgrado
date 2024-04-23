from django import forms 
from django.forms import fields 
from appevaluacion.models import *
from django.contrib.auth.models import User
import datetime

class PostulanteForm(forms.ModelForm):
    class Meta:
        model = Postulante
        fields = [
            'idPostulante',
            'codigo',
            'ap_paterno',            
            'ap_materno',
            'nombres',
            'dni',
            'email',
            'celular',            
            'pdf_curriculum',            
            'doctorado',            
            'maestria',
            'unidad',
            'modalidad',
        ]
        widgets = {                            
            #'codigo': forms.TextInput(attrs={'placeholder': True}),
            'ap_paterno': forms.TextInput(attrs={'placeholder': 'Ingrese apellido paterno'}),
            'ap_materno': forms.TextInput(attrs={'placeholder': 'Ingrese apellido materno'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Ingrese nombres completos'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese dni'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Ingrese celular'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese correo electronico'}),
            'pdf_curriculum': forms.TextInput(attrs={'placeholder': 'Ingrese enlace de drive'}),
                          
        }
        labels = {
            'codigo': 'Codigo',
            'ap_paterno': 'Apellido paterno',
            'ap_materno': 'Apellido materno',
            'nombres': 'Nombres',
            'dni': 'Dni',
            'email': 'Email',
            'celular': 'Celular',
            'pdf_curriculum': 'Drive | Curriculum Vitae',
            'doctorado': 'Doctorado',
            'maestria': 'Maestria',
            'unidad': 'Unidad',
            'modalidad': 'Modalidad',                         
        }

class EvaluadorForm(forms.ModelForm):
    class Meta:
        model = Evaluador
        fields = [
            'idEvaluador',
            'codigo_evaluador',
            'user',
            'apellidos',            
            'nombres',
            'dni',
            'email',
            'activo',                    
            'cargo',                          
            'unidad',               
        ]
        widgets = {                            
            'codigo_evaluador': forms.TextInput(attrs={'placeholder': 'Ingrese codigo'}),     
            'nombres': forms.TextInput(attrs={'placeholder': 'Ingrese nombres completos'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ingrese apellidos'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese dni'}),           
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese correo electronico'}),                                
        }
        labels = {
            'codigo_evaluador': 'Codigo',
            'apellidos': 'Apellidos',
            'user': '',
            'nombres': 'Nombres',
            'dni': 'Dni',
            'email': 'Email',
            'celular': 'Celular',  
            'cargo' : 'Cargo',                     
            'unidad': 'Unidad',                                   
        }

    def __init__(self, *args, **kwargs):
        super(EvaluadorForm, self).__init__(*args, **kwargs)        
        usuarios_disponibles = User.objects.exclude(evaluador__isnull=False)
        self.fields['user'].queryset = usuarios_disponibles

class EvaluacionForm(forms.ModelForm):
    def __init__(self, *args, unidades=None, **kwargs):
        super().__init__(*args, **kwargs)
        postulantes_asignados = Evaluacion.objects.values_list('postulante', flat=True)
        self.fields['postulante'].queryset = Postulante.objects.exclude(idPostulante__in=postulantes_asignados)
      
    class Meta:
        model = Evaluacion        
        fields = [
            'idEvaluacion',
            'codigo_evaluacion',
            'estado_evaluacion',          
            'postulante',         
            'evaluador',
            'fecha_creacion',          
        ]
        exclude = ['codigo_evaluacion']
        widgets = {              
            'codigo_evaluacion': forms.TextInput(attrs={'required': False, 'readonly': True}),
            'fecha_creacion': forms.TextInput(attrs={'readonly': True}),       
        }
        labels = {
            'fecha_creacion': '',
        }

class DetalleEvaluacionForm(forms.ModelForm):
 

    class Meta:
        model = DetalleEvaluacion
        fields =  [
            'idDetalleEva',
            'evaluacion',           
            'puntaje_promedioP',
            'puntaje_cursosEva',
            'puntaje_partCientifica',
            'puntaje_docenciaUni',
            'puntaje_idiomaExt',
            'puntaje_capacitacion',
            'puntaje_libroInscritos',
            'puntaje_publicaciones',         
            'puntaje_produccionCien',
            'puntajeFinal',       
        ]
        labels = {
            'puntaje_promedioP': '',
            'puntaje_cursosEva': '',
            'puntaje_partCientifica': '',
            'puntaje_docenciaUni': '',
            'puntaje_idiomaExt': '',
            'puntaje_capacitacion': '',
            'puntaje_libroInscritos': '',
            'puntaje_publicaciones': '',           
            'puntaje_produccionCien': '',
            'puntajeFinal': '',    
            
            # Define las etiquetas personalizadas para otros campos aquí
        }
        widgets = {
            'evaluacion': forms.TextInput(attrs={'required': False, 'readonly': True}),
            'puntaje_capacitacion': forms.TextInput(attrs={'required': False, 'readonly': True}),
            'puntaje_produccionCien': forms.TextInput(attrs={'required': False, 'readonly': True}),
            'puntajeFinal': forms.TextInput(attrs={'required': False, 'readonly': True})
        }

