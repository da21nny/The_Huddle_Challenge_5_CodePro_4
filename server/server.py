from flask import Flask
from routes import registrar_rutas
import database

# Inicializar la app
app = Flask(__name__)

# Configurar la base de datos antes de arrancar
database.inicializar_db()

# Registrar las rutas que acabamos de crear
registrar_rutas(app)

if __name__ == '__main__':
    print("🚀 Servidor LogHero levantado en http://localhost:5000")
    app.run(port=5000, debug=True)