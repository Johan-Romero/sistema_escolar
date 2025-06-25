from .models import Usuario

def usuarios_pendientes(request):
    if request.user.is_authenticated and hasattr(request.user, 'rol'):
        if request.user.rol.nombre.lower() == 'coordinador':
            cantidad = Usuario.objects.filter(is_active=False).count()
            return {'notificaciones_pendientes': cantidad}
    return {'notificaciones_pendientes': 0}
