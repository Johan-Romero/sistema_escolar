from django import forms
from .models import Usuario, Rol, NivelEducativo, Grado, Persona, Ciudad, TipoDocumento, Departamento, Area, Asignatura, Tema, Logro, Aula, Grupo, AsignacionDocente
from django.contrib.auth.hashers import make_password

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="""<ul>
                        <li>Debe tener al menos 8 caracteres.</li>
                        <li>Incluir mayúsculas y minúsculas.</li>
                        <li>Contener al menos un número.</li>
                        <li>Debe tener un símbolo especial: #, $, %, !</li>
                    </ul>"""  # Asegúrate de cerrar correctamente la cadena
    )
    

    class Meta:
        model = Usuario
        fields = ['correo', 'password', 'rol', 'persona']


    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Aquí puedes agregar validaciones adicionales si lo deseas
        return make_password(password)
    
    def clean_persona(self):
        persona = self.cleaned_data.get('persona')
        if Usuario.objects.filter(persona=persona).exists():
            raise forms.ValidationError("Esta persona ya está asociada a un usuario.")
        return persona
    

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'tipo_documento', 'numero_documento', 'direccion_linea1', 'direccion_linea2',
            'ciudad'
        ]
        widgets = {
            'direccion_linea2': forms.TextInput(attrs={'placeholder': 'Opcional'})
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'obligatoria']

class NivelEducativoForm(forms.ModelForm):
    class Meta:
        model = NivelEducativo
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Primaria'}),
        }


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

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['asignatura', 'nombre']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }


class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = ['asignatura', 'descripcion']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-2 border rounded'}),
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