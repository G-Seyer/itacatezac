"""
Inicialización principal de la aplicación Flask.

Aquí se crea la app, se cargan configuraciones básicas
y se registran las rutas del proyecto.
"""

import os

from flask import Flask
from dotenv import load_dotenv

# Carga variables desde el archivo .env
load_dotenv()


def create_app():
    """
    Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)

    # =========================
    # CONFIGURACIÓN GENERAL
    # =========================
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_key_segura")

    # =========================
    # CONFIGURACIÓN DE CORREO
    # =========================
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
    app.config["CONTACT_RECEIVER"] = os.getenv("CONTACT_RECEIVER")

    # =========================
    # REGISTRO DE RUTAS
    # =========================
    from app.routes import register_blueprints
    register_blueprints(app)

    # =========================
    # RUTA DE PRUEBA
    # =========================
    @app.route("/")
    def index():
        return {
            "status": "ok",
            "message": "NovaDigital funcionando correctamente"
        }

    return app