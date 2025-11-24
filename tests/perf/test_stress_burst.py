import os
import math
import time
import requests
import pytest
from django.urls import reverse
from concurrent.futures import ThreadPoolExecutor, as_completed

# =================================================================
# CONFIGURACIÓN DEL ACUERDO DE NIVEL DE SERVICIO (SLA)
# =================================================================

# La variable SLA_MS se lee de la variable de entorno 'SLA_MS'.
# Esto permite que el usuario ajuste el umbral de rendimiento sin
# modificar el código fuente de la prueba.
# Valor por defecto: 2500 ms (2.5 segundos).
SLA_MS = int(os.getenv("SLA_MS", 3000)) 

# --- Configuración para la Prueba de Ráfaga de Estrés (Burst) ---
USERS = int(os.getenv("BURST_USERS", "20")) # 20 hilos concurrentes
REQUESTS = int(os.getenv("BURST_REQUESTS", "100")) # 100 requests en total
P95_MS = int(os.getenv("P95_MS", "2500")) # Umbral P95: 2500 ms (2.5 segundos)
ERROR_RATE_MAX = float(os.getenv("ERROR_RATE_MAX", "0.05")) # Tasa de error máxima: 5%

# =================================================================
# FIXTURE PARA OBTENER LA URL DE LOGIN (REUTILIZACIÓN)
# =================================================================

@pytest.fixture
def login_url(live_server):
    """
    Fixture que resuelve la URL absoluta de la vista 'login_page'.
    Se inyecta automáticamente en las funciones de prueba que lo requieren.
    """
    # Usamos 'login_page' por consistencia en todo el proyecto.
    try:
        login_url_path = reverse('login_page')
    except Exception as e:
        pytest.fail(f"No se encontró la URL con el nombre 'login_page'. Revise su urls.py. Error: {e}")
        
    return f"{live_server.url}{login_url_path}"

# =================================================================
# FUNCIÓN UTILITARIA
# =================================================================

