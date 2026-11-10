"""Cliente con datos privados y actualizaciones validadas."""

import re  # Permite comprobar formatos básicos de correo y teléfono.

from .entidad import Entidad  # Hereda identificador y contrato de descripción.
from .excepciones import ValidacionError  # Informa datos inválidos de manera controlada.
from .registro import logger  # Registra eventos sin volcar información personal.
from .validaciones import texto  # Evita duplicar la validación de cadenas.


class Cliente(Entidad):
    """Representa un cliente; el identificador es interno, no una cédula real."""

    def __init__(self, identificador=None, nombre=None, correo=None, telefono=None):
        """Valida cada campo antes de considerar creado el cliente."""
        super().__init__(identificador)  # Delega la validación del identificador a Entidad.
        self.nombre = nombre  # Usa el setter para impedir nombres vacíos.
        self.correo = correo  # Usa el setter para validar correo.
        self.telefono = telefono  # Usa el setter para validar teléfono.
        logger.info("Cliente creado: %s", self.identificador)  # Registra solo la clave interna.

    @property  # Expone lectura controlada del nombre.
    def nombre(self):
        """Devuelve el nombre registrado."""
        return self.__nombre  # Conserva el atributo privado.

    @nombre.setter  # Comprueba toda asignación pública del nombre.
    def nombre(self, valor):
        """Acepta nombres diversos, con un límite de longitud explícito."""
        nuevo = texto(valor, "Nombre")  # No impone un alfabeto que excluya nombres válidos.
        if len(nuevo) > 100:  # Regla de diseño: máximo 100 caracteres.
            raise ValidacionError("Nombre: máximo 100 caracteres.")  # Conserva el valor anterior.
        self.__nombre = nuevo  # Solo cambia el dato después de validarlo.

    @property  # Expone lectura controlada del correo.
    def correo(self):
        """Devuelve el correo registrado."""
        return self.__correo  # No expone un atributo público modificable sin validación.

    @correo.setter  # Valida también las actualizaciones posteriores al registro.
    def correo(self, valor):
        """Comprueba un formato académico básico; no verifica existencia del buzón."""
        nuevo = texto(valor, "Correo")  # Rechaza campos faltantes y caracteres de control.
        if len(nuevo) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+", nuevo):
            raise ValidacionError("Correo: formato inválido.")  # Evita guardar el correo inválido.
        self.__correo = nuevo  # Conserva el correo escrito, sin pasarlo a minúsculas.

    @property  # Expone lectura controlada del teléfono.
    def telefono(self):
        """Devuelve el teléfono en el formato de captura."""
        return self.__telefono  # Mantiene el cero inicial si existe.

    @telefono.setter  # Aplica la misma regla al crear y actualizar.
    def telefono(self, valor):
        """Admite de 7 a 15 dígitos ASCII y un signo + opcional al inicio."""
        nuevo = texto(valor, "Teléfono")  # Exige cadena para preservar ceros iniciales.
        if not re.fullmatch(r"\+?[0-9]{7,15}", nuevo):  # Regla académica, sin consulta externa.
            raise ValidacionError("Teléfono: use de 7 a 15 dígitos, con + inicial opcional.")
        self.__telefono = nuevo  # Asigna únicamente el teléfono válido.

    def describir(self):
        """Sobrescribe el contrato de Entidad sin mostrar datos de contacto."""
        return f"Cliente {self.identificador}: {self.nombre}"  # Descripción para consola.
