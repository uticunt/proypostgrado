import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Evaluador,Evaluacion, Postulante  # Asegúrate de importar tu modelo específico
from django.db.models import Max
from .models import Evaluador


def generar_codigo_evaluador():    
    ultimo_codigo = Evaluador.objects.aggregate(Max('codigo_evaluador'))['codigo_evaluador__max']    
    if ultimo_codigo:       
        ultimo_numero = int(ultimo_codigo.split('-')[1])
    else:       
        ultimo_numero = 0     
    nuevo_numero = ultimo_numero + 1       
    nuevo_codigo = 'EV-' + str(nuevo_numero).zfill(5)    
    return nuevo_codigo


@receiver(pre_save, sender=Evaluador)
def set_codigo_evaluador(sender, instance, **kwargs):
    if not instance.codigo_evaluador:
        instance.codigo_evaluador = generar_codigo_evaluador()

#    E00012401 
@receiver(post_save, sender=Evaluacion)
def generar_codigo_evaluacion(sender, instance, created, **kwargs):
    if created and not instance.codigo_evaluacion:                    
        codigo = f"E{instance.pk:04d}2401"
        instance.codigo_evaluacion = codigo
        instance.save()

post_save.connect(generar_codigo_evaluacion, sender=Evaluacion)
