from django.urls import path
from .views import registrar_usuario_panel, inicio, login_usuario, logout_view
from .views import panel_coordinador, panel_docente, panel_estudiante, panel_acudiente, lista_areas, nueva_area, editar_area, lista_niveles, nuevo_nivel, editar_nivel, eliminar_nivel, lista_grados, registrar_grado, editar_grado, lista_asignaturas, registrar_asignatura, editar_asignatura


urlpatterns = [
    path('', inicio, name='inicio'),

    path('login/', login_usuario, name='login'),

    path('coordinador/', panel_coordinador, name='panel_coordinador'),

    path('docente/', panel_docente, name='panel_docente'),

    path('estudiante/', panel_estudiante, name='panel_estudiante'),

    path('acudiente/', panel_acudiente, name='panel_acudiente'),

    path('coordinador/registrar_usuario/', registrar_usuario_panel, name='registrar_usuario_panel'),

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

    path('coordinador/asignaturas/', lista_asignaturas, name='lista_asignaturas'),

    path('coordinador/asignaturas/nueva/', registrar_asignatura, name='registrar_asignatura'),

    path('coordinador/asignaturas/<int:asignatura_id>/editar/',editar_asignatura, name='editar_asignatura'),


]



