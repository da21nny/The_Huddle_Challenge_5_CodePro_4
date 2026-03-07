import requests
import time
import random
import sys
from datetime import datetime, timezone

URL = "http://localhost:5000/logs" # URL del servidor

NOMBRE_SERVICIO = "Servicio-Unico" # Nombre del servicio
SERVICIOS = [
    {"token": "Token Servicio-A-123", "tipo": "autentico"},
    {"token": "Token-Invalido-999", "tipo": "falso"}
] # Tokens validos para los servicios
MENSAJES = {
    "INFO": "Operacion exitosa",
    "DEBUG": "Verificando datos",
    "WARNING": "Respuesta lenta",
    "ERROR": "Conexion perdida",
    "CRITICAL": "Sistema caido"
}   # Mensajes para los logs

def enviar_log(session, config, numero): # Envia los logs
    headers = {"Authorization": config['token'], "Content-Type": "application/json"} # Headers para el request
    severidad, texto = random.choice(list(MENSAJES.items())) # Selecciona un mensaje aleatorio
    
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": NOMBRE_SERVICIO,
        "severity": severidad,
        "message": texto
    } # Log a enviar

    try:
        res = session.post(URL, json=log, headers=headers, timeout=0.5) # Envía el log al servidor con un timeout de 0.5 segundos
        if res.status_code == 401:
            print(f"[{numero:02d}] [{config['tipo'].upper()}] RECHAZADO. Servidor dice: {res.text.strip()}") # Si el token es invalido, muestra un mensaje de error
        else:
            status = "EXITO" if res.status_code == 201 else f"ERROR ({res.status_code})"
            print(f"[{numero:02d}] [{config['tipo'].upper()}] Envio -> {status}") # Si el token es valido, muestra un mensaje de exito
    except requests.exceptions.RequestException as e:
        print(f"[{numero:02d}] Error: {e}") # Si hay un error, muestra un mensaje de error

if __name__ == '__main__':
    print("Simulación rápida (50 envíos aleatorios)...")
    session = requests.Session() # Session para reutilizar la conexión y ser más rápido
    
    try:
        for i in range(1, 51): # Itera 50 veces
            config = random.choice(SERVICIOS) # Selecciona un servicio aleatorio
            enviar_log(session, config, i) # Envía el log al servidor
    except KeyboardInterrupt:
        print("\n[!] Detenido por el usuario.") # Si se presiona Ctrl+C, muestra un mensaje de error
        sys.exit(0)

    print("\nSimulacion finalizada.") # Muestra un mensaje de que la simulacion ha finalizado
