from django import forms
from .models import Paciente,Medico, Cita, Historial, Receta, MetricaPaciente, Consulta 

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'edad', 'fecha_nacimiento', 'correo', 'telefono', 'genero', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo', 'estado']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'select2-paciente'}), # <<< CAMBIO AQUÍ
            'medico': forms.Select(attrs={'class': 'select2-medico'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            
            
        }
# --- NUEVO FORMULARIO PARA EL HISTORIAL ---
class HistorialForm(forms.ModelForm):
    # Aquí puedes personalizar los campos si es necesario.
    # Por ejemplo, para que el campo de paciente sea un select.
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccione un paciente")

    class Meta:
        model = Historial
        fields = ['paciente', 'otros_datos'] # 'fecha_creacion' es auto_now_add, no se incluye en el formulario
        widgets = {
            'otros_datos': forms.Textarea(attrs={'rows': 10}), # Ajusta las filas del textarea
            'paciente': forms.Select(attrs={'class': 'select2-paciente'}), # <<< CAMBIO AQUÍ
        }
# --- NUEVO FORMULARIO PARA RECETA ---
class RecetaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccione un paciente")

    class Meta:
        model = Receta
        fields = ['paciente', 'nombre_medicamento', 'dosis', 'frecuencia', 'indicaciones']
        widgets = {
            'indicaciones': forms.Textarea(attrs={'rows': 5}), # Ajusta las filas del textarea
            'paciente': forms.Select(attrs={'class': 'select2-paciente'}), # <<< CAMBIO AQUÍ
        }
# --- NUEVO FORMULARIO PARA METRICAS DE PACIENTE ---
class MetricaPacienteForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccione un paciente")

    class Meta:
        model = MetricaPaciente
        fields = ['paciente', 'fecha_medicion', 'talla', 'peso', 'otros_datos']
        widgets = {
            'fecha_medicion': forms.DateInput(attrs={'type': 'date'}),
            'otros_datos': forms.Textarea(attrs={'rows': 5}),
            'paciente': forms.Select(attrs={'class': 'select2-paciente'}), # <<< CAMBIO AQUÍ
        }
        
# --- FORMULARIO PARA CONSULTA ---
class ConsultaForm(forms.ModelForm):
    # Usamos ModelChoiceField para seleccionar el paciente y el médico de los modelos existentes.
    # Esto creará un campo <select> en el HTML.
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccione un paciente", label="Paciente")
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(), empty_label="Seleccione un médico", label="Médico")

    class Meta:
        model = Consulta
        # Los campos que se mostrarán en el formulario para el modelo Consulta
        fields = ['paciente', 'medico', 'fecha_consulta', 'diagnostico', 'observaciones']
        widgets = {
            # Establece el tipo de input como 'date' para el campo de fecha
            'fecha_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Define el número de filas para los campos de texto grandes
            'diagnostico': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }
        # Etiquetas personalizadas para los campos del formulario
        labels = {
            'fecha_consulta': 'Fecha de consulta',
            'diagnostico': 'Diagnóstico',
            'observaciones': 'Observaciones',
        }

# --- FORMULARIO PARA MÉDICO (Gestiona un solo objeto Médico) ---
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'apellido', 'especialidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Médico',
            'apellido': 'Apellido del Médico',
            'especialidad': 'Especialidad',
        }