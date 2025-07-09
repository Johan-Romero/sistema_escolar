from core.models import TipoDocumento, Ciudad, Departamento, Persona, Rol, Usuario

# Crear datos básicos
dep, _ = Departamento.objects.get_or_create(nombre='Antioquia')
ciudad, _ = Ciudad.objects.get_or_create(nombre='Medellín', departamento=dep)
tipo_doc, _ = TipoDocumento.objects.get_or_create(nombre='Cédula de Ciudadanía')
rol, _ = Rol.objects.get_or_create(nombre='Administrador')

persona, _ = Persona.objects.get_or_create(
    primer_nombre='Juan',
    segundo_nombre='Carlos',
    primer_apellido='Pérez',
    segundo_apellido='Gómez',
    tipo_documento=tipo_doc,
    numero_documento='111111111',
    ciudad=ciudad,
    direccion_linea1='Calle 123',
)

# Crear superusuario
Usuario.objects.create_superuser(
    correo='admin@example.com',
    password='admin123',
    persona=persona,
    rol=rol,
    is_staff=True,
    is_superuser=True
)
print("✅ Superusuario creado correctamente.")