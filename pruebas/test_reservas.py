"""Pruebas cortas de los estados de Reserva y de la lista del gestor."""

import io  # Captura la demo sin llenar la consola.
import unittest  # Ejecuta las pruebas con la biblioteca estándar.
from contextlib import redirect_stdout  # Aísla la salida de la simulación.
from decimal import Decimal  # Compara el costo sin tolerancia de punto flotante.

from sistema_fj.cliente import Cliente  # Cliente real del proyecto.
from sistema_fj.demo_integrada import main  # Recorrido completo.
from sistema_fj.excepciones import DuplicadoError, ReservaError, ServicioNoDisponibleError  # Errores esperados.
from sistema_fj.excepciones import ValidacionError  # Datos que no se pueden guardar.
from sistema_fj.gestor_reservas import GestorReservas  # Lista interna y cupo.
from sistema_fj.reserva import Reserva  # Clase organizada a partir del aporte de la compañera.
from sistema_fj.servicios import AlquilerEquipo, ReservaSala  # Sala y equipo para cupo y costo.


class PruebasReservas(unittest.TestCase):
    """Comprueba transiciones y que un rechazo no guarde la reserva."""

    def setUp(self):
        """Prepara un cliente, una sala y un gestor vacíos."""
        self.cliente = Cliente("C1", "Ana", "ana@example.com", "3001234567")  # Datos ficticios.
        self.sala = ReservaSala("S1", "Sala", "50000", 10)  # Capacidad conocida.
        self.gestor = GestorReservas()  # Sin reservas al empezar.

    def test_ciclo_confirmar_y_procesar(self):
        """Una reserva válida pasa de pendiente a confirmada y luego a procesada."""
        reserva = Reserva("R1", self.cliente, self.sala, 2)  # Dos horas.
        self.assertEqual(reserva.estado, "PENDIENTE")  # El estado inicial no se elige por fuera.
        reserva.confirmar()  # Primera transición válida.
        self.assertEqual(reserva.estado, "CONFIRMADA")  # Quedó confirmada.
        reserva.procesar()  # Segunda transición válida.
        self.assertEqual(reserva.estado, "PROCESADA")  # Quedó cerrada.

    def test_procesar_sin_confirmar_conserva_estado(self):
        """Procesar una reserva pendiente falla y la deja pendiente."""
        reserva = Reserva("R1", self.cliente, self.sala, 1)  # Todavía no está confirmada.
        with self.assertRaises(ReservaError):  # La transición no está permitida.
            reserva.procesar()  # Intenta saltarse la confirmación.
        self.assertEqual(reserva.estado, "PENDIENTE")  # El estado anterior se conserva.

    def test_no_repite_confirmacion_ni_cancela_procesada(self):
        """Una confirmación repetida y una cancelación final se rechazan."""
        reserva = Reserva("R1", self.cliente, self.sala, 1)  # Reserva de una hora.
        reserva.confirmar()  # Queda confirmada.
        with self.assertRaises(ReservaError):  # No se confirma dos veces.
            reserva.confirmar()  # Segunda confirmación.
        self.assertEqual(reserva.estado, "CONFIRMADA")  # Sigue confirmada.
        reserva.procesar()  # Pasa al estado final.
        with self.assertRaises(ReservaError):  # Una procesada no se cancela.
            reserva.cancelar()  # Intento de cancelación.
        self.assertEqual(reserva.estado, "PROCESADA")  # El estado final no cambió.

    def test_duplicado_no_aumenta_la_lista(self):
        """La segunda reserva con la misma clave no entra al gestor."""
        reserva = Reserva("R1", self.cliente, self.sala, 1)  # Primera reserva.
        self.gestor.agregar_reserva(reserva)  # Alta válida.
        with self.assertRaises(DuplicadoError):  # La clave ya existe.
            self.gestor.agregar_reserva(Reserva("R1", self.cliente, self.sala, 2))  # Otra con el mismo id.
        self.assertEqual(len(self.gestor.listar_reservas()), 1)  # La lista sigue con una sola.

    def test_cliente_o_duracion_invalidos_no_crean_reserva(self):
        """Sin cliente o con duración no positiva no queda una reserva a medias."""
        with self.assertRaises(ValidacionError):  # El cliente es obligatorio.
            Reserva("R1", None, self.sala, 1)  # Cliente nulo.
        with self.assertRaises(ValidacionError):  # Cero no es una duración.
            Reserva("R2", self.cliente, self.sala, 0)  # Duración inválida.

    def test_costo_capacidad_disponibilidad_y_cupo(self):
        """El costo queda guardado, y un rechazo de cupo o de disponibilidad no confirma."""
        reserva = Reserva("R1", self.cliente, self.sala, 2, impuesto="0.19", personas=4)  # Cuatro personas, dos horas.
        self.assertEqual(reserva.costo, Decimal("119000.00"))  # 50000 × 2 × 1.19. Las personas no cambian el precio.
        with self.assertRaises(ValidacionError):  # Once personas superan la capacidad.
            Reserva("R2", self.cliente, self.sala, 1, personas=11)  # No llega a crearse.
        self.gestor.agregar_reserva(reserva)  # Entra pendiente.
        self.gestor.confirmar(reserva)  # Ocupa la sala.
        otra = Reserva("R3", self.cliente, self.sala, 1)  # Otra reserva de la misma sala.
        self.gestor.agregar_reserva(otra)  # Puede existir pendiente.
        with self.assertRaises(ReservaError):  # La sala ya tiene una confirmada.
            self.gestor.confirmar(otra)  # No debe ocupar la sala.
        self.assertEqual(otra.estado, "PENDIENTE")  # El rechazo no la confirma.
        self.assertEqual(reserva.estado, "CONFIRMADA")  # La primera sigue ocupando la sala.
        reserva.cancelar()  # Liberar permite confirmar la otra.
        self.gestor.confirmar(otra)  # Ahora sí hay cupo.
        self.assertEqual(otra.estado, "CONFIRMADA")  # Quedó confirmada después de liberar.

        equipo = AlquilerEquipo("E1", "Portatil", "10000", 3)  # Stock de tres unidades.
        primera = Reserva("E-R1", self.cliente, equipo, 1, unidades=2)  # Pide dos.
        segunda = Reserva("E-R2", self.cliente, equipo, 1, unidades=2)  # Otras dos no caben junto a las primeras.
        self.gestor.agregar_reserva(primera)  # Guarda la primera.
        self.gestor.confirmar(primera)  # Ocupa dos unidades.
        self.gestor.agregar_reserva(segunda)  # La segunda espera.
        with self.assertRaises(ReservaError):  # 2 + 2 superan las 3 disponibles.
            self.gestor.confirmar(segunda)  # No confirma y no descuenta de más.
        self.assertEqual(segunda.estado, "PENDIENTE")  # Sigue pendiente.
        primera.procesar()  # Procesar libera las unidades.
        equipo.disponible = False  # El equipo sale de servicio.
        with self.assertRaises(ServicioNoDisponibleError):  # No se confirma apagado.
            self.gestor.confirmar(segunda)  # Hay stock, pero el servicio está apagado.
        self.assertEqual(segunda.estado, "PENDIENTE")  # El estado anterior se conserva.

    def test_demo_completa(self):
        """La simulación recorre 12 operaciones y confirma una reserva después de los errores."""
        salida = io.StringIO()  # Guarda el texto de la demo.
        with redirect_stdout(salida):  # No mezcla la demo con el resultado de la prueba.
            gestor = main()  # Ejecuta clientes, servicios y reservas.
        self.assertIn("6 correctas, 6 rechazadas, 12 ejecutadas", salida.getvalue())  # El recorrido no se detuvo.
        estados = {reserva.identificador: reserva.estado for reserva in gestor.listar_reservas()}  # Resultado final.
        self.assertEqual(estados["R001"], "CANCELADA")  # La primera sala se liberó.
        self.assertEqual(estados["R003"], "CONFIRMADA")  # Esta se confirmó después de los errores.
        self.assertEqual(estados["R005"], "PENDIENTE")  # El equipo apagado no llegó a confirmarse.


if __name__ == "__main__":  # Permite ejecutar solo este archivo.
    unittest.main()  # Inicia el ejecutor estándar.
