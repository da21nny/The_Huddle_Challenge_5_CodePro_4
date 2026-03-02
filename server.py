from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__)
TOKENS_VALIDOS = {"Token auth-secreto-123", "Token order-secreto-456"}
DATABASE = "logs.db"

def init_db():
    #Crea la base de datos y la tabla si no existen
    conn = sqlite3.connect(DATABASE)

    conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    received_at TEXT,
                    service TEXT,
                    severity TEXT,
                    message TEXT)''')
    conn.commit()
    conn.close()

@app.route('/logs', methods=['POST'])
def recibir_log():
    if request.headers.get('Authorization') not in TOKENS_VALIDOS:
        return jsonify({"error": "Quien sos, bro?"}), 401

    datos = request.get_json()
    if not datos:
        return jsonify({"error": "JSON invalido"}), 400

    if isinstance(datos, dict):
        datos = [datos]

    conn = sqlite3.connect(DATABASE)
    hora_recepcion = datetime.now(timezone.utc).isoformat()

    campos_requeridos = {'timestamp', 'service', 'severity', 'message'}
    for d in datos:
        for campo in campos_requeridos:
            if campo not in d:
                return jsonify({"error": f"Falta el campo '{campo}' en uno de los logs"}), 400
        conn.execute('''INSERT INTO logs (timestamp, received_at, service, severity, message)
                        VALUES (?, ?, ?, ?, ?)''',
                    (d['timestamp'], hora_recepcion, d['service'], d['severity'], d['message']))

    conn.commit()
    conn.close()
    return jsonify({"status": "Logs registrados exitosamente"}), 201

@app.route('/logs', methods=['GET'])
def consultar_logs():
    if request.headers.get('Authorization') not in TOKENS_VALIDOS:
        return jsonify({"error": "Quien sos, bro?"}), 401
    
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    filtros = {
        'timestamp_start': 'timestamp >= ?',
        'timestamp_end': 'timestamp <= ?',
        'received_at_start': 'received_at >= ?',
        'received_at_end': 'received_at <= ?'
    }

    for clave_url, condicion_sql in filtros.items():
        valor = request.args.get(clave_url)
        if valor:
            query += f" AND {condicion_sql}"
            params.append(valor)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    filas = conn.execute(query + " ORDER BY id DESC", params).fetchall()
    conn.close()

    return jsonify([dict(f) for f in filas]), 200

if __name__ == '__main__':
    init_db()
    print("Servidor LogHero levantado en http://localhost:5000")
    app.run(port=5000, debug=True)