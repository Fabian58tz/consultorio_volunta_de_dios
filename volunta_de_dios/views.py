from django.shortcuts import render, redirect, get_object_or_404, redirect
from django. http import HttpResponse
from .forms import PacienteForm, CitaForm, HistorialForm, RecetaForm, MetricaPacienteForm, ConsultaForm,MedicoForm
from .models import Paciente, Cita,Medico , Cita, Historial, Receta, MetricaPaciente,Consulta
from django.contrib.auth.forms import AuthenticationForm # Importa el formulario de autenticación
from django.contrib.auth import login, authenticate, logout # Importa funciones de autenticación
from django.contrib import messages # Para mostrar mensajes (opcional, pero recomendado para errores)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def holamundo(request):
    return HttpResponse("<h1>Hola mundo, aprendiendo a programar en python</h1>")

@login_required
def paguina_principal(request):
    return render(request,'paguina_principal.html')

@login_required
def agregar_historial(request):
    if request.method == 'POST':
        form = HistorialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_historial')
    else:
        form = HistorialForm()
    return render(request, 'agregar_historial.html', {'form': form})
@login_required
def tabla_citas(request):
    citas = Cita.objects.all()
    return render(request, 'tabla_citas.html', {'citas': citas})

@login_required
def agregar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_citas') # Redirige a la tabla de citas
    else:
        form = CitaForm()
    return render(request, 'agregar_cita.html', {'form': form})

@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('tabla_citas') # Redirige a la tabla de citas después de guardar
    else:
        form = CitaForm(instance=cita)
    return render(request, 'editar_cita.html', {'form': form, 'cita': cita})

@login_required
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        return redirect('tabla_citas') # Redirige a la tabla de citas después de eliminar
    return render(request, 'confirmar_eliminar_cita.html', {'cita': cita}) # Nueva plantilla para confirmar

@login_required
def agregar_pacientes(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_pacientes') 
    else: 
        form = PacienteForm()
    return render(request, 'agregar_pacientes.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') # AuthenticationForm usa 'username'
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige a la página principal si el login es exitoso
                return redirect('paguina_principal')
            else:
                # Mensaje de error si las credenciales son inválidas
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            # Mensajes de error del formulario (ej. campos vacíos)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AuthenticationForm()
    
    # Renderiza la plantilla de login con el formulario
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login_page') # Redirige a la página de login después de cerrar sesión

@login_required
def metrica_paciente(request):
    return redirect('agregar_metrica')

@login_required
def tabla_de_recetas_de_pacientes(request):
    recetas = Receta.objects.all()
    return render(request, 'tabla_de_recetas_de_pacientes.html', {'recetas': recetas})

@login_required
def agregar_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_de_recetas_de_pacientes')
    else:
        form = RecetaForm()
    # Usa la plantilla existente 'recetas_de_pacientes.html' para el formulario
    return render(request, 'recetas_de_pacientes.html', {'form': form})

@login_required
def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('tabla_de_recetas_de_pacientes')
    else:
        form = RecetaForm(instance=receta)
    # Crea una plantilla específica para editar o reutiliza la de agregar si la adaptas
    return render(request, 'editar_receta.html', {'form': form, 'receta': receta})

@login_required
def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        receta.delete()
        return redirect('tabla_de_recetas_de_pacientes')
    return render(request, 'confirmar_eliminar_receta.html', {'receta': receta})

@login_required
def tabla_pacientes(request):
    
    pacientes = Paciente.objects.all() 
    
    return render(request, 'tabla_pacientes.html', {'pacientes': pacientes})

@login_required
def editar_paciente(request, pk):
    
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save() 
            return redirect('tabla_pacientes') 
    else:
        
        form = PacienteForm(instance=paciente)

    return render(request, 'editar_pacientes.html', {'form': form, 'paciente': paciente})

# --- VISTA PARA ELIMINAR PACIENTE ---
@login_required
def eliminar_paciente(request, pk):
    
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        paciente.delete() 
        return redirect('tabla_pacientes') 

    
    return render(request, 'confirmar_eliminar_paciente.html', {'paciente': paciente})

@login_required
def consulta_pacientes(request):
    return render(request,'consulta_pacientes.html')

@login_required
def recetas_de_pacientes(request):
    
    return render(request, 'recetas_de_pacientes.html')

@login_required
def tabla_historial(request):
    historiales = Historial.objects.all()
    return render(request, 'tabla_historial.html', {'historiales': historiales})

@login_required
def agregar_historial(request):
    if request.method == 'POST':
        form = HistorialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_historial')
    else:
        form = HistorialForm()
    return render(request, 'agregar_historial.html', {'form': form})

@login_required
def editar_historial(request, pk):
    historial = get_object_or_404(Historial, pk=pk)
    if request.method == 'POST':
        form = HistorialForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('tabla_historial')
    else:
        form = HistorialForm(instance=historial)
    return render(request, 'editar_historial.html', {'form': form, 'historial': historial})

@login_required
def eliminar_historial(request, pk):
    historial = get_object_or_404(Historial, pk=pk)
    if request.method == 'POST':
        historial.delete()
        return redirect('tabla_historial')
    return render(request, 'confirmar_eliminar_historial.html', {'historial': historial})

@login_required
def tabla_metrica(request):
   metricas = MetricaPaciente.objects.all()
   return render(request, 'tabla_metrica.html', {'metricas': metricas})

@login_required
def agregar_metrica(request):
    if request.method == 'POST':
        form = MetricaPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_metrica')
    else:
        form = MetricaPacienteForm()
    # Usa la plantilla 'metrica_paciente.html' para el formulario
    return render(request, 'metrica_paciente.html', {'form': form})

@login_required
def editar_metrica(request, pk):
    metrica = get_object_or_404(MetricaPaciente, pk=pk)
    if request.method == 'POST':
        form = MetricaPacienteForm(request.POST, instance=metrica)
        if form.is_valid():
            form.save()
            return redirect('tabla_metrica')
    else:
        form = MetricaPacienteForm(instance=metrica)
    # Reutiliza la plantilla de agregar para editar, pasando el objeto 'metrica'
    return render(request, 'metrica_paciente.html', {'form': form, 'metrica': metrica})

@login_required
def eliminar_metrica(request, pk):
    metrica = get_object_or_404(MetricaPaciente, pk=pk)
    if request.method == 'POST':
        metrica.delete()
        return redirect('tabla_metrica')
    return render(request, 'confirmar_eliminar_metrica.html', {'metrica': metrica})

@login_required
def tabla_consulta(request):
    consultas = Consulta.objects.all().order_by('-fecha_consulta')
    # Renderiza 'tabla_consulta.html' (singular)
    return render(request, 'tabla_consulta.html', {'consultas': consultas})

@login_required
def agregar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a 'tabla_consulta' (singular)
            return redirect('tabla_consulta')
    else:
        form = ConsultaForm()
    return render(request, 'agregar_consulta.html', {'form': form})

@login_required
def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            # Redirige a 'tabla_consulta' (singular)
            return redirect('tabla_consulta')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'editar_consulta.html', {'form': form, 'consulta': consulta})

