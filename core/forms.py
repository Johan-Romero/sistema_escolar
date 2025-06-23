from django import forms
from .models import Usuario, Rol, Persona, NivelEducativo, Grado, Persona, Area, Asignatura, Tema, Logro, Aula, Grupo, AsignacionDocente
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
            'direccion_linea2': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'sexo': forms.Select(choices=Persona.SEXO_CHOICES),
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