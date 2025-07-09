from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['correo', 'rol', 'is_staff', 'is_active']
    list_filter = ['rol', 'is_staff']
    search_fields = ['correo']
    ordering = ['correo']
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Datos Personales', {'fields': ('persona', 'rol')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'password1', 'password2', 'persona', 'rol', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(TipoDocumento)
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Persona)
admin.site.register(Estudiante)
admin.site.register(Docente)
admin.site.register(Acudiente)
admin.site.register(NivelEducativo)
admin.site.register(Grado)
admin.site.register(Area)
admin.site.register(Asignatura)
admin.site.register(Aula)
admin.site.register(Grupo)
admin.site.register(AsignacionDocente)
admin.site.register(Actividad)
admin.site.register(Calificacion)