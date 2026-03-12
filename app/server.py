from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__) # Inicializa la aplicacion
TOKENS_VALIDOS = {"Token Servicio-A-123", "Token Servicio-B-456"} # Tokens validos para los servicios
DATABASE = "logs.db" # Base de datos

def init_db(): # Inicializa la base de datos
    conn = sqlite3.connect(DATABASE) # Conecta a la base de datos

    conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    received_at TEXT,
                    service TEXT,
                    severity TEXT,
                    message TEXT)''') # Crea la tabla si no existe
    conn.commit() # Guarda los cambios
    conn.close() # Cierra la conexion

@app.route('/logs', methods=['POST']) # Define la ruta /logs
def recibir_log(): # Recibe los logs
    if request.headers.get('Authorization') not in TOKENS_VALIDOS: # Verifica que el token sea valido
        return jsonify({"error": "Quien sos, bro?"}), 401

    datos = request.get_json() # Obtiene los datos del request
    if not datos: # Verifica que los datos no esten vacios
        return jsonify({"error": "JSON invalido"}), 400

    if isinstance(datos, dict): # Verifica que los datos sean un diccionario
        datos = [datos] # Convierte los datos a una lista

    conn = sqlite3.connect(DATABASE) # Conecta a la base de datos
    hora_recepcion = datetime.now(timezone.utc).isoformat() # Obtiene la hora de recepcion

    campos_requeridos = {'timestamp', 'service', 'severity', 'message'} # Campos requeridos
    for d in datos: # Itera sobre los datos
        for campo in campos_requeridos: # Itera sobre los campos requeridos
            if campo not in d: # Verifica que el campo no este en los datos
                return jsonify({"error": f"Falta el campo '{campo}' en uno de los logs"}), 400
        conn.execute('''INSERT INTO logs (timestamp, received_at, service, severity, message)
                        VALUES (?, ?, ?, ?, ?)''',
                    (d['timestamp'], hora_recepcion, d['service'], d['severity'], d['message']))

    conn.commit() # Guarda los cambios
    conn.close() # Cierra la conexion
    return jsonify({"status": "Logs registrados exitosamente"}), 201

@app.route('/logs', methods=['GET']) # Define la ruta /logs
def consultar_logs(): # Consulta los logs
    query = "SELECT * FROM logs WHERE 1=1" # Consulta a la base de datos
    params = []

    filtros = {
        'timestamp_start': 'timestamp >= ?',
        'timestamp_end': 'timestamp <= ?',
        'received_at_start': 'received_at >= ?',
        'received_at_end': 'received_at <= ?',
        'severity': 'severity = ?',
        'service': 'service = ?'
    } # Filtros para la consulta

    for clave_url, condicion_sql in filtros.items(): # Itera sobre los filtros
        valor = request.args.get(clave_url) # Obtiene los valores de los filtros
        if valor: # Verifica que los valores no esten vacios
            query += f" AND {condicion_sql}" # Agrega la condicion a la consulta
            params.append(valor) # Agrega los valores a los parametros

    conn = sqlite3.connect(DATABASE) # Conecta a la base de datos
    conn.row_factory = sqlite3.Row # Convierte las filas a diccionarios
    filas = conn.execute(query + " ORDER BY id ASC", params).fetchall() # Ejecuta la consulta y obtiene los resultados
    conn.close() # Cierra la conexion

    return jsonify([dict(f) for f in filas]), 200 # Retorna los resultados

if __name__ == '__main__':
    init_db() # Inicializa la base de datos
    print("Servidor LogHero levantado en http://localhost:5000")
    app.run(port=5000, debug=True) # Ejecuta el servidor