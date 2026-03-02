import requests
import time
import random
import threading
from datetime import datetime, timezone

URL = "http://localhost:5000/logs"

SERVICIOS = [
    {
        "nombre": "auth-service",
        "token": "Token auth-secerto-123",
        "mensajes": [
            ("INFO", "Usuario 'admin' inicio sesion"),
            ("ERROR", "Conexion a BD perdida")
        ]
    },
    {
        "nombre": "order-service",
        "token": "Token order-secreto-456",
        "mensajes": [
            ("INFO", "Pedido #1024 creado"),
            ("WARNING", "Stock bajo")
        ]
    }
]

def simular(config):
    print(f" Iniciando Simulacion de {config['nombre']}...")
    headers = {"Authorization": config['token'], "Content-Type": "application/json"}

    while True:
        severidad, texto = random.choice(config['mensajes'])
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": config['nombre'],
            "severity": severidad,
            "message": texto
        }

        try:
            res = requests.post(URL, json=log, headers=headers)
            print(f"[{config['nombre']}] Log enviado -> Status: {res.status_code}")
        except:
            print(f"[{config['nombre']}] Error de conexion.")

        time.sleep(random.randint(2,5))

if __name__ == '__main__':
    print("Levantando la flota de servicios simulados (Ctrl+C para detener)")

    for servicio in SERVICIOS:
        hilo = threading.Thread(target=simular, args=(servicio,), daemon=True)
        hilo.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Simulacion detenida")
