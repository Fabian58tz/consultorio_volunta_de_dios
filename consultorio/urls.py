
from django.contrib import admin
from django.urls import path
from volunta_de_dios import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('paguina_principal/', views.paguina_principal, name='paguina_principal'),
    path('agregar_historial/', views.agregar_historial, name='agregar_historial'),
    path('tabla_citas/', views.tabla_citas, name='tabla_citas'),
    path('agregar_pacientes/', views.agregar_pacientes, name='agregar_pacientes'),
    path('login/', views.login_view, name='login_page'),
    path('metrica_paciente/', views.metrica_paciente, name='metrica_paciente'),
     path('tabla_de_recetas_de_pacientes/', views.tabla_de_recetas_de_pacientes, name='tabla_de_recetas_de_pacientes'),
     path('tabla_pacientes/', views.tabla_pacientes, name='tabla_pacientes'),
      path('consulta_pacientes/', views.consulta_pacientes, name='consulta_pacientes'),
      path('recetas_de_pacientes/', views.recetas_de_pacientes, name='recetas_de_pacientes'),
        path('tabla_historial/', views.tabla_historial, name='tabla_historial'),
        path('tabla_metrica/', views.tabla_metrica, name='tabla_metrica'),
         path('editar_paciente/<int:pk>/', views.editar_paciente, name='editar_paciente'), # <int:pk> captura el ID
    path('eliminar_paciente/<int:pk>/', views.eliminar_paciente, name='eliminar_paciente'), # <int:pk> captura el ID
     path('agregar_cita/', views.agregar_cita, name='agregar_cita'),
    path('editar_cita/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('eliminar_cita/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),
     path('agregar_historial/', views.agregar_historial, name='agregar_historial'),
    path('editar_historial/<int:pk>/', views.editar_historial, name='editar_historial'),
    path('eliminar_historial/<int:pk>/', views.eliminar_historial, name='eliminar_historial'),
    path('agregar_receta/', views.agregar_receta, name='agregar_receta'),
    path('editar_receta/<int:pk>/', views.editar_receta, name='editar_receta'),
    path('eliminar_receta/<int:pk>/', views.eliminar_receta, name='eliminar_receta'),
    path('agregar_metrica/', views.agregar_metrica, name='agregar_metrica'),
    path('editar_metrica/<int:pk>/', views.editar_metrica, name='editar_metrica'),
    path('eliminar_metrica/<int:pk>/', views.eliminar_metrica, name='eliminar_metrica'),
    path('tabla_consulta/', views.tabla_consulta, name='tabla_consulta'), # ¡AHORA ES SINGULAR!
    path('agregar_consulta/', views.agregar_consulta, name='agregar_consulta'),
    path('editar_consulta/<int:pk>/', views.editar_consulta, name='editar_consulta'),
    path('eliminar_consulta/<int:pk>/', views.eliminar_consulta, name='eliminar_consulta'),

path('tabla_medicos/', views.tabla_medicos, name='tabla_medicos'),
    path('agregar_medico/', views.agregar_medico, name='agregar_medico'),
    path('editar_medico/<int:pk>/', views.editar_medico, name='editar_medico'),
    path('eliminar_medico/<int:pk>/', views.eliminar_medico, name='eliminar_medico'),
    # URL para cerrar sesión
    path('logout/', views.logout_view, name='logout_page'),
path('registro/', views.registro_usuario_view, name='registro_usuario'),
]

