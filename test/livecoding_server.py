# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "Servidor activo"}), 200

@app.route('/mensaje', methods=['POST'])
def recibir_mensaje():
    # PSEUDOCODIGO PARA PRACTICAR:
    # 1. Obtener los datos JSON de la peticion (request)
    datos = request.get_json()
    # 2. Verificar si la clave "texto" existe en esos datos
    if not datos or "texto" not in datos:
    # 3. Si existe, retornar un JSON con {"respuesta": "Mensaje recibido"} y codigo de estado 200
        return jsonify({"respuesta": "Mensaje recibido"}), 200
    # 4. Si no existe, retornar un JSON con {"error": "Falta el texto"} y codigo de estado 400
    return jsonify({"error": "Falta el texto"}), 400
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)