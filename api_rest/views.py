from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

# Importamos los modelos de la app volunta_de_dios
# Asegúrate de que Historial esté definido en tu models.py si decides usarlo en el futuro
from volunta_de_dios.models import (
    Paciente, Medico, Cita, MetricaPaciente, Consulta, Receta
)

# Importamos los serializadores exactamente como están nombrados en serializers.py
# Se corrigió el orden y se verificó que coincidan con la estructura del archivo anterior
from .serializers import (
    UserSerializer, 
    GroupSerializer, 
    MedicoSerializer,
    RecetaSerializer, 
    MetricaPacienteSerializer, 
    CitaSerializer,
    ConsultaSerializer, 
    PacienteSerializer
)

# --- VISTAS DE ADMINISTRACIÓN DE USUARIOS ---

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar usuarios.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar grupos/roles.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- VISTAS DEL NEGOCIO MÉDICO (CRUD Completo) ---

class PacienteViewSet(viewsets.ModelViewSet):
    """
    Maneja la lógica de pacientes y sus relaciones anidadas (citas/recetas).
    """
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [permissions.IsAuthenticated]

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

class MetricaPacienteViewSet(viewsets.ModelViewSet):
    queryset = MetricaPaciente.objects.all()
    serializer_class = MetricaPacienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer
    permission_classes = [permissions.IsAuthenticated]