from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocenteForm, RegistroUsuarioForm, LoginForm, RegistroUsuarioForm, PersonaForm, AreaForm, NivelEducativoForm, GradoForm, AsignaturaForm, AulaForm, GrupoForm, AsignacionDocenteForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Area, NivelEducativo, Grado, Asignatura, Aula, Grupo, AsignacionDocente, Persona, Docente
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .decoradores import rol_requerido
from django.contrib import messages
from .forms import UsuarioUpdateForm


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Guardamos el usuario
            persona = form.cleaned_data['persona']
            usuario = form.save()

            # Extraemos los datos relacionados
            

            # Aquí decides qué hacer con esa info:
            # ejemplo: si el rol es estudiante, crear el estudiante
            if usuario.rol.nombre == 'Estudiante':
                from .models import Estudiante
                Estudiante.objects.create(persona=persona)
                # Aquí puedes guardar nivel y grado en un modelo nuevo si tienes uno para eso

            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def inicio(request):
    return render(request, 'inicio.html')

def login_usuario(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

            # ✅ Autenticación correcta usando authenticate()
            usuario = authenticate(request, correo=correo, password=password)

            if usuario is not None:
                login(request, usuario)

                # ✅ Redirección según el rol
                rol = usuario.rol.nombre.strip().lower()
                if rol == 'coordinador':
                    return redirect('panel_coordinador')
                elif rol == 'docente':
                    return redirect('panel_docente')
                elif rol == 'estudiante':
                    return redirect('panel_estudiante')
                elif rol == 'acudiente':
                    return redirect('panel_acudiente')
                else:
                    return redirect('inicio')
  # Por si el rol no coincide con nada
            else:
                error = "Correo o contraseña incorrectos"
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})


#Area
@rol_requerido('Coordinador')
def lista_areas(request):
    areas = Area.objects.all()
    return render(request, 'coordinador/areas/lista_areas.html', {'areas': areas})


@rol_requerido('Coordinador')
def nueva_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_areas')
    else:
        form = AreaForm()
    return render(request, 'coordinador/areas/area_form.html', {'form': form})

