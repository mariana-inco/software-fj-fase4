"""Recorrido completo: clientes, servicios y reservas, con un acierto después de los errores."""

from .cliente import Cliente  # Cliente con identificador, nombre, correo y teléfono.
from .demo_base import ejecutar_operacion  # Un error no corta las operaciones siguientes.
from .gestor_reservas import GestorReservas  # Lista interna y control de cupo.
from .registro import RUTA_LOG  # Dónde quedan los eventos y los errores.
from .reserva import Reserva  # Operación que une cliente, servicio, duración y costo.
from .servicios import AlquilerEquipo, ReservaSala  # Servicios usados en este recorrido.


def main():
    """Ejecuta 12 operaciones. Los datos son ficticios y los rechazos son intencionales."""
    gestor = GestorReservas()  # Empieza sin reservas.
    creados = {}  # Guarda los objetos que las operaciones siguientes reutilizan.

    def guardar(clave, objeto):
        """Recuerda un objeto válido para usarlo más adelante."""
        creados[clave] = objeto  # Queda solo en memoria.
        return objeto  # La demo puede describirlo.

    def confirmar_nueva(identificador, cliente, servicio, duracion, **parametros):
        """Crea la reserva, la guarda y la confirma si hay cupo."""
        reserva = Reserva(identificador, cliente, servicio, duracion, **parametros)  # Nace pendiente.
        gestor.agregar_reserva(reserva)  # Entra a la lista antes de ocupar el servicio.
        gestor.confirmar(reserva)  # Ocupa solo si el cupo y la disponibilidad alcanzan.
        return reserva  # Confirmada, con el costo ya calculado.

    def segunda_sala():
        """Intenta confirmar otra sala mientras la primera sigue confirmada."""
        reserva = Reserva("R003", creados["cliente"], creados["sala"], 1, personas=2)  # Cabe en la capacidad.
        gestor.agregar_reserva(reserva)  # Queda pendiente aunque la confirmación falle.
        creados["pendiente"] = reserva  # Se confirmará cuando la primera se cancele.
        return gestor.confirmar(reserva)  # Debe rechazarse: la sala ya está ocupada.

    def equipo_apagado():
        """Crea la reserva con el equipo encendido y confirma cuando ya está apagado."""
        reserva = Reserva("R005", creados["cliente"], creados["equipo"], 1, unidades=1)  # El costo sí se calcula.
        gestor.agregar_reserva(reserva)  # Todavía no ocupa stock.
        creados["equipo"].disponible = False  # Simula que el equipo sale de servicio.
        return gestor.confirmar(reserva)  # Falla y la reserva sigue pendiente.

    operaciones = [  # El último caso es un acierto, después de los rechazos.
        ("Registrar cliente válido", lambda: guardar(
            "cliente", Cliente("C001", "Juan Perez", "juan@example.com", "3001234567"))),
        ("Rechazar cliente con correo inválido", lambda: Cliente(
            "C002", "Ana Ruiz", "sin-arroba", "3001234567")),
        ("Registrar sala válida", lambda: guardar(
            "sala", ReservaSala("S001", "Sala A", "50000", 10))),
        ("Rechazar sala sin capacidad", lambda: ReservaSala("S002", "Sala B", "50000", 0)),
        ("Registrar equipo válido", lambda: guardar(
            "equipo", AlquilerEquipo("E001", "Portatil", "10000", 3))),
        ("Confirmar reserva de sala", lambda: guardar(
            "sala_reserva", confirmar_nueva("R001", creados["cliente"], creados["sala"], 2, personas=4))),
        ("Rechazar sala con demasiadas personas", lambda: Reserva(
            "R002", creados["cliente"], creados["sala"], 1, personas=11)),
        ("Rechazar segunda sala mientras la primera está confirmada", segunda_sala),
        ("Rechazar duración cero", lambda: Reserva("R004", creados["cliente"], creados["sala"], 0)),
        ("Rechazar confirmación de equipo apagado", equipo_apagado),
        ("Cancelar la sala confirmada y liberarla", lambda: creados["sala_reserva"].cancelar()),
        ("Confirmar la sala pendiente después de los errores", lambda: gestor.confirmar(creados["pendiente"])),
    ]  # Doce operaciones: aciertos, rechazos y un acierto final.
    print("SOFTWARE FJ - simulación completa de clientes, servicios y reservas")  # Alcance de este recorrido.
    exitos = 0  # Cuenta las operaciones que terminan bien.
    for numero, (titulo, accion) in enumerate(operaciones, start=1):  # Recorre las doce en orden.
        if ejecutar_operacion(numero, titulo, accion):  # Si falla, sigue con la siguiente.
            exitos += 1  # Solo cuenta las que no lanzaron error.
    print(f"\nResumen: {exitos} correctas, {len(operaciones) - exitos} rechazadas, {len(operaciones)} ejecutadas.")
    print(f"Reservas en memoria: {len(gestor.listar_reservas())}.")  # Incluye confirmadas, canceladas y pendientes.
    print(f"Log habitual: {RUTA_LOG}")  # El mismo archivo del resto del sistema.
    return gestor  # Permite revisar el resultado desde las pruebas.


if __name__ == "__main__":  # No ejecuta la demo cuando otro módulo la importa.
    main()  # Arranca el recorrido con python3 -m sistema_fj.demo_integrada.
