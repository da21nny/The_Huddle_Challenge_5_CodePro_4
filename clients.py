import requests
import time
import random
import sys
from datetime import datetime, timezone

URL = "http://localhost:5000/logs" 

NOMBRE_SERVICIO = "Servicio-Unico"
SERVICIOS = [
    {"token": "Token Servicio-A-123", "tipo": "autentico"},
    {"token": "Token-Invalido-999", "tipo": "falso"}
]
MENSAJES = {
    "INFO": "Operacion exitosa",
    "DEBUG": "Verificando datos",
    "WARNING": "Respuesta lenta",
    "ERROR": "Conexion perdida",
    "CRITICAL": "Sistema caido"
}

def enviar_log(session, config, numero):
    headers = {"Authorization": config['token'], "Content-Type": "application/json"}
    severidad, texto = random.choice(list(MENSAJES.items()))
    
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": NOMBRE_SERVICIO,
        "severity": severidad,
        "message": texto
    }

    try:
        # Añadimos un timeout corto para que Ctrl+C responda más rápido si el servidor se cuelga
        res = session.post(URL, json=log, headers=headers, timeout=0.5)
        if res.status_code == 401:
            print(f"[{numero:02d}] [{config['tipo'].upper()}] RECHAZADO. Servidor dice: {res.text.strip()}")
        else:
            status = "EXITO" if res.status_code == 201 else f"ERROR ({res.status_code})"
            print(f"[{numero:02d}] [{config['tipo'].upper()}] Envio -> {status}")
    except requests.exceptions.RequestException as e:
        print(f"[{numero:02d}] Error: {e}")

if __name__ == '__main__':
    print("Simulación rápida (50 envíos aleatorios)...")
    
    session = requests.Session() # Session para reutilizar la conexión y ser más rápido
    
    try:
        for i in range(1, 51):
            config = random.choice(SERVICIOS)
            enviar_log(session, config, i)
            # Sin sleep para velocidad máxima
    except KeyboardInterrupt:
        print("\n[!] Detenido por el usuario.")
        sys.exit(0)

    print("\nSimulacion finalizada.")
