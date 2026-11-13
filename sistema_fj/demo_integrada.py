"""Diez operaciones de reserva. Los cinco rechazos no detienen el recorrido.

Los casos salen de la simulación que subió Marianita82J-m. Aquí usan
los clientes y servicios que ya existen en el proyecto.
"""

from .cliente import Cliente  # Cliente con identificador, nombre, correo y teléfono.
from .demo_base import ejecutar_operacion  # Un error no corta las operaciones siguientes.
from .gestor_reservas import GestorReservas  # Lista interna de reservas.
from .registro import RUTA_LOG  # Dónde quedan los eventos y los errores.
from .reserva import Reserva  # Operación que une cliente, servicio y duración.
from .servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Tres servicios reales.


def main():
    """Ejecuta cinco reservas válidas y cinco rechazos. Los datos son ficticios."""
    gestor = GestorReservas()  # Empieza sin reservas.
    cliente1 = Cliente("C001", "Juan Perez", "juan@example.com", "3001234567")  # Primer cliente ficticio.
    cliente2 = Cliente("C002", "Maria Lopez", "maria@example.com", "3001234568")  # Segundo cliente ficticio.
    sala = ReservaSala("S001", "Sala A", "50000", 10)  # Sala con capacidad de diez personas.
    equipo = AlquilerEquipo("E001", "Portatil", "30000", 3)  # Equipo con tres unidades.
    asesoria = AsesoriaEspecializada("A001", "Asesoria Python", "80000", "Python")  # Asesoría del área Python.

    def completar(identificador, cliente, servicio, duracion):
        """Crea, confirma, procesa y guarda una reserva válida."""
        reserva = Reserva(identificador, cliente, servicio, duracion)  # Nace en estado PENDIENTE.
        reserva.confirmar()  # Pasa a CONFIRMADA.
        reserva.procesar()  # Pasa a PROCESADA.
        return gestor.agregar_reserva(reserva)  # Queda en la lista interna.

    operaciones = [  # Cinco aciertos y cinco rechazos, en ese orden.
        ("Reserva válida de sala", lambda: completar("R001", cliente1, sala, 2)),
        ("Reserva válida de equipo", lambda: completar("R002", cliente2, equipo, 1)),
        ("Reserva válida de asesoría", lambda: completar("R003", cliente1, asesoria, 3)),
        ("Segunda reserva válida de sala", lambda: completar("R004", cliente2, sala, 4)),
        ("Segunda reserva válida de equipo", lambda: completar("R005", cliente1, equipo, 5)),
        ("Rechazar reserva sin cliente", lambda: Reserva("R006", None, sala, 2)),
        ("Rechazar reserva sin servicio", lambda: Reserva("R007", cliente1, None, 2)),
        ("Rechazar duración negativa", lambda: Reserva("R008", cliente1, sala, -5)),
        ("Rechazar duración cero", lambda: Reserva("R009", cliente1, sala, 0)),
        ("Rechazar procesar sin confirmar", lambda: Reserva("R010", cliente1, sala, 1).procesar()),
    ]  # Termina la lista de las diez operaciones.
    print("SOFTWARE FJ - reservas integradas con clientes y servicios")  # Aclara que ya hay reservas.
    exitos = 0  # Cuenta las operaciones que terminan bien.
    for numero, (titulo, accion) in enumerate(operaciones, start=1):  # Recorre las diez en orden.
        if ejecutar_operacion(numero, titulo, accion):  # Si falla, sigue con la siguiente.
            exitos += 1  # Solo cuenta las que no lanzaron error.
    print(f"\nResumen: {exitos} correctas, {len(operaciones) - exitos} rechazadas, {len(operaciones)} ejecutadas.")
    print(f"Reservas en memoria: {len(gestor.listar_reservas())}.")  # Deben quedar las cinco válidas.
    print(f"Log habitual: {RUTA_LOG}")  # El mismo archivo del resto del sistema.
    return gestor  # Permite revisar el resultado desde las pruebas.


if __name__ == "__main__":  # No ejecuta la demo cuando otro módulo la importa.
    main()  # Arranca el recorrido con python3 -m sistema_fj.demo_integrada.
