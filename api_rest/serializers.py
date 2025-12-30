from django.contrib.auth.models import User, Group
from rest_framework import serializers

# CORRECCIÓN DE IMPORTACIÓN: 
# En image_c316ed.png se veía 'consultorio.models'. 
# Debe ser 'volunta_de_dios.models' para encontrar los modelos correctamente.
from volunta_de_dios.models import (
    Paciente, Medico, Cita, MetricaPaciente, 
    Consulta, Historial, Receta
) 

# --- SERIALIZADORES DE SISTEMA ---

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# --- SERIALIZADORES DE NEGOCIO ---

class MedicoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medico
        fields = ['url', 'id', 'nombre', 'apellido', 'especialidad']

class RecetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Receta
        # Ajustado según campos en image_cd012c.png
        fields = ['url', 'paciente', 'nombre_medicamento', 'dosis', 'frecuencia', 'indicaciones', 'fecha_emision']

class MetricaPacienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricaPaciente
        # Se corrigió 'presion_arterial' por 'otros_datos' o campos existentes en image_cd014d.png
        fields = ['url', 'paciente', 'fecha_medicion', 'talla', 'peso', 'otros_datos']

class CitaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cita
        # Basado en campos de image_cd0109.png
        fields = ['url', 'paciente', 'medico', 'fecha', 'hora', 'motivo', 'estado']

class ConsultaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consulta
        # Basado en campos de image_cd014d.png
        fields = ['url', 'paciente', 'medico', 'fecha_consulta', 'diagnostico', 'observaciones']

# --- SERIALIZADOR MAESTRO (PACIENTE) ---

class PacienteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Relaciones anidadas usando los related_name del modelo.
    """
    # source='citas' definido en image_cd0109.png
    citas_paciente = CitaSerializer(many=True, read_only=True, source='citas')
    # source='recetas' definido en image_cd012c.png
    recetas_paciente = RecetaSerializer(many=True, read_only=True, source='recetas')

    class Meta:
        model = Paciente
        fields = [
            'url', 'id', 'nombre', 'apellido', 'edad', 
            'fecha_nacimiento', 'correo', 'telefono', 
            'genero', 'direccion', 'citas_paciente', 'recetas_paciente'
        ]