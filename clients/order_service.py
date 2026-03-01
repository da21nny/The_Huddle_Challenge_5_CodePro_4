import requests
import time
import random
from datetime import datetime, timezone

URL_SERVIDOR = "http://localhost:5000/logs"
TOKEN = "Token orders-secreto-456"
NOMBRE_SERVICIO = "order-service"

MENSAJES = [
    ("INFO", "Pedido #1024 creado exitosamente"),
    ("ERROR", "Fallo al procesar pago con tarjeta terminada en 4455"),
    ("WARNING", "Stock bajo para el producto 'Teclado Mecánico'"),
    ("INFO", "Pedido #1020 enviado al cliente")
]

def simular_orders():
    print(f"📦 Iniciando simulación de {NOMBRE_SERVICIO}...")
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

    while True:
        severidad, texto = random.choice(MENSAJES)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        datos_log = {
            "timestamp": timestamp,
            "service": NOMBRE_SERVICIO,
            "severity": severidad,
            "message": texto
        }
        
        try:
            respuesta = requests.post(URL_SERVIDOR, json=datos_log, headers=headers)
            print(f"[{NOMBRE_SERVICIO}] Log enviado -> Status: {respuesta.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[{NOMBRE_SERVICIO}] ❌ Error de conexión.")
            
        # Este servicio es un poco más lento, dispara cada 3 a 7 segundos
        time.sleep(random.randint(3, 7))