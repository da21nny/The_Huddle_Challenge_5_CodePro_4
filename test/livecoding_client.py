# client.py
import requests

URL_SERVIDOR = "http://127.0.0.1:5000"

def verificar_servidor():
    try:
        respuesta = requests.get(f"{URL_SERVIDOR}/ping")
        print("Ping exitoso:", respuesta.json())
    except requests.exceptions.ConnectionError:
        print("Error: El servidor no esta en linea.")

def enviar_mensaje(texto_mensaje):
    # PSEUDOCODIGO PARA PRACTICAR:
    # 1. Crear un diccionario llamado 'carga_util' que contenga la clave "texto" y el valor de 'texto_mensaje'
    carga_util = {"texto": texto_mensaje}
    # 2. Hacer una peticion POST a la URL: URL_SERVIDOR + "/mensaje"
    respuesta = requests.post(f"{URL_SERVIDOR}/mensaje", json=carga_util)
    # 3. Enviar el diccionario 'carga_util' utilizando el parametro json= en la peticion
    # 4. Imprimir en pantalla el codigo de estado (status_code) y el contenido (json) de la respuesta
    print(f"code: {respuesta.status_code}")
    print(f"Respuesta", respuesta.json())
    

if __name__ == '__main__':
    verificar_servidor()
    enviar_mensaje("Hola, este es mi primer mensaje de prueba")