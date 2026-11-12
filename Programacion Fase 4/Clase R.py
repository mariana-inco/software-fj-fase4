from datetime import datetime


class Reserva:
    ESTADOS_VALIDOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"]

    def __init__(self, cliente, servicio, duracion):
        if cliente is None:
            raise ValueError("El cliente no puede ser nulo")

        if servicio is None:
            raise ValueError("El servicio no puede ser nulo")

        if duracion <= 0:
            raise ValueError("La duración debe ser mayor que cero")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._fecha_creacion = datetime.now()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise Exception(
                f"No se puede confirmar una reserva en estado {self._estado}"
            )

        self._estado = "CONFIRMADA"

    def cancelar(self):
        if self._estado == "PROCESADA":
            raise Exception(
                "No se puede cancelar una reserva ya procesada"
            )

        self._estado = "CANCELADA"

    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise Exception(
                "Solo las reservas confirmadas pueden procesarse"
            )

        self._estado = "PROCESADA"

    def __str__(self):
        return (
            f"Reserva(cliente={self._cliente}, "
            f"servicio={self._servicio}, "
            f"duracion={self._duracion}, "
            f"estado={self._estado})"
        )