def percentile(values, p):
    """Retorna el percentil p (0-100) de una lista no vacía."""
    if not values:
        return math.nan
    values = sorted(values)
    k = (len(values)-1) * (p/100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    # Interpolación lineal simple
    return values[f] + (values[c] - values[f]) * (k - f)

# =================================================================
# PRUEBA 1: Latencia de Página y SLA
# =================================================================

@pytest.mark.perf
def test_login_page_latency_sla(login_url):
    """
    Verifica que la página de login responda por debajo del SLA (SLA_MS).
    Mide el tiempo real que tarda el servidor en responder al cliente.
    """
    
    print(f"\n--- Probando SLA: {SLA_MS} ms en {login_url} ---")

    # Iniciar medición de tiempo
    t0 = time.perf_counter()
    
    # 1. Realizar la solicitud HTTP
    # Usar un timeout de 10 segundos para la solicitud para evitar bloqueos.
    try:
        resp = requests.get(login_url, timeout=10)
    except requests.exceptions.Timeout:
        pytest.fail(f"La solicitud a {login_url} ha excedido el tiempo de espera de 10s.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Fallo en la solicitud HTTP a {login_url}: {e}")
            
    # Finalizar medición de tiempo y calcular latencia
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print(f"Latencia medida: {elapsed_ms:.1f} ms")

    # 2. Verificación de Status Code
    assert resp.status_code == 200, f"Status inesperado {resp.status_code} para {login_url}. Contenido: {resp.text[:100]}..."
    
    # 3. Verificación del SLA (Tiempo de Respuesta)
    assert elapsed_ms <= SLA_MS, f"FALLO SLA: Latencia {elapsed_ms:.1f} ms excede el umbral de {SLA_MS} ms"

# =================================================================
# PRUEBA 2: Latencia Detallada (TTFB)
# =================================================================

@pytest.mark.perf
def test_login_latency_detailed(login_url):
    """
    Mide el tiempo total de respuesta y el Time To First Byte (TTFB) 
    para la página de inicio de sesión. Proporciona diagnóstico detallado.
    """
    
    print(f"\nProbando URL: {login_url}")
    
    # Medición DNS + Conexión + Transferencia
    t0 = time.perf_counter()
    # Usar un timeout de 10 segundos para evitar que el test se cuelgue.
    try:
        resp = requests.get(login_url, timeout=10)
    except requests.exceptions.Timeout:
        pytest.fail(f"La solicitud a {login_url} ha excedido el tiempo de espera (10s)")
        
    total_time = (time.perf_counter() - t0) * 1000

    # Tiempo hasta primer byte (TTFB)
    # resp.elapsed proporciona el objeto timedelta.
    ttfb = resp.elapsed.total_seconds() * 1000

    print(f"\n=== DIAGNÓSTICO DETALLADO ===")
    print(f"Tiempo total (latencia): {total_time:.1f} ms")
    print(f"TTFB (Time To First Byte): {ttfb:.1f} ms")
    print(f"Tiempo de Transferencia: {total_time - ttfb:.1f} ms")
    print(f"Tamaño respuesta: {len(resp.content)} bytes")

    # Verificación de que la solicitud fue exitosa
    assert resp.status_code == 200, f"Se esperaba un código 200, se recibió {resp.status_code}"

# =================================================================
# PRUEBA 3: Ráfaga de Estrés (Concurrencia)
# =================================================================

@pytest.mark.perf
def test_burst_stress_login(login_url):
    """
    Ráfaga concurrente de requests (GET) al login para medir estabilidad.
    
    Verifica que la latencia del percentil 95 (P95) y la tasa de errores
    se mantengan por debajo de los umbrales definidos por las variables de
    entorno.
    """
        
    print(f"\n--- Burst Test ---")
    print(f"URL: {login_url}")
    print(f"Concurrent Users (Threads): {USERS}")
    print(f"Total Requests: {REQUESTS}")
    print(f"SLA P95: {P95_MS} ms | Max Error Rate: {ERROR_RATE_MAX:.1%}")

    latencies = []
    errors = 0

    def shoot(_):
        """Función que realiza un solo request y mide la latencia."""
        t0 = time.perf_counter()
        try:
            # Timeout para la solicitud de 5 segundos
            r = requests.get(login_url, timeout=5) 
            # Se considera OK si el status está en el rango 2xx o 3xx
            ok = (200 <= r.status_code < 400) 
        except Exception:
            # Error de conexión o timeout
            ok = False
        dt = (time.perf_counter() - t0) * 1000
        return ok, dt

    # Utilizamos ThreadPoolExecutor para simular la concurrencia
    with ThreadPoolExecutor(max_workers=USERS) as ex:
        futures = [ex.submit(shoot, i) for i in range(REQUESTS)]
        for fut in as_completed(futures):
            ok, ms = fut.result()
            if ok:
                latencies.append(ms)
            else:
                errors += 1

    total = REQUESTS
    error_rate = errors / total
    
    # Cálculo de métricas
    p95 = percentile(latencies, 95) if latencies else float("inf")
    avg = sum(latencies) / len(latencies) if latencies else float("inf")

    print(f"Results: Avg={avg:.1f} ms | P95={p95:.1f} ms | Errors={errors}")
    
    # --- Assertions (Verificaciones Funcionales y No Funcionales) ---
    
    # 1. Tasa de error (funcionalidad y estabilidad)
    assert error_rate <= ERROR_RATE_MAX, f"FALLO: Tasa de error {error_rate:.1%} > {ERROR_RATE_MAX:.1%} (Errores: {errors}/{total})"
    
    # 2. Latencia P95 (rendimiento)
    assert p95 <= P95_MS, f"FALLO: P95 {p95:.1f} ms > {P95_MS} ms (Latencia promedio: {avg:.1f} ms)"