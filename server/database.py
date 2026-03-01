import sqlite3
import os

# Definimos la ruta donde vivirá nuestro archivo de base de datos
# Guardarlo en una carpeta 'storage' mantiene la raíz del proyecto limpia
DB_DIR = "server/storage"
DB_PATH = os.path.join(DB_DIR, "logs.db")

def obtener_conexion():
    """Crea y retorna una conexión a la base de datos configurada para devolver diccionarios."""
    conn = sqlite3.connect(DB_PATH)
    # Esto es magia pura: hace que las filas devueltas se comporten como diccionarios
    # en lugar de tuplas, facilitando la conversión a JSON en Flask.
    conn.row_factory = sqlite3.Row 
    return conn

def inicializar_db():
    """Crea la carpeta storage y la tabla de logs si no existen. Se ejecuta al iniciar el server."""
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Estructura de la tabla. Usamos TEXT para timestamp (formato ISO 8601 idealmente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Base de datos SQLite lista y conectada.")

def guardar_log(datos):
    """Inserta un nuevo log en la tabla. Recibe un diccionario 'datos'."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Usamos (?) para evitar inyecciones SQL. NUNCA concatenar strings directamente en SQL.
    cursor.execute('''
        INSERT INTO logs (timestamp, service, severity, message)
        VALUES (?, ?, ?, ?)
    ''', (
        datos.get('timestamp'),
        datos.get('service'),
        datos.get('severity'),
        datos.get('message')
    ))
    
    conn.commit()
    conn.close()

def obtener_logs(servicio=None, fecha_inicio=None, fecha_fin=None):
    """
    Consulta los logs. Arma la query dinámicamente dependiendo de los filtros que lleguen.
    Si todos los parámetros son None, devuelve toda la tabla.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # El 'WHERE 1=1' es un truco clásico. Siempre es verdadero, 
    # lo que nos permite añadir 'AND...' dinámicamente sin romper la sintaxis.
    query = "SELECT * FROM logs WHERE 1=1"
    parametros = []
    
    if servicio:
        query += " AND service = ?"
        parametros.append(servicio)
        
    if fecha_inicio:
        query += " AND timestamp >= ?"
        parametros.append(fecha_inicio)
        
    if fecha_fin:
        query += " AND timestamp <= ?"
        parametros.append(fecha_fin)
        
    # Ordenamos del más reciente al más antiguo
    query += " ORDER BY timestamp DESC"
    
    cursor.execute(query, parametros)
    filas = cursor.fetchall()
    conn.close()
    
    # Convertimos las filas (sqlite3.Row) a una lista de diccionarios estándar de Python
    return [dict(fila) for fila in filas]