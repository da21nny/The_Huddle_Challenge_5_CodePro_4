import threading
import time
from auth_service import simular_auth
from order_service import simular_orders

def iniciar_simulacion():
    """Inicia los hilos de los servicios simulados."""
    print("🚀 Levantando flota de servicios simulados (Presiona Ctrl+C para detener)")
    
    # Crear los hilos apuntando a las funciones principales de cada servicio
    hilo_auth = threading.Thread(target=simular_auth, daemon=True)
    hilo_orders = threading.Thread(target=simular_orders, daemon=True)
    
    # Iniciar los hilos
    hilo_auth.start()
    hilo_orders.start()
    
    # Mantener el hilo principal vivo para que los daemons sigan corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Simulación detenida por el usuario.")

if __name__ == '__main__':
    iniciar_simulacion()