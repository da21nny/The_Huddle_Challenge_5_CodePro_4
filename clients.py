import requests
import time
import random
import threading
from datetime import datetime, timezone

URL = "http://localhost:5000/logs" # URL del servidor

# Configuración centralizada
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

def simular(config): # Simula el envio de logs
    print(f" Iniciando Simulacion de {NOMBRE_SERVICIO} ({config['tipo']})...")
    headers = {"Authorization": config['token'], "Content-Type": "application/json"}

    while True:
        severidad, texto = random.choice(list(MENSAJES.items()))
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": NOMBRE_SERVICIO,
            "severity": severidad,
            "message": texto
        }

        try:
            res = requests.post(URL, json=log, headers=headers)
            status = "EXITO" if res.status_code == 201 else "RECHAZADO"
            print(f"[{NOMBRE_SERVICIO} - {config['tipo']}] Log enviado -> {status} ({res.status_code})")
        except:
            print(f"[{NOMBRE_SERVICIO}] Error de conexion.")

        time.sleep(random.randint(2,5))

if __name__ == '__main__':
    print("Simulación de servicios (Ctrl+C para detener)")

    for servicio in SERVICIOS:
        threading.Thread(target=simular, args=(servicio,), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Simulacion detenida")
