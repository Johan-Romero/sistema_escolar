from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def rol_requerido(Coordinador):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            perfil = getattr(request.user, 'perfil', None)
            if request.user.rol.nombre in Coordinador:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorador
