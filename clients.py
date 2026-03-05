import requests
import time
import random
import threading
from datetime import datetime, timezone

URL = "http://localhost:5000/logs" # URL del servidor

SERVICIOS = [ # Lista de servicios
    {
        "nombre": "servicio-a",
        "token": "Token Servicio-123",
        "mensajes": [
            ("INFO",     "Operacion exitosa"),
            ("DEBUG",    "Verificando datos"),
            ("WARNING",  "Respuesta lenta"),
            ("ERROR",    "Conexion perdida"),
            ("CRITICAL", "Sistema caido"),
        ]
    }, # Servicio A
    {
        "nombre": "servicio-b",
        "token": "Token Servicio-B-456",
        "mensajes": [
            ("INFO",     "Tarea completada"),
            ("DEBUG",    "Procesando solicitud"),
            ("WARNING",  "Recurso bajo"),
            ("ERROR",    "Fallo inesperado"),
            ("CRITICAL", "Error critico detectado"),
        ]
    } # Servicio B
]

def simular(config): # Simula el envio de logs
    print(f" Iniciando Simulacion de {config['nombre']}...")
    headers = {"Authorization": config['token'], "Content-Type": "application/json"} # Headers para el request

    while True: # Ciclo infinito para enviar logs
        severidad, texto = random.choice(config['mensajes']) # Selecciona un mensaje aleatorio
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": config['nombre'],
            "severity": severidad,
            "message": texto
        } # Crea el log

        try:
            res = requests.post(URL, json=log, headers=headers) # Envía el log al servidor
            if res.status_code == 401: # Verifica que el estado del request sea 401
                print(f"[{config['nombre']}] Rechazado. El servidor dijo: {res.text}") # Imprime el mensaje de error
            else:
                print(f"[{config['nombre']}] Log enviado -> Status: {res.status_code}") # Imprime el estado del request
        except:
            print(f"[{config['nombre']}] Error de conexion.") # Imprime el error de conexion

        time.sleep(random.randint(2,5)) # Espera un tiempo aleatorio antes de enviar el siguiente log

if __name__ == '__main__':
    print("Levantando la flota de servicios simulados (Ctrl+C para detener)") # Imprime el mensaje de inicio

    for servicio in SERVICIOS: # Itera sobre los servicios
        hilo = threading.Thread(target=simular, args=(servicio,), daemon=True) # Crea un hilo para cada servicio
        hilo.start() # Inicia el hilo

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Simulacion detenida") # Imprime el mensaje de detencion
