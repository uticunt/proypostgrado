'''from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def configurar_roles_y_permisos(sender, **kwargs):
    from . import roles_permisos
    roles_permisos.configurar_roles_y_permisos()'''