"""Tres servicios intercambiables mediante el contrato abstracto Servicio."""

from abc import abstractmethod  # Establece métodos obligatorios para las clases hijas.
from decimal import Decimal, ROUND_HALF_UP  # Trabaja con importes decimales y centavos.

from .entidad import Entidad  # Comparte la abstracción general del sistema.
from .excepciones import CalculoError, ServicioNoDisponibleError, ValidacionError  # Errores propios.
from .registro import logger  # Centraliza eventos y errores.
from .validaciones import entero_positivo, numero, texto  # Reutiliza reglas comunes.


class Servicio(Entidad):
    """Contrato común; toda tarifa de esta implementación es por hora."""

    def __init__(self, identificador=None, nombre=None, tarifa_hora=None):
        """Valida datos comunes; un servicio nuevo comienza disponible."""
        super().__init__(identificador)  # Valida y encapsula la clave interna.
        self.__nombre = texto(nombre, "Nombre del servicio")  # Encapsula el nombre.
        self.__tarifa_hora = numero(tarifa_hora, "Tarifa por hora")  # Exige tarifa positiva.
        self.__disponible = True  # Representa disponibilidad general, sin calendario todavía.

    @property  # Protege el nombre contra cambios sin validación.
    def nombre(self):
        """Devuelve el nombre descriptivo."""
        return self.__nombre  # Mantiene el atributo privado.

    @property  # Expone la tarifa sin permitir su sustitución pública.
    def tarifa_hora(self):
        """Devuelve la tarifa por hora como Decimal."""
        return self.__tarifa_hora  # El llamador no recibe un float monetario.

    @property  # Permite consultar el estado general.
    def disponible(self):
        """Indica si se admite iniciar una operación sobre el servicio."""
        return self.__disponible  # No representa disponibilidad por fecha.

    @disponible.setter  # Controla cambios de estado externos.
    def disponible(self, valor):
        """Acepta exclusivamente valores booleanos."""
        if not isinstance(valor, bool):  # Evita que textos como 'no' se interpreten como True.
            raise ValidacionError("Disponibilidad: debe ser True o False.")  # Informa el error.
        self.__disponible = valor  # Actualiza el estado válido.
        logger.info("Disponibilidad de %s: %s", self.identificador, valor)  # Registra el evento.

    def _validar_disponibilidad(self, otros):
        """Rechaza parámetros desconocidos y servicios deshabilitados."""
        if otros:  # Detecta errores de escritura en parámetros opcionales.
            raise ValidacionError("El servicio recibió parámetros no admitidos.")  # No los ignora.
        if not self.disponible:  # Impide operar con servicios inactivos.
            raise ServicioNoDisponibleError("El servicio está deshabilitado.")  # Error del negocio.

    def _calcular_total(self, duracion, impuesto, descuento, cantidad=1):
        """Aplica descuento, después impuesto y finalmente redondea a centavos."""
        horas = numero(duracion, "Duración")  # Permite horas fraccionarias mayores que cero.
        tasa = numero(impuesto, "Impuesto", incluir_minimo=True, maximo=Decimal("1"))  # Rango 0..1.
        rebaja = numero(descuento, "Descuento", incluir_minimo=True, maximo=Decimal("1"))  # Rango 0..1.
        try:  # Una magnitud extrema puede superar la capacidad del contexto decimal.
            base = self.tarifa_hora * horas * cantidad  # Calcula subtotal antes de ajustes.
            total = base * (Decimal("1") - rebaja) * (Decimal("1") + tasa)  # Aplica las tasas.
            resultado = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # Redondea al final.
        except ArithmeticError as causa:  # Incluye errores aritméticos de Decimal.
            raise CalculoError("No se pudo representar el costo solicitado.") from causa  # Encadena.
        else:  # Solo se ejecuta si el cálculo terminó correctamente.
            logger.info("Costo calculado para %s: %s", self.identificador, resultado)  # Evento válido.
            return resultado  # Devuelve el importe monetario.

    @abstractmethod  # Obliga a sobrescribir el cálculo en cada especialidad.
    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        """Variantes mediante argumentos opcionales; no redefine el mismo nombre varias veces."""

    @abstractmethod  # Cada servicio tiene parámetros propios de reserva.
    def validar_parametros(self, **parametros):
        """Devuelve los parámetros específicos ya validados."""


