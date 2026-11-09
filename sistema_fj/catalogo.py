"""Almacenamiento exclusivamente en listas; no lee ni escribe datos del negocio."""

from .cliente import Cliente  # Define el tipo permitido en la lista de clientes.
from .excepciones import DuplicadoError, NoEncontradoError, ValidacionError  # Errores de catálogo.
from .registro import logger  # Registra las altas exitosas.
from .servicios import Servicio  # Permite cualquier subclase concreta del contrato.
from .validaciones import texto  # Valida claves de búsqueda.


class Catalogo:
    """Mantiene clientes y servicios hasta que termina el proceso de Python."""

    def __init__(self):
        """Cada catálogo comienza sin datos."""
        self.__clientes = []  # Lista privada de objetos Cliente.
        self.__servicios = []  # Lista privada de objetos Servicio.

    @property  # Evita que un llamador agregue objetos sin pasar por registrar_cliente.
    def clientes(self):
        """Entrega una vista inmutable de las referencias registradas."""
        return tuple(self.__clientes)  # Conserva la lista original dentro del catálogo.

    @property  # Protege la estructura de la lista de servicios.
    def servicios(self):
        """Entrega los servicios mediante una tupla."""
        return tuple(self.__servicios)  # No copia ni persiste los objetos.

    def _registrar(self, objeto, tipo, lista):
        """Comparte controles de tipo e identificador duplicado."""
        if not isinstance(objeto, tipo):  # Evita mezclar clientes con servicios u otros objetos.
            raise ValidacionError(f"Se esperaba un objeto {tipo.__name__}.")  # Error controlado.
        for registrado in lista:  # Revisa uno por uno los objetos guardados.
            if registrado.identificador == objeto.identificador:  # Compara sus identificadores.
                raise DuplicadoError("El identificador ya está registrado en este catálogo.")
        lista.append(objeto)  # Guarda el objeto únicamente en memoria.
        logger.info("%s registrado: %s", tipo.__name__, objeto.identificador)  # Confirma alta.
        return objeto  # Permite usar de inmediato el objeto registrado.

    def registrar_cliente(self, cliente):
        """Agrega un cliente válido, sin repetir su identificador."""
        return self._registrar(cliente, Cliente, self.__clientes)  # Delega controles comunes.

    def registrar_servicio(self, servicio):
        """Agrega cualquier especialidad de Servicio válida."""
        return self._registrar(servicio, Servicio, self.__servicios)  # Admite polimorfismo.

    def _buscar(self, identificador, lista):
        """Busca por clave estable y distingue ausencia de entrada inválida."""
        clave = texto(identificador, "Identificador de búsqueda")  # Comprueba el parámetro.
        for objeto in lista:  # Recorre los objetos almacenados en memoria.
            if objeto.identificador == clave:  # Compara claves normalizadas.
                return objeto  # Devuelve la misma instancia registrada.
        raise NoEncontradoError("No existe un objeto con el identificador indicado.")  # Sin coincidencia.

    def buscar_cliente(self, identificador):
        """Obtiene un cliente para integrarlo con la futura clase Reserva."""
        return self._buscar(identificador, self.__clientes)  # Consulta la lista de clientes.

    def buscar_servicio(self, identificador):
        """Obtiene un servicio para calcular costos o crear una reserva."""
        return self._buscar(identificador, self.__servicios)  # Consulta la lista de servicios.
