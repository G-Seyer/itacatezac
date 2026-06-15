"""
Servicio de envío de correos.

Centraliza la lógica SMTP del proyecto para que las rutas
solo se encarguen de recibir y validar datos.
"""

import smtplib
from email.message import EmailMessage


def enviar_correo(app, asunto: str, cuerpo: str, reply_to: str | None = None) -> None:
    """
    Envía un correo de texto plano usando la configuración SMTP
    definida en la aplicación Flask.

    Args:
        app: Instancia de la app Flask o current_app.
        asunto: Asunto del correo.
        cuerpo: Contenido del correo.
        reply_to: Correo al que se responderá directamente.

    Raises:
        ValueError: Si faltan variables de configuración obligatorias.
        Exception: Si ocurre un error durante el envío SMTP.
    """
    mail_server = app.config.get("MAIL_SERVER")
    mail_port = app.config.get("MAIL_PORT")
    mail_use_tls = app.config.get("MAIL_USE_TLS")
    mail_username = app.config.get("MAIL_USERNAME")
    mail_password = app.config.get("MAIL_PASSWORD")
    mail_default_sender = app.config.get("MAIL_DEFAULT_SENDER")
    contact_receiver = app.config.get("CONTACT_RECEIVER")

    if not all([
        mail_server,
        mail_port,
        mail_username,
        mail_password,
        mail_default_sender,
        contact_receiver,
    ]):
        raise ValueError(
            "Faltan variables de configuración del correo. "
            "Revisa MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, "
            "MAIL_PASSWORD, MAIL_DEFAULT_SENDER y CONTACT_RECEIVER."
        )

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = mail_default_sender
    mensaje["To"] = contact_receiver

    if reply_to:
        mensaje["Reply-To"] = reply_to

    mensaje.set_content(cuerpo)

    with smtplib.SMTP(mail_server, mail_port) as servidor:
        if mail_use_tls:
            servidor.starttls()
        servidor.login(mail_username, mail_password)
        servidor.send_message(mensaje)