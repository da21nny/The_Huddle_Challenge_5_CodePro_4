# 🐧 LogHero - Servicio de Logging Distribuido

"Los sistemas caen. Los logs sobreviven. Si no lo logueaste, no pasó."

LogHero es un sistema de logging centralizado construido con Python y Flask. Funciona como un receptor central seguro para múltiples microservicios, permitiendo la validación, persistencia y consulta de logs de forma eficiente.

## 📖 Descripción General
LogHero nace como una solución al caos de la falta de visibilidad en sistemas distribuidos. En una arquitectura moderna, donde múltiples servicios interactúan simultáneamente, saber qué falló y cuándo es crítico. Este proyecto implementa un "Faro de Verdad": un servidor centralizado que recolecta, valida y almacena cada evento significativo del ecosistema, permitiendo un análisis posterior preciso y auditable.

## ⚙️ Cómo Funciona
El ciclo de vida de un log en LogHero sigue estos pasos:

1.  **Emisión**: Los microservicios generan eventos en formato JSON. Cada evento contiene obligatoriamente: `timestamp`, `service`, `severity` y `message`.
2.  **Autenticación**: Para garantizar la seguridad, cada cliente debe enviar un `Authorization: Token <token>` válido en los headers de su petición POST.
3.  **Recepción y Validacion**: El servidor LogHero recibe el JSON, verifica que el token sea reconocido y que el formato de los datos sea correcto. Si algo falla (token inválido o campos faltantes), el servidor responde con errores descriptivos (ej. `"Quién sos, bro?"` para fallos de auth).
4.  **Persistencia**: Los logs válidos se guardan inmediatamente en una base de datos SQLite (`logs.db`). El servidor añade automáticamente una marca de tiempo de recepción (`received_at`) para diferenciar cuándo ocurrió el evento de cuándo fue recibido.
5.  **Explotación de Datos**: Los administradores pueden realizar consultas mediante el endpoint `GET /logs`, utilizando filtros dinámicos por rangos de fechas tanto para el momento de emisión como para el de recepción.

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