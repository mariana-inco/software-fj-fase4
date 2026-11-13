"""Lista interna de reservas. No guarda el negocio en archivos."""

from .excepciones import DuplicadoError, ReservaError, ValidacionError  # Rechaza tipos, claves y cupos.
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

    def confirmar(self, reserva):
        """Confirma si queda cupo. Una sala o asesoría admite una reserva activa; el equipo, su stock."""
        if reserva.estado != "PENDIENTE":  # Una confirmación repetida no ocupa nada nuevo.
            reserva.confirmar()  # Lanza el error y conserva el estado.
        self._exigir_cupo(reserva)  # Mira las confirmadas antes de cambiar el estado.
        reserva.confirmar()  # Pasa a CONFIRMADA solo si el servicio sigue disponible.
        return reserva  # La misma reserva, ya confirmada.

    def _exigir_cupo(self, reserva):
        """Suma lo que ya está confirmado para el mismo servicio. No modifica reservas."""
        activas = [otra for otra in self.__reservas  # Solo las que retienen el recurso.
                   if otra is not reserva and otra.estado == "CONFIRMADA"
                   and otra.servicio.identificador == reserva.servicio.identificador]
        if "unidades" in reserva.parametros:  # El equipo se controla por stock acumulado.
            ocupadas = sum(otra.parametros["unidades"] for otra in activas)  # Unidades ya confirmadas.
            pedidas = reserva.parametros["unidades"]  # Unidades de esta reserva.
            if ocupadas + pedidas > reserva.servicio.unidades_disponibles:  # No pasa del stock.
                raise ReservaError("Unidades: no hay stock suficiente para otra reserva confirmada.")
        elif activas:  # Sala y asesoría: una sola reserva confirmada a la vez.
            raise ReservaError("El servicio ya tiene una reserva confirmada.")  # Esta sigue pendiente.
