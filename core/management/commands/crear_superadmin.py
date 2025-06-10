from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Persona, Rol, TipoDocumento, Ciudad, Departamento

class Command(BaseCommand):
    help = 'Crea un superusuario coordinador con datos predeterminados.'

    def handle(self, *args, **options):
        Usuario = get_user_model()

        if Usuario.objects.filter(correo='admin@admin.com').exists():
            self.stdout.write(self.style.WARNING("⚠️ El superadmin ya existe."))
            return

        # Crear datos base si no existen
        depto, _ = Departamento.objects.get_or_create(nombre='Antioquia')
        ciudad, _ = Ciudad.objects.get_or_create(nombre='Medellín', departamento=depto)
        tipo_doc, _ = TipoDocumento.objects.get_or_create(nombre='Cédula')
        persona, _ = Persona.objects.get_or_create(
            primer_nombre="Zoe",
            primer_apellido="Admin",
            tipo_documento=tipo_doc,
            numero_documento="99999999",
            direccion_linea1="Calle Admin 123",
            ciudad=ciudad
        )
        rol, _ = Rol.objects.get_or_create(nombre='Coordinador')

        # Crear superusuario
        Usuario.objects.create_superuser(
            correo='admin@admin.com',
            password='admin1234',
            persona=persona,
            rol=rol,
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(self.style.SUCCESS("✅ Superadmin creado correctamente."))