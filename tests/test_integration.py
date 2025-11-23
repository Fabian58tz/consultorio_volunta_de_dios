from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
# CORRECCIÓN: Importación absoluta usando el nombre de la aplicación
from volunta_de_dios.models import Paciente 

# --- PRUEBA UNITARIA PARA LOGIN ---
class LoginTests(TestCase):
    def setUp(self):
        # Configuración inicial: crear un usuario para las pruebas
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)
        # La URL de login la sacamos de urls.py (name='login_view')
        self.login_url = reverse('login_page')
        # La URL de éxito (página principal) la sacamos de urls.py (name='pagina_principal')
        self.success_url = reverse('paguina_principal')

    def test_login_get(self):
        """La vista de login debe cargar correctamente con una solicitud GET."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_successful_login(self):
        """Un login con credenciales válidas debe redirigir a la página principal."""
        response = self.client.post(self.login_url, self.user_data, follow=True)
        # Verifica la redirección y el código de estado final
        self.assertEqual(response.status_code, 200)
        # Verifica que haya sido redirigido a la página principal después del login
        self.assertRedirects(response, self.success_url)
        # Opcional: Verifica que el usuario haya sido autenticado
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_invalid_login(self):
        """Un login con credenciales inválidas debe mostrar un error y no autenticar."""
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_data, follow=True)
        # Debe permanecer en la misma página de login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # Verifica que el usuario NO haya sido autenticado
        self.assertFalse('_auth_user_id' in self.client.session)


# --- PRUEBA UNITARIA PARA AGREGAR PACIENTE ---
class AgregarPacienteTests(TestCase):
    def setUp(self):
        # Configuración: Necesitas un usuario autenticado para acceder a la vista de agregar paciente
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='password')
        # Iniciar sesión al cliente
        self.client.login(username='admin', password='password')
        
        # La URL para agregar paciente la sacamos de urls.py (name='agregar_pacientes')
        self.agregar_url = reverse('agregar_pacientes')
        # La URL de éxito (tabla de pacientes) la sacamos de urls.py (name='tabla_pacientes')
        self.success_url = reverse('tabla_pacientes')
        
        # Datos válidos de prueba para crear un paciente (debe coincidir con fields en PacienteForm)
        # Asegúrate que el campo 'genero' use el valor correcto ('M', 'F', 'O', 'Otro')
        self.valid_data = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'edad': 30,
            'fecha_nacimiento': '1995-01-01', # Formato YYYY-MM-DD
            'correo': 'juan.perez@example.com',
            'telefono': '555-1234',
            'genero': 'M', 
            'direccion': 'Calle Falsa 123'
        }

    def test_view_accessible(self):
        """La vista de agregar paciente debe ser accesible para un usuario autenticado."""
        response = self.client.get(self.agregar_url)
        self.assertEqual(response.status_code, 200)
        # El template usado es 'agregar_pacientes.html' (basado en la URL)
        self.assertTemplateUsed(response, 'agregar_pacientes.html')

    def test_successful_patient_creation(self):
        """Un POST con datos válidos debe crear un paciente y redirigir."""
        initial_count = Paciente.objects.count()
        response = self.client.post(self.agregar_url, self.valid_data, follow=True)
        
        # Debe haber un nuevo paciente en la base de datos
        self.assertEqual(Paciente.objects.count(), initial_count + 1)
        
        # Debe redirigir a la URL de la tabla de pacientes
        self.assertRedirects(response, self.success_url)
        
        # Verificar que los datos del paciente se hayan guardado correctamente
        paciente = Paciente.objects.latest('id')
        self.assertEqual(paciente.nombre, 'Juan')
        self.assertEqual(paciente.apellido, 'Perez')

    def test_invalid_patient_creation(self):
        """Un POST con datos inválidos (ej. campo requerido faltante) no debe crear el paciente."""
        initial_count = Paciente.objects.count()
        # Datos inválidos: falta el nombre
        invalid_data = self.valid_data.copy()
        del invalid_data['nombre'] 
        
        response = self.client.post(self.agregar_url, invalid_data)
        
        # El conteo de pacientes no debe cambiar
        self.assertEqual(Paciente.objects.count(), initial_count)
        # La respuesta debe ser 200 (se renderiza la misma página con errores)
        self.assertEqual(response.status_code, 200)
        # Debe contener los errores del formulario
        self.assertContains(response, 'This field is required.')

    def test_unauthenticated_access(self):
        """Un usuario no autenticado debe ser redirigido al intentar acceder."""
        self.client.logout() # Asegurar que no está logeado
        response = self.client.get(self.agregar_url, follow=False)
        # Esperamos una redirección (normalmente a la página de login)
        self.assertEqual(response.status_code, 302)
        # Opcional: Verificar a dónde redirige (puedes descomentar esto si conoces la URL exacta de redirección de login)
        # self.assertRedirects(response, '/login/?next=/pacientes/agregar/')

# 🚀 --- PRUEBA DE INTEGRACIÓN ---
class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'integration_user',
            'password': 'safe_password'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # URLs necesarias
        self.login_url = reverse('login_page')
        self.agregar_url = reverse('agregar_pacientes')
        self.tabla_url = reverse('tabla_pacientes')
        
        # Datos de un nuevo paciente
        self.new_patient_data = {
            'nombre': 'Maria',
            'apellido': 'Gomez',
            'edad': 25,
            'fecha_nacimiento': '2000-10-20',
            'correo': 'maria.gomez@test.com',
            'telefono': '999-8888',
            'genero': 'F', 
            'direccion': 'Avenida Siempre Viva 742'
        }

    def test_full_patient_workflow(self):
        """Prueba el flujo completo: Login -> Agregar Paciente -> Ver en la Tabla."""
        
        # 1. Ejecutar Login Exitoso
        # El follow=True maneja la redirección a la página principal después del login
        login_response = self.client.post(self.login_url, self.user_data, follow=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)
        
        # 2. Verificar que no hay pacientes antes de la creación
        initial_count = Paciente.objects.count()
        self.assertEqual(initial_count, 0)
        
        # 3. Agregar un nuevo Paciente (POST)
        # Debe redirigir automáticamente a la tabla de pacientes (success_url)
        add_response = self.client.post(self.agregar_url, self.new_patient_data, follow=True)
        
        # 4. Verificar la creación y la redirección
        self.assertEqual(Paciente.objects.count(), initial_count + 1)
        self.assertRedirects(add_response, self.tabla_url)
        
        # 5. Verificar el contenido en la página de la Tabla (Paso de Integración Clave)
        # El response final (add_response) es la página de la tabla de pacientes.
        self.assertEqual(add_response.status_code, 200)
        self.assertTemplateUsed(add_response, 'tabla_pacientes.html') 
        
        # Verificar que el nombre del paciente recién creado se muestre en la tabla
        self.assertContains(add_response, self.new_patient_data['nombre'])
        self.assertContains(add_response, self.new_patient_data['apellido'])
        
        # 6. Verificación final de la base de datos
        paciente_db = Paciente.objects.latest('id')
        self.assertEqual(paciente_db.nombre, 'Maria')