"""
Registro central de blueprints de la aplicación.

Este archivo concentra la carga de todas las rutas del proyecto.
La idea es que, conforme vayas llenando archivos dentro de app/routes,
solamente tengas que importarlos aquí y registrarlos en la app Flask.
"""

from importlib import import_module
from typing import Iterable

# Lista de módulos de rutas a registrar.
# Conforme agregues más archivos en app/routes, inclúyelos aquí.
ROUTE_MODULES: Iterable[str] = (
    "app.routes.contacto",
)


def register_blueprints(app) -> None:
    """
    Importa y registra todos los blueprints disponibles en la aplicación.

    Si algún módulo todavía está vacío o no tiene un blueprint llamado `bp`,
    simplemente se omite para no romper el arranque del proyecto mientras
    sigues desarrollándolo.
    """
    for module_path in ROUTE_MODULES:
        try:
            module = import_module(module_path)
            blueprint = getattr(module, "bp", None)

            if blueprint is not None:
                app.register_blueprint(blueprint)
            else:
                app.logger.warning(
                    "El módulo '%s' no define un blueprint llamado 'bp'.",
                    module_path,
                )

        except Exception as exc:
            app.logger.warning(
                "No se pudo registrar el módulo de rutas '%s': %s",
                module_path,
                exc,
            )