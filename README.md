# 🐧 LogHero - Servicio de Logging Distribuido

"Los sistemas caen. Los logs sobreviven. Si no lo logueaste, no pasó."

LogHero es un sistema de logging centralizado construido con Python y Flask. Funciona como un receptor central seguro para múltiples microservicios, permitiendo la validación, persistencia y consulta de logs de forma eficiente.

---

## 🏗️ Arquitectura del Sistema

```text
   [ Microservicio A ]       [ Microservicio B ]
          |                         |
          |  (JSON POST + Token)    |  (JSON POST + Token)
          └───────────┬─────────────┘
                      |
              ▼───────┴───────▼
              |   LogHero IP  |
              |   (API Port)  |
              ▲───────┬───────▲
                      |
          ┌───────────┴───────────┐
          |    Validación Token   |
          ├───────────────────────┤
          |   Escritura SQLite    |
          └───────────┬───────────┘
                      |
              ▼───────┴───────▼
              |    logs.db    |
              └───────────────┘
```

---

## 📂 Estructura del Proyecto

```text
The_Huddle_Challenge_5/
├── app/                  # Núcleo de la aplicación
│   ├── server.py         # Servidor API Flask (Recibe y consulta logs)
│   └── clients.py        # Simulador de clientes (Genera tráfico de logs)
├── test/                 # Pruebas automatizadas del sistema
│   ├── server/           # Tests de integración del servidor
│   └── clients/          # Tests de lógica de los clientes
├── requirements.txt      # Dependencias del proyecto
├── .gitignore            # Archivos excluidos de Git
└── README.md             # Documentación principal
```

---

## ✨ Características Principales

*   **API RESTful**: Recepción (`POST /logs`) y consulta (`GET /logs`) con filtros dinámicos.
*   **Seguridad**: Autenticación estricta por tokens (`Authorization: Token ...`).
*   **Persistencia**: Registro automático en **SQLite** con tiempos de evento y recepción.
*   **Simulación Pro**: Generador de ráfagas rápidas (500+ envíos) con mezcla aleatoria de tokens válidos e inválidos.
*   **Alto Rendimiento**: Reutilización de conexiones mediante `requests.Session` y comunicación directa por IP.

---

## 🚀 Instalación y Uso

### 1. Clonar e instalar dependencias
Asegúrate de tener Python instalado. Luego, instala los requisitos necesarios:

```bash
pip install -r requirements.txt
```

### 2. Iniciar el Servidor
Ejecuta el servidor central desde la carpeta raíz:

```bash
python app/server.py
```
*El servidor escuchará en `http://127.0.0.1:5000`.*

### 3. Ejecutar la Simulación de Clientes
En otra terminal, lanza el simulador para empezar a llenar la base de datos:

```bash
python app/clients.py
```
*Puedes detener la ráfaga en cualquier momento con `Ctrl+C`.*

---

## 🛠️ Tecnologías
*   **Servidor:** Flask, SQLite3
*   **Cliente:** Requests (Session pooling)
*   **Lógica:** Python 3.8+

---
*Desarrollado por Edgar Vega (Da21nny) - 💻 Software Developer.*