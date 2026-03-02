from flask import request, jsonify
import database # Importamos tu archivo donde estará la lógica de SQLite

# Lista simple de tokens válidos (puedes agregar los que necesites para tus servicios)
TOKENS_VALIDOS = [
    "Token auth-secreto-123", 
    "Token orders-secreto-456"
]

def registrar_rutas(app):
    
    # ==========================================
    # 🛑 ENDPOINT 1: RECIBIR LOGS (POST)
    # ==========================================
    @app.route('/logs', methods=['POST'])
    def recibir_log():
        # 1. El Portero: Validar el Token
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or auth_header not in TOKENS_VALIDOS:
            # El mensaje seco y honesto que pide el documento
            return jsonify({"error": "Quién sos, bro?"}), 401
        
        # 2. Procesar el paquete JSON
        datos = request.get_json()
        
        if not datos:
            return jsonify({"error": "No se envió un JSON válido"}), 400
            
        # 3. El Archivista: Enviar a la base de datos
        # Asumimos que creaste esta función en database.py
        database.guardar_log(datos)
        
        return jsonify({"status": "Log registrado exitosamente"}), 201


    # ==========================================
    # 🔍 ENDPOINT 2: CONSULTAR LOGS (GET)
    # ==========================================
    @app.route('/logs', methods=['GET'])
    def consultar_logs():
        # 1. Leer los filtros de la URL (ej: /logs?service=auth)
        servicio = request.args.get('service')
        fecha_inicio = request.args.get('start')
        fecha_fin = request.args.get('end')
        
        # 2. Pedir datos a database.py aplicando los filtros
        # Si no hay filtros, las variables serán 'None' y database.py devolverá todo
        resultados = database.obtener_logs(servicio, fecha_inicio, fecha_fin)
        
        # 3. Devolver la lista en formato JSON
        return jsonify(resultados), 200