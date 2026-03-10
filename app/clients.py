import requests
import time
import random
import sys
from datetime import datetime, timezone

URL = "http://127.0.0.1:5000/logs" # URL con IP para evitar retrasos de resolución DNS en Windows

TOKENS = {"Token Servicio-A-123", "Token Servicio-B-456", "Token-Invalido-999"} # Tokens para los servicios (2 validos y 1 invalido)

SERVICIOS = [
    {"nombre": "Servicio A"},
    {"nombre": "Servicio B"}
] # Nombres de los servicios 

MENSAJES = {
    "INFO": "Operacion exitosa",
    "DEBUG": "Verificando datos",
    "WARNING": "Respuesta lenta",
    "ERROR": "Conexion perdida",
    "CRITICAL": "Sistema caido"
}   # Mensajes para los logs

def enviar_log(session, config, numero): # Funcion que envia los logs
    headers = {"Authorization": random.choice(list(TOKENS)), "Content-Type": "application/json"} # Cabeceras para la peticion
    severidad, texto = random.choice(list(MENSAJES.items())) # Selecciona una severidad y un mensaje aleatorio
    
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(), # Obtiene la fecha y hora actual
        "service": config['nombre'], # Nombre del servicio
        "severity": severidad, # Severidad del log
        "message": texto # Mensaje del log
    } # Crea el log con los datos del servicio

    try:
        res = session.post(URL, json=log, headers=headers, timeout=1) # Envia la peticion al servidor con los datos del log
        # Formato limpio: [Numero] NombreServicio (Status) -> Mensaje del Servidor
        print(f"[{numero:03d}] {config['nombre']} ({res.status_code}) -> {res.text.strip()}")
    except requests.exceptions.RequestException as e: # Captura la excepcion si hay un error en la peticion
        print(f"[{numero:03d}] Error de conexion: {e}")

if __name__ == '__main__':
    print(f"Simulación rápida de {SERVICIOS} (500 envíos)...") # Muestra un mensaje de que la simulacion ha comenzado
    session = requests.Session() # Crea una sesion para la peticion
    
    try:
        for i in range(1, 501): # Itera sobre los 500 envios
            config = random.choice(SERVICIOS) # Selecciona una configuracion aleatoria
            enviar_log(session, config, i) # Envia el log al servidor
    except KeyboardInterrupt:
        print("\n[!] Detenido por el usuario.") # Muestra un mensaje de que la simulacion ha sido detenida por el usuario
        sys.exit(0) # Sale del programa

    print("\nSimulacion finalizada.") # Muestra un mensaje de que la simulacion ha finalizado
