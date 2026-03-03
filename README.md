# The_Huddle_Challenge_5_CodePro_4
"Los sistemas caen. Los logs sobreviven." — proverbio DevOps

# 🐧 LogHero - Servicio de Logging Distribuido

LogHero es un sistema de logging centralizado construido con Python y Flask. Actúa como el "confesor de los sistemas", diseñado para recibir, validar, almacenar y filtrar logs provenientes de múltiples microservicios de forma concurrente y segura.

## ✨ Características Principales

* **API RESTful**: Recepción (`POST /logs`) y consulta (`GET /logs`) de eventos del sistema.
* **Autenticación por Tokens**: Seguridad estricta a través de la cabecera HTTP `Authorization`, rechazando accesos no autorizados con respuestas claras.
* **Persistencia Robusta**: Almacenamiento local automatizado en **SQLite**, registrando tanto el momento en que ocurrió el evento (`timestamp`) como el momento exacto en que el servidor lo recibió (`received_at`).
* **Soporte de Batching**: Capacidad para procesar y guardar de manera eficiente múltiples logs enviados en una sola petición.
* **Simulación Concurrente**: Incluye un orquestador basado en hilos (`threading`) que simula el tráfico de varios microservicios (`auth-service` y `order-service`) operando en paralelo.

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

Abre una **segunda terminal** en la misma carpeta y ejecuta el script de clientes. Esto levantará los microservicios que empezarán a disparar logs aleatorios al servidor:

```bash
python clients.py

```

*Presiona `Ctrl+C` en esta terminal para detener la simulación.*

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Flask
* **Base de Datos:** SQLite3
* **Peticiones HTTP:** Librería `requests`
* **Concurrencia:** Módulo `threading` nativo de Python

---

*Desarrollado por Edgar Vega (Da21nny) - 💻 Software Developer desde Paraguay.*