"""Configura un log local; una falla del archivo no detiene la aplicación."""

import logging  # Biblioteca estándar para registrar eventos y errores.
from pathlib import Path  # Permite construir rutas en distintos sistemas operativos.

RUTA_LOG = Path(__file__).resolve().parent.parent / "registros" / "sistema_fj.log"  # Log del proyecto.


def obtener_logger():
    """Crea un único manejador, incluso si se importa desde varios módulos."""
    logger = logging.getLogger("sistema_fj")  # Comparte el mismo registrador.
    if logger.handlers:  # Evita repetir cada mensaje por múltiples manejadores.
        return logger  # Reutiliza la configuración existente.
    logger.setLevel(logging.INFO)  # Incluye errores y eventos relevantes.
    logger.propagate = False  # Evita duplicados en el registrador raíz.
    try:  # La carpeta o el archivo pueden no tener permisos de escritura.
        RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta de registros.
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # Escribe texto en UTF-8.
    except OSError:  # Conserva la ejecución si no puede abrirse el archivo.
        manejador = logging.StreamHandler()  # Envía el registro a la consola como respaldo.
        logger.addHandler(manejador)  # Instala el respaldo antes de informar el error.
        logger.exception("No se pudo abrir el archivo de registros; se usará la consola.")  # Guarda causa.
        return logger  # Continúa con el respaldo disponible.
    manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))  # Formato.
    logger.addHandler(manejador)  # Activa la escritura al archivo.
    return logger  # Entrega el registrador configurado.


logger = obtener_logger()  # Inicializa el registro al cargar el módulo.
