from django import forms
from .models import Usuario, Rol, Persona, NivelEducativo, Grado, Persona, Area, Asignatura, Aula, Grupo, AsignacionDocente, Docente, FormacionAcademica, Capacitacion, Idioma, ExperienciaLaboral
from django.contrib.auth.hashers import make_password


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full border border-gray-300 rounded-md px-4 py-2',
            'placeholder': 'Contraseña segura'
        }),
        help_text='Debe tener al menos 8 caracteres.'
    )

    class Meta:
        model = Usuario
        fields = ['correo', 'password', 'rol', 'persona']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-input block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'persona': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.all()
        self.fields['persona'].queryset = Persona.objects.all()

    def clean_persona(self):
        persona = self.cleaned_data.get('persona')
        qs = Usuario.objects.filter(persona=persona)

        # Si estamos editando, excluye el usuario actual
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Esta persona ya está asociada a otro usuario.")
        
        return persona

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return make_password(password)
    
class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'tipo_documento', 'numero_documento', 'fecha_nacimiento', 'sexo',
            'telefono', 'correo_personal',
            'direccion_linea1', 'direccion_linea2', 'ciudad'
        ]
        widgets = {
            'direccion_linea2': forms.TextInput(attrs={'placeholder': 'Opcional', 'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'sexo': forms.Select(choices=Persona.SEXO_CHOICES, attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'primer_nombre': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'segundo_nombre': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'tipo_documento': forms.Select(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'numero_documento': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'telefono': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'correo_personal': forms.EmailInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'direccion_linea1': forms.TextInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
            'ciudad': forms.Select(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'obligatoria'] # Specify the fields you want in the form
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Matemáticas', 'class': 'form-control'}),
            # 'obligatoria' is likely a CheckboxInput, default rendering is usually fine,
            # but you can customize if needed.
        }


       
class NivelEducativoForm(forms.ModelForm):
    class Meta:
        model = NivelEducativo
        fields = ['nombre', 'descripcion'] # Added 'descripcion'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-purple-500 focus:border-purple-500',
                'placeholder': 'Ej. Primaria, Secundaria, Preescolar',
                'required': 'required'
            }),
            'descripcion': forms.Textarea(attrs={ # New widget for descripcion
                'class': 'block w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-purple-500 focus:border-purple-500',
                'placeholder': 'Breve descripción del nivel educativo (opcional)',
                'rows': 3 # Adjust rows as needed
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'nombre':
                field.label = 'Nombre del Nivel Educativo'
            elif field_name == 'descripcion': # Set label for descripcion
                field.label = 'Descripción'
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
            })
class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['nivel', 'nombre']
        widgets = {
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'grado', 'area']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'grado': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
        }


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['nombre', 'capacidad', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'capacidad': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'estado': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['grado', 'nombre', 'aula']
        widgets = {
            'grado': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'aula': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }



class AsignacionDocenteForm(forms.ModelForm):
    class Meta:
        model = AsignacionDocente
        fields = ['docente', 'grupo', 'asignatura']
        widgets = {
            'docente': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'grupo': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'asignatura': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }

#DOCENTE

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['especialidad']

class FormacionAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacionAcademica
        exclude = ['docente']

class CapacitacionForm(forms.ModelForm):
    class Meta:
        model = Capacitacion
        exclude = ['docente']

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        exclude = ['docente']

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        exclude = ['docente']

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo', 'rol'] # Asegúrate de que 'nombre_de_usuario' exista en tu modelo Usuario si lo usas
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2', 'readonly': 'readonly'}),
            'rol': forms.Select(attrs={'class': 'block w-full border border-gray-300 rounded-md px-4 py-2', 'readonly': 'readonly'}), # Generalmente el rol no se edita aquí
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace que los campos sean de solo lectura si no quieres que se editen
        # if 'correo' in self.fields:
        #     self.fields['correo'].widget.attrs['readonly'] = 'readonly'
        # if 'rol' in self.fields:
        #     self.fields['rol'].widget.attrs['disabled'] = 'disabled' # disabled también evita que el valor sea enviado en POST