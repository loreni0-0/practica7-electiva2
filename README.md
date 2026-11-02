# Práctica 7 - Electiva II: Aplicación Web "Hola Mundo" con Docker Compose y MySQL

Aplicación web desarrollada en **Python (Flask)** conectada a un servicio de base de datos **MySQL 8.0**, orquestada y administrada mediante **Docker Compose**.

---

## 📋 Pasos y Requerimientos Implementados

### a) Directorio `src/` con código fuente de la app Hola Mundo y conexión a BD
Dentro del directorio `src/` se encuentran los archivos que componen la lógica de la aplicación:
- **`app.py`**: Aplicación web en Flask que implementa:
  - Ruta principal (`/`) que responde con una interfaz web "¡Hola Mundo!".
  - Conexión a la base de datos MySQL mediante la librería `PyMySQL` con reintentos automáticos de conexión.
  - Creación automática de la tabla `registro_saludos`, inserción de registros de prueba (comprobando escritura) y consulta de estadísticas, versión y hora del servidor MySQL (comprobando lectura).
- **`requirements.txt`**: Especificación de dependencias de Python (`Flask`, `PyMySQL`, `cryptography`).
- **`Dockerfile`**: Definición para construir la imagen del contenedor de la aplicación sobre `python:3.11-slim`.

### b) Archivo `docker-compose.yml` con los servicios y parámetros
Archivo de configuración que define y coordina los contenedores, redes virtuales internas, volúmenes de persistencia y comprobaciones de estado de salud (*healthchecks*).

### c) Servicio de servidor de aplicación (`web`)
- Construido automáticamente a partir del contexto `./src` usando su `Dockerfile`.
- Mapeado al puerto local `5000:5000`.
- Configurado con variables de entorno (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) para comunicarse con el contenedor de base de datos.
- Dependencia `depends_on` con condición `service_healthy` para iniciar una vez que MySQL esté 100% listo.

### d) Servicio de base de datos MySQL (`db`)
- Imagen oficial `mysql:8.0`.
- Configurado con variables de entorno para base de datos (`MYSQL_DATABASE`), usuario (`MYSQL_USER`), contraseña (`MYSQL_PASSWORD`) y superusuario (`MYSQL_ROOT_PASSWORD`).
- Persistencia de datos mediante el volumen Docker `mysql_practica7_data`.
- Mapeo de puerto en host `3307:3306` para evitar colisiones con instancias de MySQL que puedan estar ejecutándose en el equipo local (puerto 3306).
- Comprobación de salud (*healthcheck*) periódica con `mysqladmin ping`.

---

## 📁 Estructura del Directorio

```text
practica7-electiva2/
├── .gitignore               # Archivos y carpetas ignorados por Git
├── docker-compose.yml       # Orquestación de servicios web y db
├── README.md                # Documentación del proyecto
└── src/
    ├── app.py               # Servidor Flask y conexión a MySQL
    ├── Dockerfile           # Imagen Docker para el servidor web
    └── requirements.txt     # Dependencias del servidor web
```

---

## 🚀 Instrucciones para Ejecutar el Proyecto

### 1. Iniciar Docker Desktop
Asegúrate de que la aplicación **Docker Desktop** se encuentre abierta y en ejecución en tu equipo.

### 2. Construir e iniciar los servicios
Abre una terminal (PowerShell, CMD o Git Bash) en la carpeta del proyecto y ejecuta:

```bash
docker compose up -d --build
```

### 3. Verificar en el Navegador
Ingresa a:
👉 [http://localhost:5000](http://localhost:5000)

Verás la tarjeta interactiva de **¡Hola Mundo!** con el estado de conexión a MySQL, versión de la base de datos, hora del servidor y contador de visitas almacenadas.

### 4. Monitorear logs (opcional)
Para revisar el registro de eventos en tiempo real:

```bash
docker compose logs -f
```

### 5. Detener los servicios
Para detener y retirar los contenedores:

```bash
docker compose down
```
*(Si deseas eliminar también los datos almacenados en el volumen de MySQL: `docker compose down -v`)*

---

## 📤 Instrucciones para Vincular y Subir a GitHub

El repositorio local de Git ya ha sido inicializado y configurado en la rama `main` con el commit inicial de todos los archivos del proyecto.

Para subirlo a tu cuenta de GitHub, sigue estos sencillos pasos:

1. Ve a [GitHub](https://github.com/new) y crea un nuevo repositorio (por ejemplo: `practica7-electiva2`). **No** marques la opción de inicializar con README ni `.gitignore` (ya están creados localmente).
2. Abre la terminal en esta carpeta (`practica7-electiva2`) y vincula tu repositorio remoto reemplazando `<TU-USUARIO>` y `<TU-REPOSITORIO>`:

```bash
git remote add origin https://github.com/<TU-USUARIO>/practica7-electiva2.git
```

3. Sube el código a GitHub:

```bash
git push -u origin main
```

4. Copia la URL de tu repositorio de GitHub (por ejemplo: `https://github.com/<TU-USUARIO>/practica7-electiva2`) y pégala en la entrega de la práctica.
