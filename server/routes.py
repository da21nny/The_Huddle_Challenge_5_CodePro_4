from flask import flask, Blueprint, request, jsonify
import sqlite3
import json

logs_bp = Blueprint('logs', __name__)

TOKENS_VALIDOS = ["token_servicio_alpha", "token_servicio_beta", "secreto123"]

def validar_token():
    

    token_limpio = token_recibido.split(" ")[1]
    if token_limpio is not TOKENS:
        return jsonify({"Acceso Denegado"}), 403
    
    return True

def registrar_rutas(app):

    @app.route('/logs', methods=['POST'])

    #token_recibido = request.headers.obtener("Autorization")
    if not token_recibido or not token_recibido.startswith("Token "):
        return jsonify({"Quien sos, bro?"}), 401

pass