@rol_requerido('Coordinador')
def editar_area(request, area_id):
    area = get_object_or_404(Area, id=area.id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('lista_areas')  # Asegúrate de que esta vista existe
    else:
        form = AreaForm(instance=area)
    return render(request, 'coordinador/areas/area_form.html', {'form': form,'modo': 'Editar'})



def eliminar_area(request, area_id):
    area = get_object_or_404(Area, id=area_id) # Obtiene el objeto Área Académica o un 404 si no existe

    if request.method == 'POST':
        area.delete() # Elimina el objeto del base de datos
        return redirect('lista_areas') # Redirige a la vista de lista_areas

    # Si la petición no es POST (por ejemplo, es GET), se podría renderizar una página de confirmación
    # En este ejemplo simple, asumimos que el POST viene de un formulario de confirmación o un botón
    # que envía un POST directamente. Para una mejor UX, deberías tener una plantilla de confirmación.
    return render(request, 'confirmar_eliminar_area.html', {'area': area}) # O redirigir a lista_areas si no quieres una confirmación explícita
#Cerrar seccion

def logout_view(request):
    logout(request)
    return redirect('login')

#Nivel educativo

@rol_requerido('Coordinador')
def lista_niveles(request):
    niveles = NivelEducativo.objects.all()
    return render(request, 'coordinador/niveles/lista_niveles.html', {'niveles': niveles})

@rol_requerido('Coordinador')
def nuevo_nivel(request):
    if request.method == 'POST':
        form = NivelEducativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_niveles')
    else:
        form = NivelEducativoForm()
    return render(request, 'coordinador/niveles/niveles_form.html', {'form': form, 'modo': 'Nuevo'})

@rol_requerido('Coordinador')
def editar_nivel(request, nivel_id):
    nivel = get_object_or_404(NivelEducativo, id=nivel_id)
    if request.method == 'POST':
        form = NivelEducativoForm(request.POST, instance=nivel)
        if form.is_valid():
            form.save()
            return redirect('lista_niveles')
    else:
        form = NivelEducativoForm(instance=nivel)
    return render(request, 'coordinador/niveles/niveles_form.html', {'form': form, 'modo': 'Editar'})

@rol_requerido('Coordinador')
def eliminar_nivel(request, nivel_id):
    nivel = get_object_or_404(NivelEducativo, id=nivel_id)
    nivel.delete()
    return redirect('lista_niveles')


#Grado

@login_required
@rol_requerido('Coordinador')
def lista_grados(request):
    grados = Grado.objects.select_related('nivel').all()
    return render(request, 'coordinador/grados/lista_grados.html', {'grados': grados})

@login_required
@rol_requerido('Coordinador')
def registrar_grado(request):
    if request.method == 'POST':
        form = GradoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_grados')
    else:
        form = GradoForm()
    return render(request, 'coordinador/grados/form_grado.html', {'form': form, 'modo': 'Registrar'})

@login_required
@rol_requerido('Coordinador')
def editar_grado(request, grado_id):
    grado = get_object_or_404(Grado, id=grado_id)
    if request.method == 'POST':
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            return redirect('lista_grados')
    else:
        form = GradoForm(instance=grado)
    return render(request, 'coordinador/grados/form_grado.html', {'form': form, 'modo': 'Editar'})

def eliminar_grado(request, grado_id):
    grado = get_object_or_404(Grado, id=grado_id)
    
    if request.method == 'POST':
        grado.delete()
        messages.success(request, 'Grado eliminado correctamente.')
        return redirect('lista_grados')

    # Si alguien accede directamente por GET sin confirmar, redirige o muestra una alerta
    messages.warning(request, 'Para eliminar un grado debes confirmar la acción.')
    return redirect('lista_grados')

#Asignatura

@login_required
@rol_requerido('Coordinador')
def lista_asignaturas(request):
    asignaturas = Asignatura.objects.select_related('grado', 'area').all()
    return render(request, 'coordinador/asignaturas/lista_asignaturas.html', {'asignaturas': asignaturas})

@login_required
@rol_requerido('Coordinador')
def registrar_asignatura(request):
    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_asignaturas')
    else:
        form = AsignaturaForm()
    return render(request, 'coordinador/asignaturas/form_asignatura.html', {'form': form, 'modo': 'Registrar'})

@login_required
@rol_requerido('Coordinador')
def editar_asignatura(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            return redirect('lista_asignaturas')
    else:
        form = AsignaturaForm(instance=asignatura)
    return render(request, 'coordinador/asignaturas/form_asignatura.html', {'form': form, 'modo': 'Editar'})


#Aulas

@rol_requerido('Coordinador')
def lista_aulas(request):
    aulas = Aula.objects.all()
    return render(request, 'coordinador/aulas/lista_aulas.html', {'aulas': aulas})

@rol_requerido('Coordinador')
def nueva_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_aulas')
    else:
        form = AulaForm()
    return render(request, 'coordinador/aulas/nueva_aula.html', {'form': form})

#Grupo

@rol_requerido('Coordinador')
def lista_grupos(request):
    grupos = Grupo.objects.select_related('grado', 'aula')
    return render(request, 'coordinador/grupos/lista_grupos.html', {'grupos': grupos})

@rol_requerido('Coordinador')
def nuevo_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_grupos')
    else:
        form = GrupoForm()
    return render(request, 'coordinador/grupos/nuevo_grupo.html', {'form': form})

#Asignacion de docente

@rol_requerido('Coordinador')
def lista_asignaciones(request):
    asignaciones = AsignacionDocente.objects.select_related('docente', 'grupo', 'asignatura')
    return render(request, 'coordinador/asignaciones/lista_asignaciones.html', {'asignaciones': asignaciones})

@rol_requerido('Coordinador')
def nueva_asignacion(request):
    if request.method == 'POST':
        form = AsignacionDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_asignaciones')
    else:
        form = AsignacionDocenteForm()
    return render(request, 'coordinador/asignaciones/nueva_asignacion.html', {'form': form})

#Usuarios

@rol_requerido('Coordinador')
def registrar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Persona registrada correctamente.')
            return redirect('listar_personas')
    else:
        form = PersonaForm()
    return render(request, 'coordinador/personas/registrar_persona.html', {'form': form})

@rol_requerido('Coordinador')
def listar_personas(request):
    personas = Persona.objects.all()
    return render(request, 'coordinador/personas/listar_personas.html', {'personas': personas})

@login_required
@rol_requerido('Coordinador')
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.persona = form.cleaned_data['persona']
            print("🧠 Persona asignada al usuario:", usuario.persona)
            usuario.save()
            

            # Crear perfil automático según el rol
            rol_nombre = usuario.rol.nombre.strip().lower()

            if rol_nombre == 'docente':
                from .models import Docente
                if not Docente.objects.filter(persona=usuario.persona).exists():
                    docente, creado = Docente.objects.get_or_create(
                        persona=usuario.persona,
                        defaults={'especialidad': 'Por definir'}
                    )
                    print("✅ Docente creado:", creado)

            elif rol_nombre == 'estudiante':
                from .models import Estudiante
                if not Estudiante.objects.filter(persona=usuario.persona).exists():
                    Estudiante.objects.create(persona=usuario.persona)

            elif rol_nombre == 'acudiente':
                from .models import Acudiente
                if not Acudiente.objects.filter(persona=usuario.persona).exists():
                    Acudiente.objects.create(persona=usuario.persona)
            print("Campos del formulario:", form.fields)
            print("Errores:", form.errors)
            return redirect('lista_usuarios')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'coordinador/usuarios/registrar_usuario.html', {'form': form})

@rol_requerido('Coordinador')
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('persona', 'rol')
    return render(request, 'coordinador/usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@rol_requerido('Coordinador')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    form = RegistroUsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('lista_usuarios')
    return render(request, 'coordinador/usuarios/editar_usuario.html', {'form': form})

@rol_requerido('Coordinador')
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('lista_usuarios')

    # Protección si acceden por GET
    return redirect('lista_usuarios')

def rol_requerido(rol_nombre):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.rol.nombre.strip().lower() == rol_nombre.strip().lower():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return login_required(_wrapped_view)
    return decorator

@rol_requerido('Docente')
def panel_docente(request):
    return render(request, 'docente/panel_docente.html')

@rol_requerido('Docente')
def hoja_vida_docente(request):
    print("🔍 Usuario:", request.user)
    print("🔍 Persona:", request.user.persona)
    persona = request.user.persona
    if not persona:
        return HttpResponse("Este usuario no tiene una persona asociada.")

    docente = Docente.objects.filter(persona=persona).first()
    if not docente:
        return HttpResponse("Este usuario no tiene un perfil de Docente asignado.")
    
    return render(request, 'docente/hoja_vida.html', {'docente': docente})
    

@rol_requerido('Docente')
def editar_datos_docente(request):
    docente = get_object_or_404(Docente, persona=request.user.persona)
    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            return redirect('hoja_vida_docente')
    else:
        form = DocenteForm(instance=docente)
    return render(request, 'docente/editar_datos.html', {'form': form})


@rol_requerido('Estudiante')
def panel_estudiante(request):
    return render(request, 'estudiantes/panel_estudiante.html')

@rol_requerido('Acudiente')
def panel_acudiente(request):
    return render(request, 'acudientes/panel_acudiente.html')

# 📌 Vista: Registrar usuarios desde el panel del Coordinador
# Protegida por rol 'Coordinador'. Usa el formulario RegistroUsuarioForm.
@rol_requerido('coordinador')
def registrar_usuario_panel(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'coordinador/usuarios/registrar_usuario.html', {
        'form': form
    })

@login_required
@rol_requerido('Coordinador')
def editar_area(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('lista_areas')
    else:
        form = AreaForm(instance=area)
    return render(request, 'coordinador/areas/form_area.html', {'form': form, 'modo': 'Editar'})
    
#Validar usuario

@rol_requerido('Coordinador')
def panel_coordinador(request):
    usuarios_pendientes = Usuario.objects.filter(is_active=False)
    return render(request, 'coordinador/panel_coordinador.html', {
        'usuarios_pendientes': usuarios_pendientes,
        'cantidad_pendientes': usuarios_pendientes.count()
    })


@rol_requerido('Coordinador')
def validar_usuarios(request):
    usuarios_pendientes = Usuario.objects.filter(is_active=False)
    return render(request, 'coordinador/validar_usuarios.html', {
        'usuarios': usuarios_pendientes
    })

@rol_requerido('Coordinador')
def activar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    usuario.is_active = True
    usuario.save()
    return redirect('validar_usuarios')



@login_required
def ver_perfil(request):
    # Esta vista simplemente renderiza la plantilla. Los datos vienen de request.user en la plantilla.
    return render(request, 'usuarios/perfil.html')

@login_required
def editar_perfil(request):
    persona = request.user.persona  # Obtiene la instancia de Persona asociada al usuario
    usuario = request.user          # Obtiene la instancia del Usuario actual

    if request.method == 'POST': #
        # Instancia los formularios con los datos POST y las instancias existentes
        form_persona = PersonaForm(request.POST, instance=persona) #
        form_usuario = UsuarioUpdateForm(request.POST, instance=usuario) #

        if form_persona.is_valid() and form_usuario.is_valid(): #
            form_persona.save() # Guarda los cambios en la instancia de Persona
            form_usuario.save() # Guarda los cambios en la instancia de Usuario
            messages.success(request, 'Perfil actualizado correctamente.') #
            return redirect('ver_perfil') # Redirige a la vista de perfil después de guardar
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil. Por favor, revisa los datos.') #
    else:
        # Si es una petición GET, instancia los formularios con los datos existentes
        form_persona = PersonaForm(instance=persona) #
        form_usuario = UsuarioUpdateForm(instance=usuario) #

    context = {
        'form_persona': form_persona, # Pasa el formulario de Persona al contexto
        'form_usuario': form_usuario, # Pasa el formulario de Usuario al contexto
    }
    return render(request, 'usuarios/editar_perfil.html', context) #