class ReservaSala(Servicio):
    """Servicio de uso de una sala, limitado por número de personas."""

    def __init__(self, identificador=None, nombre=None, tarifa_hora=None, capacidad=None):
        """La capacidad debe ser un entero positivo."""
        super().__init__(identificador, nombre, tarifa_hora)  # Valida los datos comunes.
        self.__capacidad = entero_positivo(capacidad, "Capacidad")  # Encapsula la capacidad.
        logger.info("Servicio de sala creado: %s", self.identificador)  # Registra creación válida.

    @property  # Solo permite consultar la capacidad validada.
    def capacidad(self):
        """Devuelve el máximo de personas."""
        return self.__capacidad  # Evita cambios sin validación.

    def validar_parametros(self, personas=1, **otros):
        """Una cotización sin parámetros adicionales corresponde a una persona."""
        self._validar_disponibilidad(otros)  # Revisa disponibilidad y argumentos inesperados.
        asistentes = entero_positivo(personas, "Personas")  # No admite cero ni fracciones.
        if asistentes > self.capacidad:  # Comprueba la regla específica de la sala.
            raise ValidacionError("Personas: se supera la capacidad de la sala.")  # Error controlado.
        return {"personas": asistentes}  # Facilita guardar los parámetros en una futura reserva.

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        """La sala se cobra por hora, independientemente de los asistentes admitidos."""
        self.validar_parametros(**parametros)  # Valida antes de cotizar.
        return self._calcular_total(duracion, impuesto, descuento)  # Usa la fórmula común.

    def describir(self):
        """Sobrescribe la descripción con información propia de la sala."""
        return f"Sala {self.nombre}: capacidad {self.capacidad}, tarifa/hora {self.tarifa_hora}"


class AlquilerEquipo(Servicio):
    """Servicio de equipos idénticos, con límite de unidades por operación."""

    def __init__(self, identificador=None, nombre=None, tarifa_hora=None, unidades_disponibles=None):
        """La tarifa corresponde a una unidad durante una hora."""
        super().__init__(identificador, nombre, tarifa_hora)  # Valida los datos comunes.
        self.__unidades = entero_positivo(unidades_disponibles, "Unidades disponibles")  # Stock base.
        logger.info("Servicio de equipos creado: %s", self.identificador)  # Evento de creación.

    @property  # Expone el límite sin permitir sustituciones sin validación.
    def unidades_disponibles(self):
        """Devuelve el máximo por operación; no descuenta reservas en este módulo."""
        return self.__unidades  # La asignación de reservas pertenece a la siguiente parte.

    def validar_parametros(self, unidades=1, **otros):
        """Valida la cantidad solicitada sin modificar el inventario base."""
        self._validar_disponibilidad(otros)  # Comprueba disponibilidad general y parámetros.
        cantidad = entero_positivo(unidades, "Unidades solicitadas")  # Exige cantidad entera.
        if cantidad > self.unidades_disponibles:  # Aplica el límite por operación.
            raise ValidacionError("Unidades: se supera la cantidad disponible.")  # Rechaza exceso.
        return {"unidades": cantidad}  # Entrega una cantidad validada.

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        """Multiplica la tarifa horaria por las unidades solicitadas."""
        datos = self.validar_parametros(**parametros)  # Obtiene la cantidad validada.
        return self._calcular_total(duracion, impuesto, descuento, datos["unidades"])  # Polimorfismo.

    def describir(self):
        """Sobrescribe la descripción para mostrar unidades y tarifa unitaria."""
        return f"Equipo {self.nombre}: unidades {self.unidades_disponibles}, tarifa/unidad/hora {self.tarifa_hora}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría asociado a un área de conocimiento."""

    def __init__(self, identificador=None, nombre=None, tarifa_hora=None, especialidad=None):
        """El área de especialidad es obligatoria."""
        super().__init__(identificador, nombre, tarifa_hora)  # Valida los datos comunes.
        self.__especialidad = texto(especialidad, "Especialidad")  # Encapsula el área de asesoría.
        logger.info("Servicio de asesoría creado: %s", self.identificador)  # Evento válido.

    @property  # Solo permite leer la especialidad ya validada.
    def especialidad(self):
        """Devuelve el área del servicio."""
        return self.__especialidad  # Evita modificaciones externas sin validación.

    def validar_parametros(self, tema=None, **otros):
        """Si no se indica tema, utiliza el área de especialidad como tema general."""
        self._validar_disponibilidad(otros)  # Revisa reglas comunes del servicio.
        asunto = self.especialidad if tema is None else texto(tema, "Tema")  # Valida tema explícito.
        return {"tema": asunto}  # Entrega el tema que podrá conservar la reserva.

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        """Cobra por hora de asesoría dentro de la especialidad configurada."""
        self.validar_parametros(**parametros)  # Valida el tema y la disponibilidad.
        return self._calcular_total(duracion, impuesto, descuento)  # Reutiliza cálculo monetario.

    def describir(self):
        """Sobrescribe la descripción para informar la especialidad."""
        return f"Asesoría {self.nombre}: área {self.especialidad}, tarifa/hora {self.tarifa_hora}"
