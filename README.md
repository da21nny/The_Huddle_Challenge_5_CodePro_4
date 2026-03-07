# The_Huddle_Challenge_5_CodePro_4
"Los sistemas caen. Los logs sobreviven." — proverbio DevOps

# 🐧 LogHero - Servicio de Logging Distribuido

LogHero es un sistema de logging centralizado construido con Python y Flask. Actúa como el "confesor de los sistemas", diseñado para recibir, validar, almacenar y filtrar logs provenientes de múltiples servicios de forma concurrente y segura.

## ✨ Características Principales

* **API RESTful**: Recepción (`POST /logs`) y consulta (`GET /logs`) de eventos del sistema.
* **Autenticación por Tokens**: Seguridad estricta a través de la cabecera HTTP `Authorization`, rechazando accesos no autorizados con respuestas claras del servidor.
* **Persistencia Robusta**: Almacenamiento local automatizado en **SQLite**, registrando tanto el momento del evento (`timestamp`) como la recepción en el servidor (`received_at`).
* **Simulación de Tráfico Real**: Script de cliente optimizado para realizar ráfagas de envíos rápidos (50 envíos por ejecución) utilizando selecciones aleatorias entre tokens válidos y falsos para probar la seguridad del servidor.
* **Optimización de Conexión**: Uso de `requests.Session` en los clientes para maximizar la velocidad de envío al reutilizar conexiones TCP.

---

## 🚀 Guía de Uso e Instalación

### 1. Requisitos Previos
Asegúrate de tener **Python 3.8+** instalado. Luego, instala las librerías necesarias ejecutando:
```bash
pip install flask requests
```

### 2. Levantar el Servidor Central

El servidor debe estar en ejecución para empezar a escuchar las peticiones y gestionar la base de datos `logs.db`. En tu terminal, ejecuta:

```bash
python server.py
```

*El servidor quedará corriendo en `http://localhost:5000`.*

### 3. Ejecutar la Simulación de Clientes

Abre una **segunda terminal** en la misma carpeta y ejecuta el script de clientes. Este realizará una ráfaga de 50 envíos aleatorios (auténticos y falsos) de forma secuencial y rápida:

```bash
python clients.py
```

*Puedes detener la ráfaga en cualquier momento presionando `Ctrl+C`.*

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Flask
* **Base de Datos:** SQLite3
* **Peticiones HTTP:** Librería `requests` (con optimización de `Session`)
* **Gestión de Procesos:** Captura de señales de sistema (`sys.exit`) para paradas limpias.

---

*Desarrollado por Edgar Vega (Da21nny) - 💻 Software Developer.*