"""Lista interna de reservas. No guarda el negocio en archivos."""

from .excepciones import DuplicadoError, ValidacionError  # Rechaza tipos y claves repetidas.
from .registro import logger  # Registra solo altas válidas.
from .reserva import Reserva  # Único tipo que entra en la lista.


class GestorReservas:
    """Conserva las reservas en memoria hasta que termina el programa."""

    def __init__(self):
        """Cada gestor empieza sin reservas."""
        self.__reservas = []  # Lista privada. Quien llama no la modifica directo.

    def agregar_reserva(self, reserva):
        """Guarda una reserva si su identificador no está repetido."""
        if not isinstance(reserva, Reserva):  # Evita meter otros objetos en la lista.
            raise ValidacionError("Se esperaba una reserva.")  # No agrega nada.
        for registrada in self.__reservas:  # Revisa las claves ya guardadas.
            if registrada.identificador == reserva.identificador:  # La clave debe ser única.
                raise DuplicadoError("El identificador ya está registrado en este gestor.")  # La lista no crece.
        self.__reservas.append(reserva)  # Solo entra una reserva válida y nueva.
        logger.info("Reserva registrada: %s", reserva.identificador)  # Confirma el alta.
        return reserva  # Permite seguir usando la misma reserva.

    def listar_reservas(self):
        """Devuelve una copia de solo lectura de las reservas."""
        return tuple(self.__reservas)  # La lista privada permanece dentro del gestor.

    def buscar_por_estado(self, estado):
        """Devuelve las reservas que están en el estado indicado."""
        return tuple(reserva for reserva in self.__reservas if reserva.estado == estado)  # No modifica la lista.