@login_required
def eliminar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        # Redirige a 'tabla_consulta' (singular)
        return redirect('tabla_consulta')
    return render(request, 'confirmar_eliminar_consulta.html', {'consulta': consulta})

@login_required
def tabla_medicos(request):
    medicos = Medico.objects.all().order_by('apellido', 'nombre') # Ordena por apellido, luego nombre
    return render(request, 'tabla_medicos.html', {'medicos': medicos})

@login_required
def agregar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_medicos') # Redirige a la tabla de médicos
    else:
        form = MedicoForm()
    return render(request, 'agregar_medico.html', {'form': form})

@login_required
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('tabla_medicos') # Redirige a la tabla de médicos después de guardar
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'editar_medicos.html', {'form': form, 'medico': medico})

@login_required
def eliminar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        medico.delete()
        return redirect('tabla_medicos') # Redirige a la tabla de médicos después de eliminar
    # Puedes crear una plantilla de confirmación específica si lo deseas
    return render(request, 'confirmar_eliminar_medico.html', {'medico': medico})

def registro_usuario_view(request):
    """
    Vista para manejar el registro de nuevos usuarios en el sistema.
    Asume que la persona que se registra es un 'Paciente' por defecto
    o un usuario sin privilegios de administrador.
    """
    if request.method == 'POST':
        # 1. Crear una instancia del formulario con los datos recibidos por POST
        form = UserCreationForm(request.POST) 
        
        if form.is_valid():
            # 2. Guardar el nuevo usuario en la base de datos
            user = form.save()
            
            # NOTA: Aquí podrías añadir lógica adicional:
            # - Asignar roles: user.groups.add(Group.objects.get(name='Paciente'))
            # - Crear un perfil de paciente asociado al nuevo usuario
            
            # 3. Redirigir al usuario a la página de login o al home
            return redirect('login_page')  # Asegúrate que 'login_page' es el nombre correcto de tu URL de login
    else:
        # 4. Si la petición es GET, mostrar el formulario vacío
        form = UserCreationForm()

    # Pasar el formulario a la plantilla
    return render(request, 'registro_usuario.html', {'form': form})