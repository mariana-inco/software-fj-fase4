"""Abstracción compartida por clientes y servicios."""

from abc import ABC, abstractmethod  # Prohíbe instanciar clases abstractas incompletas.

from .validaciones import texto  # Comparte las reglas de texto.


class Entidad(ABC):
    """Define identificador de solo lectura y un contrato de descripción."""

    def __init__(self, identificador=None):
        """El valor por defecto permite detectar explícitamente parámetros faltantes."""
        self.__identificador = texto(identificador, "Identificador")  # Encapsula el identificador.

    @property  # Permite leer, pero no sustituir el identificador mediante la interfaz pública.
    def identificador(self):
        """Devuelve la clave estable que usan las listas internas."""
        return self.__identificador  # No ofrece setter.

    @abstractmethod  # Cada clase concreta debe explicar cómo se describe.
    def describir(self):
        """Devuelve una descripción legible de la entidad."""
