import requests
import time
import random
from datetime import datetime, timezone

# Configuraciones del servicio
URL_SERVIDOR = "http://localhost:5000/logs"
TOKEN = "Token auth-secreto-123" # Debe coincidir con el TOKENS_VALIDOS del server
NOMBRE_SERVICIO = "auth-service"

# Lista de posibles eventos para darle realismo
MENSAJES = [
    ("INFO", "Usuario 'admin' inició sesión correctamente"),
    ("WARNING", "Intento fallido de login para 'user99'"),
    ("ERROR", "Conexión a la base de datos de usuarios perdida"),
    ("INFO", "Token de sesión renovado")
]

def simular_auth():
    """Genera y envía logs aleatorios al servidor central en un bucle infinito."""
    print(f"🟢 Iniciando simulación de {NOMBRE_SERVICIO}...")
    
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    while True:
        # Elegir un mensaje y severidad al azar
        severidad, texto = random.choice(MENSAJES)
        
        # Generar timestamp en formato ISO 8601 (estándar profesional)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Armar el paquete JSON
        datos_log = {
            "timestamp": timestamp,
            "service": NOMBRE_SERVICIO,
            "severity": severidad,
            "message": texto
        }
        
        try:
            # Disparar el log hacia nuestra API Flask
            respuesta = requests.post(URL_SERVIDOR, json=datos_log, headers=headers)
            print(f"[{NOMBRE_SERVICIO}] Log enviado -> Status: {respuesta.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[{NOMBRE_SERVICIO}] ❌ Error: ¿Está el servidor encendido?")
            
        # Esperar un tiempo aleatorio entre 2 y 5 segundos antes del siguiente log
        time.sleep(random.randint(2, 5))