from core.models import Usuario

def notificaciones_context(request):
    if request.user.is_authenticated and request.user.rol.nombre == 'Coordinador':
        cantidad_pendientes = Usuario.objects.filter(is_active=True).count()
        return {'notificaciones_pendientes': cantidad_pendientes}
    return {}
