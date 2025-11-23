from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
# Asegúrate de que los modelos Paciente, Medico, Cita, Consulta estén disponibles
from volunta_de_dios.models import Paciente, Medico, Cita, Consulta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time # Importamos time para un pequeño sleep de seguridad

# La variable global SUBMIT_XPATH no es necesaria si usamos locators más específicos
# SUBMIT_XPATH = '//button[@type="submit"]'

# --- PRUEBA END-TO-END (E2E) AVANZADA Y ROBUSTA ---
class ConsultorioFullWorkflowTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Inicializa el driver de Selenium (Asegúrate de tener ChromeDriver instalado y en PATH)
        try:
            # Usar 'options' para configurar el driver
            options = webdriver.ChromeOptions()
            # Opciones comunes para robustez en entornos CI/Headless
            # options.add_argument('--headless') # Descomentar si se ejecuta en CI sin interfaz gráfica
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev_shm-usage')
            cls.selenium = webdriver.Chrome(options=options)
        except Exception:
            # En caso de error, levanta la excepción para indicar que el setup falló
            raise
        
        # Maximizar la ventana ayuda con elementos ocultos/interceptados
        cls.selenium.maximize_window()
        # Tiempo de espera implícito general
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Crear un usuario administrador para las pruebas
        self.user_data = {'username': 'admin_e2e', 'password': 'admin_password'}
        self.user = User.objects.create_user(**self.user_data)
        
        # Datos de prueba para las entidades
        self.medico_data = {'nombre': 'Dr. Andres', 'apellido': 'Gomez', 'especialidad': 'General'}
        self.paciente_data = {
            'nombre': 'Luisa', 'apellido': 'Fernandez', 'edad': 35, 'genero': 'F',
            'fecha_nacimiento': '1990-05-10', 'correo': 'luisa@test.com', 
            'telefono': '123-4567', 'direccion': 'Av. Central 404'
        }
        # Datos de Cita y Consulta
        # Formato de fecha corregido a 'dd/mm/yyyy' (20/01/2026) 
        self.cita_data = {'fecha': '20/01/2026', 'hora': '10:30', 'motivo': 'Chequeo anual de rutina'} 
        # Ajustamos el nombre de campo: 'tratamiento' pasa a ser 'observaciones' en la UI
        # Vamos a usar 'motivo' de la consulta como parte del diagnóstico para simplificar.
        self.consulta_data = {'motivo': 'Dolor de cabeza cronico', 'diagnostico': 'Migraña por estrés', 'tratamiento': 'Paracetamol y reposo'}
        
        # URLs (usando reverse en setUp es más limpio)
        self.login_url = self.live_server_url + reverse('login_page')
        self.add_medico_url = self.live_server_url + reverse('agregar_medico')
        self.tabla_medicos_url = self.live_server_url + reverse('tabla_medicos')
        self.add_paciente_url = self.live_server_url + reverse('agregar_pacientes')
        self.tabla_pacientes_url = self.live_server_url + reverse('tabla_pacientes')
        self.add_cita_url = self.live_server_url + reverse('agregar_cita')
        self.tabla_citas_url = self.live_server_url + reverse('tabla_citas')
        self.add_consulta_url = self.live_server_url + reverse('agregar_consulta')
        self.tabla_consultas_url = self.live_server_url + reverse('tabla_consulta')
    
    def robust_click(self, locator):
        """
        Espera que el elemento sea visible y utiliza JavaScript para clickearlo.
        Esto previene la mayoría de los errores de ElementClickInterceptedException.
        """
        s = self.selenium
        # Aumentar la espera en los clics para mayor robustez
        wait = WebDriverWait(s, 15) 
        try:
            # Primero esperamos que el elemento esté visible
            element = wait.until(EC.visibility_of_element_located(locator))
            # Luego esperamos que sea clickeable
            element = wait.until(EC.element_to_be_clickable(locator))
            # Usar click de JS para máxima robustez en submit
            s.execute_script("arguments[0].click();", element)
        except TimeoutException as e:
            # Añadimos más información de diagnóstico aquí
            print(f"Error: Timeout al intentar clickear el elemento con locator {locator}")
            print(f"URL actual durante el fallo: {s.current_url}")
            # Si el timeout ocurre y estamos en la URL de agregar consulta,
            # forzamos un diagnóstico más claro.
            if s.current_url.endswith('/agregar_consulta/'):
                print("El botón 'Guardar' no se hizo clickeable/visible. Posible fallo de validación de formulario.")
            raise e
        except StaleElementReferenceException:
            # Si el elemento se vuelve 'stale' (la página cambió), no hacemos nada
            # porque asumimos que la redirección comenzó.
            print(f"Advertencia: El elemento {locator} se volvió 'stale'. Asumiendo redirección exitosa.")


    def fill_login_form(self):
        """Función auxiliar para iniciar sesión."""
        s = self.selenium
        s.find_element(By.NAME, 'username').send_keys(self.user_data['username'])
        s.find_element(By.NAME, 'password').send_keys(self.user_data['password'])
        
        # Usar el robust_click para el botón de inicio de sesión
        self.robust_click((By.XPATH, '//button[@type="submit"]'))
        
        # Esperar la redirección
        WebDriverWait(s, 15).until(EC.url_changes(self.login_url))

    def test_e2e_full_clinic_workflow(self):
        """Simula el flujo completo: Login -> Crear Médico -> Crear Paciente -> Crear Cita -> Crear Consulta -> Verificar."""
        s = self.selenium
        # Tiempo de espera aumentado a 15 segundos para manejar latencia del servidor de prueba
        wait = WebDriverWait(s, 15) 

        # --- 1. LOGIN ---
        s.get(self.login_url)
        self.assertIn('Inicio de Sesión', s.title) 
        self.fill_login_form()
        
        # Después del login, esperar a que el menú lateral cargue 
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'MENU DE OPCIONES')]")))


        # --- 2. CREAR MÉDICO ---
        s.get(self.add_medico_url)
        
        # Rellenar formulario
        s.find_element(By.NAME, 'nombre').send_keys(self.medico_data['nombre'])
        s.find_element(By.NAME, 'apellido').send_keys(self.medico_data['apellido'])
        s.find_element(By.NAME, 'especialidad').send_keys(self.medico_data['especialidad'])
        
        # Clickear el botón "Guardar" para Médico de manera robusta
        self.robust_click((By.XPATH, '//button[text()="Guardar"]'))
        
        # Esperar redirección a la tabla de médicos para confirmar el POST
        wait.until(EC.url_to_be(self.tabla_medicos_url)) 
        
        # Verificar que el médico fue creado en la DB
        self.assertEqual(Medico.objects.count(), 1)
        medico = Medico.objects.latest('id')
        
        # --- 3. CREAR PACIENTE ---
        s.get(self.add_paciente_url)
        
        # Rellenar formulario
        s.find_element(By.NAME, 'nombre').send_keys(self.paciente_data['nombre'])
        s.find_element(By.NAME, 'apellido').send_keys(self.paciente_data['apellido'])
        s.find_element(By.NAME, 'edad').send_keys(str(self.paciente_data['edad']))
        
        # TRUCO DE ROBUSTEZ: Limpiar y enviar la fecha para evitar problemas con date pickers
        fecha_input = s.find_element(By.NAME, 'fecha_nacimiento')
        fecha_input.clear()
        fecha_input.send_keys(self.paciente_data['fecha_nacimiento'])
        
        s.find_element(By.NAME, 'correo').send_keys(self.paciente_data['correo'])
        s.find_element(By.NAME, 'telefono').send_keys(self.paciente_data['telefono'])
        
        # Seleccionar género
        Select(s.find_element(By.NAME, 'genero')).select_by_value(self.paciente_data['genero'])
        s.find_element(By.NAME, 'direccion').send_keys(self.paciente_data['direccion'])
        
        # Clickear el botón "Guardar" para Paciente de manera robusta
        self.robust_click((By.XPATH, '//button[text()="Guardar"]'))
        
        # Esperar redirección a la tabla de pacientes y verificar creación
        wait.until(EC.url_to_be(self.tabla_pacientes_url)) 
        self.assertEqual(Paciente.objects.count(), 1)
        paciente = Paciente.objects.latest('id')
        
        # --- 4. CREAR CITA (Asignar Médico y Paciente) ---
        s.get(self.add_cita_url)
        
        # Esperar y seleccionar Paciente
        paciente_select = wait.until(EC.presence_of_element_located((By.NAME, 'paciente')))
        Select(paciente_select).select_by_value(str(paciente.pk))
        
        # Esperar y seleccionar Médico
        medico_select = wait.until(EC.presence_of_element_located((By.NAME, 'medico')))
        Select(medico_select).select_by_value(str(medico.pk))
        
        # Limpiar y enviar la fecha (Formato dd/mm/yyyy)
        fecha_cita_input = s.find_element(By.NAME, 'fecha')
        fecha_cita_input.clear()
        fecha_cita_input.send_keys(self.cita_data['fecha'])
        
        s.find_element(By.NAME, 'hora').send_keys(self.cita_data['hora'])

        # Rellenar el campo 'motivo' de la Cita 
        s.find_element(By.NAME, 'motivo').send_keys(self.cita_data['motivo'])
        
        # El selector del botón de Cita es "Guardar Cita"
        submit_locator = (By.XPATH, '//button[text()="Guardar Cita"]')
        
        # Hacemos el click robusto y esperamos la redirección.
        self.robust_click(submit_locator)
        
        # Esperar redirección a la tabla de citas y verificar creación
        try:
            wait.until(EC.url_to_be(self.tabla_citas_url))
        except TimeoutException:
            # Si hay timeout, imprimimos la URL y el source para diagnóstico avanzado.
            print("\n--- DIAGNÓSTICO AVANZADO DE TIMEOUT EN CREACIÓN DE CITA ---")
            print(f"URL actual: {s.current_url}")
            print("Contenido de la página (busque mensajes de error):")
            # Buscamos un mensaje de error común de Django/Bootstrap
            if "alert-danger" in s.page_source or "This field is required" in s.page_source:
                print("¡Se detectaron posibles errores de validación en la página del formulario!")
            else:
                print("No se detectaron errores de validación comunes. El problema podría ser la redirección.")
            print("---------------------------------------------------\n")
            raise 

        self.assertEqual(Cita.objects.count(), 1)
        cita = Cita.objects.latest('id')
        
        # --- 5. CREAR CONSULTA ---
        s.get(self.add_consulta_url)
        
        # Aumentamos el sleep para dar tiempo a cargar modelos/JS de validación
        time.sleep(1.5) 

        # Esperar y seleccionar Paciente
        paciente_select_consulta = wait.until(EC.presence_of_element_located((By.NAME, 'paciente')))
        # Esperar explícitamente a que al menos una opción esté disponible (el PK del paciente)
        wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@name='paciente']/option[@value='{paciente.pk}']")))
        Select(paciente_select_consulta).select_by_value(str(paciente.pk))
        
        # Esperar y seleccionar Médico
        medico_select_consulta = wait.until(EC.presence_of_element_located((By.NAME, 'medico')))
        # Esperar explícitamente a que al menos una opción esté disponible (el PK del médico)
        wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@name='medico']/option[@value='{medico.pk}']")))
        Select(medico_select_consulta).select_by_value(str(medico.pk))
        
        # Limpiar y enviar la fecha de la consulta
        fecha_consulta_input = s.find_element(By.NAME, 'fecha_consulta') 
        fecha_consulta_input.clear()
        fecha_consulta_input.send_keys(self.cita_data['fecha']) 
        
        # Rellenamos Diagnóstico y Observaciones (que sí existen)
        s.find_element(By.NAME, 'diagnostico').send_keys(self.consulta_data['diagnostico'])
        s.find_element(By.NAME, 'observaciones').send_keys(self.consulta_data['tratamiento']) 
        
        
        # ********** Clic y Espera de Redirección (CORRECCIÓN CRÍTICA DEL SELECTOR) **********
        # El botón de la Consulta tiene type="submit", pero el texto "Guardar" está fuera.
        # Usamos el selector más confiable: el botón de submit dentro del contenedor de acciones.
        consulta_submit_locator = (By.XPATH, '//div[@class="form-actions"]//button[@type="submit"]')
        
        # Buscamos el elemento y forzamos el clic JS.
        try:
            button = wait.until(EC.presence_of_element_located(consulta_submit_locator))
            # Usamos click de JS directo.
            s.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            print(f"Error: No se encontró el botón con locator {consulta_submit_locator}")
            raise # Relanzamos si ni siquiera existe.
        except TimeoutException as e:
            print(f"Error: Timeout al encontrar el botón con locator {consulta_submit_locator}. URL: {s.current_url}")
            raise e
        
        # Esperar redirección a la tabla de consultas y verificar creación
        # Si el clic fue exitoso, esta línea debe funcionar.
        try:
            wait.until(EC.url_to_be(self.tabla_consultas_url))
        except TimeoutException as e:
            # Si el clic falló o la redirección no ocurrió, reportamos el fallo de la prueba.
            print("\n[FALLO CRÍTICO] El clic en 'Guardar' no redirigió. Posible fallo de validación del formulario de Consulta.")
            print(f"URL actual: {s.current_url}")
            raise e
            
        self.assertEqual(Consulta.objects.count(), 1)

        # --- 6. VERIFICACIÓN FINAL EN LA TABLA DE CONSULTAS ---
        # Verificar que el diagnóstico del paciente aparece en la tabla
        diagnostico_text = self.consulta_data['diagnostico']
        
        # Buscar el elemento que contiene el diagnóstico (en cualquier celda)
        consulta_row = wait.until(
            EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{diagnostico_text}')]"))
        )
        self.assertTrue(consulta_row.is_displayed())
        
        # Verificar que los nombres asociados también estén en la página (mejor usando page_source)
        self.assertIn(self.paciente_data['nombre'], s.page_source)
        self.assertIn(self.medico_data['nombre'], s.page_source)
        
        # Cierre de sesión (Buena práctica E2E)
        s.get(self.live_server_url + reverse('logout_page'))
        # Verificar que vuelve a la página de login
        wait.until(EC.title_contains('Inicio de Sesión'))