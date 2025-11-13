from django.db import models

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField(null=True, blank=True) # Campo añadido
    fecha_nacimiento = models.DateField(null=True, blank=True) # Campo añadido
    correo = models.EmailField(unique=True, null=True, blank=True) # Campo añadido
    telefono = models.CharField(max_length=20, null=True, blank=True) # Campo añadido
    genero = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        null=True,
        blank=True
    ) # Campo añadido
    direccion = models.TextField(blank=True, null=True) # Campo añadido

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

# Asegúrate de que Medico y Cita también estén aquí, como ya los tienes
class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_asignadas')
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=50, default='Pendiente')

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha} a las {self.hora}"

    class Meta:
        ordering = ['fecha', 'hora']
# --- NUEVO MODELO PARA EL HISTORIAL ---
class Historial(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historiales')
    fecha_creacion = models.DateField(auto_now_add=True) # Se establece automáticamente al crear
    otros_datos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Historial de {self.paciente.nombre} {self.paciente.apellido} - {self.fecha_creacion}"

    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
        ordering = ['-fecha_creacion'] # Ordenar por fecha de creación descendente

# --- NUEVO MODELO PARA RECETA ---
class Receta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas')
    nombre_medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    indicaciones = models.TextField(blank=True, null=True)
    fecha_emision = models.DateField(auto_now_add=True) # Para registrar cuándo se creó la receta

    def __str__(self):
        return f"Receta para {self.paciente.nombre} {self.paciente.apellido} - {self.nombre_medicamento}"

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ['-fecha_emision']
# --- NUEVO MODELO PARA METRICAS DE PACIENTE ---
class MetricaPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='metricas')
    fecha_medicion = models.DateField()
    talla = models.DecimalField(max_digits=4, decimal_places=2, help_text="Talla en metros (Ej: 1.75)") # Ej: 1.75 m
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kilogramos (Ej: 70.5)") # Ej: 70.5 kg
    otros_datos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Métrica de {self.paciente.nombre} {self.paciente.apellido} - {self.fecha_medicion}"

    class Meta:
        verbose_name = "Métrica del Paciente"
        verbose_name_plural = "Métricas del Paciente"
        ordering = ['-fecha_medicion']

# --- NUEVO MODELO PARA CONSULTA ---
class Consulta(models.Model):
    # Relación con el paciente al que pertenece esta consulta
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    # Relación con el médico que realizó la consulta. SET_NULL permite que la consulta persista
    # incluso si el médico es eliminado, estableciendo el campo en NULL.
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_dadas')
    # Fecha en que se realizó la consulta
    fecha_consulta = models.DateField()
    # Campo de texto para el diagnóstico principal de la consulta
    diagnostico = models.TextField()
    # Campo de texto opcional para observaciones adicionales
    observaciones = models.TextField(blank=True, null=True)


    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        # Ordena las consultas por fecha, las más recientes primero
        ordering = ['-fecha_consulta']

    def __str__(self):
        # Asegura que paciente y medico existan antes de acceder a sus atributos para evitar errores
        paciente_str = f"{self.paciente.nombre} {self.paciente.apellido}" if self.paciente else "Paciente Desconocido"
        medico_str = f"Dr. {self.medico.nombre} {self.medico.apellido}" if self.medico else "Médico Desconocido"
        return f"Consulta de {paciente_str} con {medico_str} el {self.fecha_consulta}"
