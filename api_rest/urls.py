from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, GroupViewSet, PacienteViewSet, MedicoViewSet,
    CitaViewSet, MetricaPacienteViewSet, ConsultaViewSet, RecetaViewSet
)

# 1. Creamos el router de Django REST Framework
router = DefaultRouter()

# 2. Registramos los endpoints (URLs automáticas para CRUD)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'metricas', MetricaPacienteViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'recetas', RecetaViewSet)

# 3. Las URLs de la API deben usar el contenido del router
# ELIMINA la referencia a 'consultorio.urls' aquí para romper el bucle infinito
urlpatterns = [
    path('', include(router.urls)),
]