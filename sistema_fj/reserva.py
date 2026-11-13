"""Reserva: une un cliente, un servicio, una duración y un estado.

La lógica de estados la subió Marianita82J-m. Aquí queda en el paquete
y usa las validaciones y los errores que ya existen en el proyecto.
"""

from datetime import datetime  # Conserva la fecha de creación que traía la clase.

from .cliente import Cliente  # Solo se acepta un cliente del sistema.
from .excepciones import ReservaError, ValidacionError  # Errores propios, ya registrados.
from .registro import logger  # Eventos de la reserva, sin datos personales.
from .servicios import Servicio  # Acepta sala, equipo o asesoría.
from .validaciones import numero, texto  # Reutiliza las reglas comunes.


class Reserva:
    """Operación de reserva. Empieza pendiente y cambia solo por sus métodos."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")  # Estados de la clase original.

    def __init__(self, identificador=None, cliente=None, servicio=None, duracion=None):
        """Valida los datos y deja la reserva en estado PENDIENTE."""
        self.__identificador = texto(identificador, "Identificador")  # Clave interna, sin documentos reales.
        if not isinstance(cliente, Cliente):  # Rechaza nulos y objetos de otro tipo.
            raise ValidacionError("Se esperaba un cliente.")  # No guarda una reserva incompleta.
        if not isinstance(servicio, Servicio):  # Rechaza nulos y objetos de otro tipo.
            raise ValidacionError("Se esperaba un servicio.")  # El servicio debe ser una especialidad concreta.
        self.__cliente = cliente  # Conserva el cliente ya validado.
        self.__servicio = servicio  # Conserva el servicio ya validado.
        self.__duracion = numero(duracion, "Duración")  # Exige una duración positiva; admite horas fraccionarias.
        self.__estado = "PENDIENTE"  # Toda reserva nueva espera confirmación.
        self.__fecha_creacion = datetime.now()  # Momento de creación, solo en memoria.
        logger.info("Reserva creada: %s", self.__identificador)  # Registra la clave, no el nombre del cliente.

    @property  # El identificador no se cambia después de crear la reserva.
    def identificador(self):
        """Devuelve la clave interna."""
        return self.__identificador  # No hay setter.

    @property  # Expone el cliente sin permitir sustituirlo.
    def cliente(self):
        """Devuelve el cliente de la reserva."""
        return self.__cliente  # Es el mismo objeto recibido.

    @property  # Expone el servicio sin permitir sustituirlo.
    def servicio(self):
        """Devuelve el servicio reservado."""
        return self.__servicio  # Puede ser sala, equipo o asesoría.

    @property  # La duración ya quedó validada.
    def duracion(self):
        """Devuelve la duración en horas."""
        return self.__duracion  # Es un Decimal positivo.

    @property  # El estado solo cambia en confirmar, cancelar o procesar.
    def estado(self):
        """Devuelve el estado actual."""
        return self.__estado  # No admite una asignación directa.

    @property  # La fecha queda fija desde la creación.
    def fecha_creacion(self):
        """Devuelve el momento en que se creó la reserva."""
        return self.__fecha_creacion  # No se usa como calendario de ocupación.

    def confirmar(self):
        """Pasa de PENDIENTE a CONFIRMADA. Otro estado se rechaza."""
        if self.__estado != "PENDIENTE":  # Evita confirmar dos veces o revivir una reserva cerrada.
            raise ReservaError(f"No se puede confirmar una reserva en estado {self.__estado}.")  # Conserva el estado.
        self.__estado = "CONFIRMADA"  # Solo se actualiza si la transición es válida.
        logger.info("Reserva confirmada: %s", self.__identificador)  # Deja constancia del cambio.

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada. Una procesada no se cancela."""
        if self.__estado == "PROCESADA":  # Una reserva ya procesada queda cerrada.
            raise ReservaError("No se puede cancelar una reserva ya procesada.")  # El estado no cambia.
        if self.__estado == "CANCELADA":  # Cancelar otra vez no es una transición válida.
            raise ReservaError("No se puede cancelar una reserva ya cancelada.")  # Sigue cancelada.
        self.__estado = "CANCELADA"  # Pendiente y confirmada sí pueden cancelarse.
        logger.info("Reserva cancelada: %s", self.__identificador)  # Registra la cancelación.

    def procesar(self):
        """Pasa de CONFIRMADA a PROCESADA. Sin confirmación previa se rechaza."""
        if self.__estado != "CONFIRMADA":  # No procesa pendientes, canceladas ni procesadas.
            raise ReservaError("Solo las reservas confirmadas pueden procesarse.")  # Conserva el estado anterior.
        self.__estado = "PROCESADA"  # Cierra la operación.
        logger.info("Reserva procesada: %s", self.__identificador)  # Registra el cierre.

    def describir(self):
        """Resume la reserva sin mostrar correo ni teléfono."""
        return (f"Reserva {self.__identificador}: cliente {self.__cliente.identificador}, "
                f"servicio {self.__servicio.identificador}, {self.__duracion} h, {self.__estado}")  # Texto de consola.
