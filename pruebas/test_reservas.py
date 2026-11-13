"""Pruebas cortas de los estados de Reserva y de la lista del gestor."""

import io  # Captura la demo sin llenar la consola.
import unittest  # Ejecuta las pruebas con la biblioteca estándar.
from contextlib import redirect_stdout  # Aísla la salida de la simulación.

from sistema_fj.cliente import Cliente  # Cliente real del proyecto.
from sistema_fj.demo_integrada import main  # Recorrido de diez operaciones.
from sistema_fj.excepciones import DuplicadoError, ReservaError, ValidacionError  # Errores esperados.
from sistema_fj.gestor_reservas import GestorReservas  # Lista interna.
from sistema_fj.reserva import Reserva  # Clase organizada a partir del aporte de la compañera.
from sistema_fj.servicios import ReservaSala  # Un servicio concreto basta para estos casos.


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

    def test_demo_de_diez_operaciones(self):
        """La simulación completa diez operaciones y guarda solo las cinco válidas."""
        salida = io.StringIO()  # Guarda el texto de la demo.
        with redirect_stdout(salida):  # No mezcla la demo con el resultado de la prueba.
            gestor = main()  # Ejecuta las diez operaciones.
        self.assertIn("10 ejecutadas", salida.getvalue())  # Ningún error detuvo el recorrido.
        self.assertEqual(len(gestor.listar_reservas()), 5)  # Solo las procesadas quedan guardadas.
        self.assertTrue(all(reserva.estado == "PROCESADA" for reserva in gestor.listar_reservas()))  # Las cinco cerraron.


if __name__ == "__main__":  # Permite ejecutar solo este archivo.
    unittest.main()  # Inicia el ejecutor estándar.
