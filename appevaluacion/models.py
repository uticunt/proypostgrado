from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError


SEXO = (('M', 'Masculino'),
        ('F', 'Femenino'),)

CARGO = (('Presidente','Presidente'),
         ('Secretario','Secretario'),
         ('Vocal','Vocal'))

class Modalidad(models.Model):
    idModalidad = models.AutoField(primary_key=True)
    des_modalidad = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return f'{self.des_modalidad}'

class Maestria(models.Model):
    idMaestria = models.AutoField(primary_key = True)   
    des_maestria = models.CharField(max_length=100, null=False)   
    
    def __str__(self):
        return f'{self.des_maestria}'

class Doctorado(models.Model):
    idDoctorado = models.AutoField(primary_key = True)   
    des_doctorado = models.CharField(max_length=100, null=False)    
    
    def __str__(self):
        return f'{self.des_doctorado}'
    
class Unidad(models.Model):
    idUnidad= models.AutoField(primary_key = True)   
    des_unidad = models.CharField(max_length=100, null=False)    
    
    def __str__(self):
        return f'{self.des_unidad}'

class Postulante(models.Model):
    idPostulante = models.AutoField(primary_key=True, null=False)   
    codigo = models.CharField(max_length=10, null=True)
    ap_paterno = models.CharField(max_length=100, null=False)
    ap_materno = models.CharField(max_length=100, null=False)
    nombres = models.CharField(max_length=100, null=False)    
    dni = models.CharField(max_length=20, null=False, unique = True)  
    email = models.EmailField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)    
    pdf_curriculum = models.CharField(max_length=200,blank=True, null=True)   
    doctorado = models.ForeignKey(Doctorado, on_delete = models.CASCADE, related_name='postulantes_doctorado', null=True, blank=True)   
    maestria = models.ForeignKey(Maestria, on_delete = models.CASCADE,related_name='postulantes_maestria', null=True, blank=True ) 
    unidad = models.ForeignKey(Unidad, null=True, on_delete = models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, null=True, on_delete = models.CASCADE)

    def clean(self):
        # Validar que solo se haya ingresado una maestría o un doctorado, pero no ambos.
        if self.maestria and self.doctorado:
            raise ValidationError("Un postulante solo puede tener una maestría o un doctorado, no ambos.")
        if not self.maestria and not self.doctorado:
            raise ValidationError("Debe ingresar al menos una maestría o un doctorado.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombres} {self.ap_paterno} {self.ap_materno}'

class Evaluador(models.Model):
    idEvaluador = models.AutoField(primary_key=True, null=False)
    codigo_evaluador = models.CharField(max_length=6, default='123456') 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=100, null=False)
    dni = models.CharField(max_length=8, null=True)    
    email = models.EmailField(max_length=100, null=True)      
    activo = models.BooleanField(default= True)
    cargo = models.CharField(max_length=20, choices=CARGO, default='Presidente')
    unidad = models.ForeignKey(Unidad, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Evaluacion(models.Model):
    idEvaluacion= models.AutoField(primary_key=True, null=False)
    codigo_evaluacion = models.CharField(max_length=10,unique = True, null=True)
    estado_evaluacion = models.BooleanField(default= False)
    postulante = models.ForeignKey(Postulante,unique = True , on_delete = models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete = models.CASCADE)    
    fecha_creacion = models.DateField(default=date.today)
  
    def __str__(self):
        return f'Datos Evaluacion {self.codigo_evaluacion}: {self.evaluador} | {self.postulante}'
     
class DetalleEvaluacion(models.Model):
    idDetalleEva = models.AutoField(primary_key=True, null = False)
    evaluacion = models.ForeignKey(Evaluacion,unique = True ,on_delete = models.CASCADE, null = False)
    puntaje_promedioP = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(7.50)], null=False, default=0)
    puntaje_cursosEva = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(2.50), MaxValueValidator(9.5)] , null=False, default=0)
    puntaje_partCientifica = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(10.00)], null=False, default=0)
    puntaje_docenciaUni = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(14.00)], null=False, default=0)
    puntaje_idiomaExt = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(6.00)], null=False, default=0)
    puntaje_capacitacion = models.DecimalField(max_digits=5,decimal_places=2, validators=[MaxValueValidator(47.00)], null=False, default=0) # Primer Subtotal
    puntaje_libroInscritos = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(8.40)], null=False, default=0)
    puntaje_publicaciones = models.DecimalField(max_digits=5,decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(11.50)], null=False, default=0)   
    puntaje_produccionCien = models.DecimalField(max_digits=5,decimal_places=2, validators=[MaxValueValidator(19.90)], null=False, default=0)  # Segundo Subtotal
    puntajeFinal = models.DecimalField(max_digits=5,decimal_places=2, validators=[MaxValueValidator(66.90)], null=False, default=0) # Primer Subtotal +  Segundo Subtotal

    def __str__(self):
        return f'Detalla: {self.puntaje_capacitacion} + {self.puntaje_produccionCien} = {self.puntajeFinal}'