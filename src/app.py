import os
import time
from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

# Configuración obtenida mediante variables de entorno
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "usuario_practica")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")
DB_NAME = os.getenv("DB_NAME", "practica7_db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

def get_db_connection():
    """Establece conexión a la base de datos MySQL con reintentos."""
    retries = 10
    while retries > 0:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                connect_timeout=5,
                autocommit=True
            )
            return conn, None
        except pymysql.MySQLError as e:
            retries -= 1
            if retries == 0:
                return None, str(e)
            time.sleep(2)
    return None, "Tiempo de espera agotado al conectar a MySQL."

def init_and_query_db(conn):
    """Crea tabla de prueba si no existe, inserta un registro y consulta estadísticas."""
    with conn.cursor() as cursor:
        # 1. Crear tabla de registros de prueba
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registro_saludos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mensaje VARCHAR(255) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Insertar un saludo para verificar escritura
        cursor.execute("""
            INSERT INTO registro_saludos (mensaje)
            VALUES ('¡Hola Mundo desde MySQL y Docker Compose!');
        """)

        # 3. Consultar total de registros
        cursor.execute("SELECT COUNT(*) FROM registro_saludos;")
        total_registros = cursor.fetchone()[0]

        # 4. Consultar versión y fecha/hora del motor MySQL
        cursor.execute("SELECT VERSION(), NOW();")
        version, current_time = cursor.fetchone()

        return {
            "version": version,
            "current_time": str(current_time),
            "total_registros": total_registros
        }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Práctica 7 - Hola Mundo con Docker Compose y MySQL</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #334155;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            max-width: 580px;
            width: 100%;
            padding: 40px 32px;
            text-align: center;
        }
        .icon {
            font-size: 3rem;
            margin-bottom: 12px;
        }
        h1 {
            color: #0f172a;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .subtitle {
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 24px;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.92rem;
            margin-bottom: 24px;
        }
        .badge-success {
            background-color: #dcfce7;
            color: #15803d;
            border: 1px solid #bbf7d0;
        }
        .badge-danger {
            background-color: #fee2e2;
            color: #b91c1c;
            border: 1px solid #fecaca;
        }
        .pulse {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: currentColor;
            display: inline-block;
        }
        .info-card {
            background: #f8fafc;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            overflow: hidden;
            text-align: left;
            margin-bottom: 24px;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 18px;
            border-bottom: 1px solid #e2e8f0;
            font-size: 0.92rem;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            color: #64748b;
            font-weight: 500;
        }
        .info-value {
            color: #0f172a;
            font-weight: 600;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }
        .banner-success {
            background-color: #f0fdf4;
            border: 1px solid #86efac;
            color: #166534;
            padding: 12px;
            border-radius: 8px;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        .error-box {
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 14px;
            border-radius: 8px;
            font-size: 0.88rem;
            text-align: left;
            margin-bottom: 20px;
            word-break: break-all;
        }
        .footer {
            font-size: 0.82rem;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            padding-top: 18px;
        }
        .tech-pill {
            background: #e2e8f0;
            color: #334155;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-block;
            margin: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🚀</div>
        <h1>¡Hola Mundo!</h1>
        <p class="subtitle">Práctica 7 - Electiva II &bull; Docker Compose &amp; MySQL</p>

        {% if success %}
            <div class="badge badge-success">
                <span class="pulse"></span>
                <span>Conexión exitosa a MySQL</span>
            </div>

            <div class="banner-success">
                ✓ Se comprobó lectura y escritura en la base de datos satisfactoriamente.
            </div>

            <div class="info-card">
                <div class="info-row">
                    <span class="info-label">Host de la BD:</span>
                    <span class="info-value">{{ db_host }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Nombre de Base de Datos:</span>
                    <span class="info-value">{{ db_name }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Motor y Versión:</span>
                    <span class="info-value">MySQL {{ db_version }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Hora del Servidor MySQL:</span>
                    <span class="info-value">{{ db_time }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Peticiones / Registros en BD:</span>
                    <span class="info-value">{{ total_registros }}</span>
                </div>
            </div>
        {% else %}
            <div class="badge badge-danger">
                <span class="pulse"></span>
                <span>Error al conectar con MySQL</span>
            </div>
            <div class="error-box">
                <strong>Detalles del error:</strong><br>
                {{ error_msg }}
            </div>
        {% endif %}

        <div class="footer">
            Stack:
            <span class="tech-pill">Docker Compose</span>
            <span class="tech-pill">Python 3.11</span>
            <span class="tech-pill">Flask</span>
            <span class="tech-pill">MySQL 8.0</span>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def hola_mundo():
    conn, error_msg = get_db_connection()
    if conn:
        try:
            db_data = init_and_query_db(conn)
            return render_template_string(
                HTML_TEMPLATE,
                success=True,
                db_host=DB_HOST,
                db_name=DB_NAME,
                db_version=db_data["version"],
                db_time=db_data["current_time"],
                total_registros=db_data["total_registros"]
            )
        except Exception as e:
            return render_template_string(
                HTML_TEMPLATE,
                success=False,
                error_msg=f"Error durante las operaciones en BD: {str(e)}"
            ), 500
        finally:
            conn.close()
    else:
        return render_template_string(
            HTML_TEMPLATE,
            success=False,
            error_msg=error_msg
        ), 500

if __name__ == '__main__':
    # Flask escucha en todas las interfaces de red del contenedor
    app.run(host='0.0.0.0', port=5000)
