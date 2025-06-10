from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import Usuario, Area, NivelEducativo, Grado, Asignatura
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegistroUsuarioForm, PersonaForm
from .forms import AreaForm, NivelEducativoForm, GradoForm, AsignaturaForm
from .decoradores import rol_requerido



def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Guardamos el usuario
            usuario = form.save()

            # Extraemos los datos relacionados
            nivel = form.cleaned_data['nivel_educativo']
            grado = form.cleaned_data['grado']
            persona = form.cleaned_data['persona']

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
    return render(request, 'coordinador/areas/areas_list.html', {'areas': areas})


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
    area = get_object_or_404(Area, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('lista_areas')  # Asegúrate de que esta vista existe
    else:
        form = AreaForm(instance=area)
    return render(request, 'coordinador/areas/area_form.html', {'form': form,'modo': 'Editar'})

#Cerrar seccion

def logout_view(request):
    logout(request)
    return redirect('login')

#Nivel educativo

@rol_requerido('Coordinador')
def lista_niveles(request):
    niveles = NivelEducativo.objects.all()
    return render(request, 'coordinador/niveles/niveles_list.html', {'niveles': niveles})

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




def rol_requerido(rol_nombre):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.rol.nombre.strip().lower() == rol_nombre.strip().lower():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return login_required(_wrapped_view)
    return decorator

@rol_requerido('Coordinador')
def panel_coordinador(request):
    return render(request, 'coordinador/panel_coordinador.html')

@rol_requerido('Docente')
def panel_docente(request):
    return render(request, 'docente/panel_docente.html')

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
    from .forms import RegistroUsuarioForm, PersonaForm

    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        usuario_form = RegistroUsuarioForm(request.POST)

        if persona_form.is_valid() and usuario_form.is_valid():
            persona = persona_form.save()
            usuario = usuario_form.save(commit=False)
            usuario.persona = persona
            usuario.set_password(usuario_form.cleaned_data['password'])
            usuario.save()

            rol = usuario.rol.nombre.strip().lower()

            if rol == 'estudiante':
                Estudiante.objects.create(persona=persona)
            elif rol == 'docente':
                Docente.objects.create(persona=persona, especialidad='')
            elif rol == 'acudiente':
                Acudiente.objects.create(persona=persona)

            return redirect('panel_coordinador')
    else:
        persona_form = PersonaForm()
        usuario_form = RegistroUsuarioForm()

    # ✅ Esto va fuera del if
    return render(request, 'coordinador/registrar_usuario.html', {
        'persona_form': persona_form,
        'usuario_form': usuario_form
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
    



