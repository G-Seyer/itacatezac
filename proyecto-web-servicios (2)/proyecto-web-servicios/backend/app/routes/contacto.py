"""
Rutas de contacto del sitio.

Este módulo recibe la información enviada desde formularios
como "Contáctanos", "Cotización" o registros similares, y la
reenvía al correo configurado en la aplicación.
"""

import re

from flask import Blueprint, current_app, jsonify, request

from app.services.mail_service import enviar_correo

bp = Blueprint("contacto", __name__)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def limpiar_texto(valor: str, limite: int = 1000) -> str:
    """
    Limpia espacios y recorta longitud máxima.
    """
    if valor is None:
        return ""
    valor = str(valor).strip()
    return valor[:limite]


def correo_valido(correo: str) -> bool:
    """
    Valida formato básico de correo.
    """
    return bool(EMAIL_RE.match(correo or ""))


@bp.route("/contacto", methods=["POST"])
def contacto():
    """
    Recibe datos del formulario de contacto y los envía por correo.
    """
    data = request.get_json(silent=True) or request.form

    nombre = limpiar_texto(data.get("nombre"), 120)
    correo = limpiar_texto(data.get("correo"), 150)
    telefono = limpiar_texto(data.get("telefono"), 50)
    empresa = limpiar_texto(data.get("empresa"), 120)
    servicio = limpiar_texto(data.get("servicio"), 120)
    mensaje_usuario = limpiar_texto(data.get("mensaje"), 3000)

    errores = {}

    if not nombre:
        errores["nombre"] = "El nombre es obligatorio."

    if not correo:
        errores["correo"] = "El correo es obligatorio."
    elif not correo_valido(correo):
        errores["correo"] = "El correo no tiene un formato válido."

    if not mensaje_usuario:
        errores["mensaje"] = "El mensaje es obligatorio."

    if errores:
        return jsonify({
            "ok": False,
            "errores": errores
        }), 400

    asunto = f"[NovaDigital] Nuevo contacto de {nombre}"

    cuerpo = f"""
Se recibió una nueva solicitud de contacto desde el sitio web.

Nombre: {nombre}
Correo: {correo}
Teléfono: {telefono or "No proporcionado"}
Empresa: {empresa or "No proporcionada"}
Servicio de interés: {servicio or "No especificado"}

Mensaje:
{mensaje_usuario}
""".strip()

    try:
        enviar_correo(
            current_app,
            asunto=asunto,
            cuerpo=cuerpo,
            reply_to=correo
        )

        return jsonify({
            "ok": True,
            "mensaje": "Tu solicitud fue enviada correctamente. Pronto nos pondremos en contacto contigo."
        }), 200

    except Exception as exc:
        current_app.logger.error("Error al enviar correo de contacto: %s", exc)

        return jsonify({
            "ok": False,
            "mensaje": "No se pudo enviar la solicitud en este momento. Intenta nuevamente más tarde."
        }), 500