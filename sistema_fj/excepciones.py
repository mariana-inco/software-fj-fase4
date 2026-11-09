"""Errores del dominio; registrarlos aquí evita olvidar los errores controlados."""

from .registro import logger  # Reutiliza el log del proyecto.


class ErrorSoftwareFJ(Exception):
    """Excepción base que permite capturar todos los errores del negocio."""

    def __init__(self, mensaje):
        """Conserva el mensaje y registra el tipo de error, sin datos personales."""
        super().__init__(mensaje)  # Inicializa la excepción estándar.
        logger.error("%s: %s", type(self).__name__, mensaje)  # Registra cada error detectado.


class ValidacionError(ErrorSoftwareFJ):
    """Un dato tiene un formato o un valor no permitido."""


class DuplicadoError(ErrorSoftwareFJ):
    """Ya existe un objeto con ese identificador en su lista."""


class NoEncontradoError(ErrorSoftwareFJ):
    """No existe el identificador solicitado."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio está temporalmente deshabilitado."""


class ReservaError(ErrorSoftwareFJ):
    """Base disponible para que la compañera implemente errores de reservas."""


class CalculoError(ErrorSoftwareFJ):
    """El importe no puede representarse con la precisión monetaria elegida."""
