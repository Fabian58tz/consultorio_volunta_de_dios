import os
import time
import requests
import pytest
from django.urls import reverse

# =================================================================
# CONFIGURACIÓN DEL ACUERDO DE NIVEL DE SERVICIO (SLA)
# =================================================================

# La variable SLA_MS se lee de la variable de entorno 'SLA_MS'.
# Esto permite que el usuario ajuste el umbral de rendimiento sin
# modificar el código fuente de la prueba.
# Valor por defecto: 2500 ms (2.5 segundos).
SLA_MS = int(os.getenv("SLA_MS", 2500)) 

# Para ejecutar estas pruebas de rendimiento:
# 1. Asegúrate de tener pytest, requests, y pytest-django instalados:
#    pip install pytest requests pytest-django
# 2. Ejecuta solo las pruebas marcadas como 'perf':
#    Linux/macOS: SLA_MS=1000 pytest -m perf
#    Windows: $env:SLA_MS=1000 ; pytest -m perf
#    (Reemplaza 1000 por tu umbral deseado, o usa el valor por defecto de 2500ms)

@pytest.mark.perf
def test_login_page_latency_sla(live_server):
    """
    Verifica que la página de login responda por debajo del SLA (SLA_MS).
    
    Utiliza requests.get para medir el tiempo real que tarda el servidor 
    en responder al cliente (sin la sobrecarga del navegador de Selenium).
    """
    
    # 1. Obtener la URL de login usando el nombre de la vista.
    # Usamos 'login_page' por consistencia con test_e2e.py
    try:
        login_url_path = reverse('login_page')
    except Exception as e:
        pytest.fail(f"No se encontró la URL con el nombre 'login_page'. Revise su urls.py. Error: {e}")
        
    url = f"{live_server.url}{login_url_path}"

    print(f"\n--- Probando SLA: {SLA_MS} ms en {url} ---")

    # Iniciar medición de tiempo
    t0 = time.perf_counter()
    
    # 2. Realizar la solicitud HTTP
    # Usar un timeout de 10 segundos para la solicitud para evitar bloqueos.
    try:
        resp = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        pytest.fail(f"La solicitud a {url} ha excedido el tiempo de espera de 10s.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Fallo en la solicitud HTTP a {url}: {e}")
            
    # Finalizar medición de tiempo y calcular latencia
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print(f"Latencia medida: {elapsed_ms:.1f} ms")

    # 3. Verificación de Status Code
    assert resp.status_code == 200, f"Status inesperado {resp.status_code} para {url}. Contenido: {resp.text[:100]}..."
    
    # 4. Verificación del SLA (Tiempo de Respuesta)
    assert elapsed_ms <= SLA_MS, f"FALLO SLA: Latencia {elapsed_ms:.1f} ms excede el umbral de {SLA_MS} ms"