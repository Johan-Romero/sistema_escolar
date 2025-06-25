from django.urls import path

from .views import registrar_usuario_panel, inicio, login_usuario, logout_view

from .views import panel_coordinador, panel_docente, panel_estudiante, panel_acudiente, lista_areas, nueva_area, editar_area, lista_niveles, nuevo_nivel, editar_nivel, eliminar_nivel, lista_grados, registrar_grado, editar_grado, lista_asignaturas, registrar_asignatura, editar_asignatura, lista_aulas, nueva_aula, lista_grupos, nuevo_grupo, lista_asignaciones, nueva_asignacion, validar_usuarios, activar_usuario, lista_usuarios, editar_usuario, registrar_persona, registrar_usuario, eliminar_grado, listar_personas, registrar_usuario_panel, eliminar_usuario, hoja_vida_docente, editar_datos_docente


urlpatterns = [
    path('', inicio, name='inicio'),

    path('login/', login_usuario, name='login'),

    path('coordinador/', panel_coordinador, name='panel_coordinador'),

    path('docente/', panel_docente, name='panel_docente'),

    path('docente/hoja-vida/', hoja_vida_docente, name='hoja_vida_docente'),

    path('docente/hoja-vida/editar/', editar_datos_docente, name='editar_datos_docente'),

    path('estudiante/', panel_estudiante, name='panel_estudiante'),

    path('acudiente/', panel_acudiente, name='panel_acudiente'),

    path('coordinador/areas/', lista_areas, name='lista_areas'),

    path('coordinador/areas/<int:area_id>/editar/', editar_area, name='editar_area'),

    path('coordinador/areas/nuevo/', nueva_area, name='nueva_area'),

    path('logout/', logout_view, name='logout'),

    path('coordinador/niveles/', lista_niveles, name='lista_niveles'),

    path('coordinador/niveles/nuevo/', nuevo_nivel, name='nuevo_nivel'),

    path('coordinador/niveles/<int:nivel_id>/editar/', editar_nivel, name='editar_nivel'),
    
    path('coordinador/niveles/<int:nivel_id>/eliminar/', eliminar_nivel, name='eliminar_nivel'),

    path('coordinador/grados/', lista_grados, name='lista_grados'),

    path('coordinador/grados/nuevo/', registrar_grado, name='registrar_grado'),

    path('coordinador/grados/<int:grado_id>/editar/', editar_grado, name='editar_grado'),

    path('coordinador/grados/<int:grado_id>/eliminar/', eliminar_grado, name='eliminar_grado'),

    path('coordinador/asignaturas/', lista_asignaturas, name='lista_asignaturas'),

    path('coordinador/asignaturas/nueva/', registrar_asignatura, name='registrar_asignatura'),

    path('coordinador/asignaturas/<int:asignatura_id>/editar/',editar_asignatura, name='editar_asignatura'),

    path('coordinador/aulas/', lista_aulas, name='lista_aulas'),

    path('coordinador/aulas/nueva/', nueva_aula, name='nueva_aula'),

    path('coordinador/grupos/', lista_grupos, name='lista_grupos'),

    path('coordinador/grupos/nuevo/', nuevo_grupo, name='nuevo_grupo'),

    path('coordinador/asignaciones/', lista_asignaciones, name='lista_asignaciones'),
    
    path('coordinador/asignaciones/nueva/', nueva_asignacion, name='nueva_asignacion'),

    path('coordinador/usuarios/pendientes/', validar_usuarios, name='validar_usuarios'),

    path('coordinador/usuarios/activar/<int:usuario_id>/', activar_usuario, name='activar_usuario'),

    path('coordinador/usuarios/', lista_usuarios, name='lista_usuarios'),

    path('coordinador/usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),

    path('coordinador/usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    
    path('coordinador/personas/nueva/', registrar_persona, name='registrar_persona'),

    path('coordinador/registrar_usuario/', registrar_usuario, name='registrar_usuario'),

    path('coordinador/personas/nuevo/', registrar_persona, name='registrar_persona'),

    path('coordinador/personas/', listar_personas, name='listar_personas'),

    path('coordinador/registrar_usuario_panel/', registrar_usuario_panel, name='registrar_usuario_panel'),

]



