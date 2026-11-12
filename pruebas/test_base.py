"""Casos de negocio y errores que pueden afectar la integración de reservas."""

import io  # Captura salidas para verificar continuidad sin llenar la consola.
import logging  # Permite probar el respaldo del registrador.
import unittest  # Ejecuta pruebas sin instalar dependencias.
from contextlib import redirect_stdout, redirect_stderr  # Aísla salidas de demostraciones y errores.
from decimal import Decimal, InvalidOperation  # Compara importes y causas de conversión.
from unittest.mock import patch  # Simula la falta de permisos del archivo de registros.

from sistema_fj.catalogo import Catalogo  # Clase responsable de las listas internas.
from sistema_fj.cliente import Cliente  # Clase de datos personales encapsulados.
from sistema_fj.demo_base import ejecutar_operacion, main  # Frontera que debe sobrevivir errores.
from sistema_fj.entidad import Entidad  # Abstracción que no debe instanciarse.
from sistema_fj.excepciones import CalculoError, DuplicadoError, NoEncontradoError  # Errores esperados.
from sistema_fj.excepciones import ServicioNoDisponibleError, ValidacionError  # Reglas de validación.
from sistema_fj.registro import RUTA_LOG, obtener_logger  # Permite verificar registro y respaldo.
from sistema_fj.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio  # Modelos.


class PruebasBase(unittest.TestCase):
    """Comprueba comportamientos observables del módulo, sin escribir reservas."""

    def setUp(self):
        """Crea un catálogo y servicios nuevos antes de cada prueba."""
        self.catalogo = Catalogo()  # Evita contaminación entre pruebas.
        self.sala = ReservaSala("S1", "Sala", "50000", 10)  # Servicio con límite conocido.
        self.equipo = AlquilerEquipo("E1", "Portátil", "10000", 3)  # Tarifa por unidad.
        self.asesoria = AsesoriaEspecializada("A1", "Tutoría", "80000", "Python")  # Tercer tipo.

    def test_abstracciones_no_instanciables(self):
        """Entidad y Servicio deben conservar su contrato abstracto."""
        for tipo in (Entidad, Servicio):  # Revisa ambas abstracciones requeridas.
            with self.subTest(tipo=tipo), self.assertRaises(TypeError):  # Debe faltar implementación.
                tipo("ID")  # Intenta crear la abstracción incompleta.

    def test_cliente_valido_y_normalizacion(self):
        """La captura quita espacios externos y preserva ceros del teléfono."""
        cliente = Cliente(" C1 ", " Ana Pérez ", "ana@example.com", "0123456789")  # Datos ficticios.
        self.assertEqual(cliente.identificador, "C1")  # Identificador normalizado.
        self.assertEqual(cliente.nombre, "Ana Pérez")  # Nombre normalizado.
        self.assertEqual(cliente.telefono, "0123456789")  # No convierte teléfono a entero.

    def test_campos_faltantes_y_contactos_invalidos(self):
        """Cada campo inválido se rechaza sin crear un cliente válido."""
        cambios = [dict(identificador=None), dict(nombre=" "), dict(correo="sin-arroba"),
                   dict(correo="a@b..com"), dict(telefono="123"), dict(telefono=True),
                   dict(nombre="Ana\nPérez")]  # Incluye caracteres que podrían contaminar el log.
        for cambio in cambios:  # Revisa cada campo de forma independiente.
            datos = dict(identificador="C1", nombre="Ana", correo="a@example.com", telefono="3001234567")
            datos.update(cambio)  # Sustituye únicamente el campo que se desea invalidar.
            with self.subTest(cambio=cambio), self.assertRaises(ValidacionError):  # Error controlado.
                Cliente(**datos)  # Ejecuta la construcción con la entrada inválida.

    def test_actualizacion_invalida_conserva_dato(self):
        """Un setter fallido no debe corromper el valor anterior."""
        cliente = Cliente("C1", "Ana", "a@example.com", "3001234567")  # Cliente inicial válido.
        with self.assertRaises(ValidacionError):  # Debe impedir el cambio de correo.
            cliente.correo = "invalido"  # Simula una actualización incorrecta.
        self.assertEqual(cliente.correo, "a@example.com")  # Comprueba que el dato anterior permanece.
        cliente.correo = "nuevo@example.com"  # Simula una actualización correcta.
        self.assertEqual(cliente.correo, "nuevo@example.com")  # Comprueba el nuevo valor.

    def test_identificador_solo_lectura(self):
        """Cambiar una clave registrada rompería las búsquedas y duplicados."""
        with self.assertRaises(AttributeError):  # La propiedad no tiene setter.
            self.sala.identificador = "otro"  # Intenta cambiar la clave por la interfaz pública.

    def test_duplicados_y_busqueda(self):
        """Un duplicado no debe aumentar el tamaño del catálogo."""
        cliente = Cliente("C1", "Ana", "a@example.com", "3001234567")  # Crea registro válido.
        self.catalogo.registrar_cliente(cliente)  # Registra una vez.
        with self.assertRaises(DuplicadoError):  # La segunda alta debe fallar.
            self.catalogo.registrar_cliente(cliente)  # Repite la misma clave.
        self.assertEqual(len(self.catalogo.clientes), 1)  # La lista conserva un solo objeto.
        self.assertIs(self.catalogo.buscar_cliente(" C1 "), cliente)  # Recupera la instancia original.
        with self.assertRaises(NoEncontradoError):  # Debe distinguir la ausencia del registro.
            self.catalogo.buscar_servicio("inexistente")  # Busca en una lista vacía.

    def test_tipo_y_estructura_de_listas(self):
        """Los llamadores no pueden agregar objetos arbitrarios a la vista pública."""
        with self.assertRaises(ValidacionError):  # Un servicio no es un cliente.
            self.catalogo.registrar_cliente(self.sala)  # Rechaza el tipo equivocado.
        self.catalogo.registrar_servicio(self.sala)  # Acepta un servicio concreto.
        self.assertIsInstance(self.catalogo.servicios, tuple)  # Expone una estructura inmutable.
        with self.assertRaises(DuplicadoError):  # Protege también las claves de servicios.
            self.catalogo.registrar_servicio(ReservaSala("S1", "Otra", 1, 1))  # Misma clave.

    def test_alta_rechazada_conserva_listas(self):
        """Un duplicado, un tipo incorrecto o una búsqueda vacía no cambian el catálogo."""
        cliente = Cliente("C12", "Ana Perez", "ana@example.com", "3001234567")  # Cliente ficticio.
        self.catalogo.registrar_cliente(cliente)  # Primera alta válida.
        with self.assertRaises(DuplicadoError):  # La misma clave no puede repetirse.
            self.catalogo.registrar_cliente(Cliente("C12", "Otra", "otra@example.com", "3001234568"))
        with self.assertRaises(ValidacionError):  # Una sala no es un cliente.
            self.catalogo.registrar_cliente(self.sala)  # No debe entrar a ninguna lista.
        with self.assertRaises(ValidacionError):  # Un identificador vacío no es una búsqueda.
            self.catalogo.buscar_cliente("  ")  # Se rechaza antes de recorrer la lista.
        with self.assertRaises(NoEncontradoError):  # El servicio no fue registrado.
            self.catalogo.buscar_servicio("S12")  # La ausencia no crea un servicio.
        self.assertEqual(self.catalogo.clientes, (cliente,))  # Sigue el único cliente válido.
        self.assertEqual(self.catalogo.servicios, ())  # La lista de servicios sigue vacía.

    def test_polimorfismo_y_costos(self):
        """La misma llamada utiliza los tres métodos sobrescritos."""
        servicios = (self.sala, self.equipo, self.asesoria)  # Lista heterogénea de servicios.
        self.assertEqual([item.calcular_costo(2) for item in servicios],
                         [Decimal("100000.00"), Decimal("20000.00"), Decimal("160000.00")])
        self.assertTrue(all(isinstance(item, Servicio) for item in servicios))  # Herencia común.
        self.assertEqual(len({item.describir() for item in servicios}), 3)  # Descripciones específicas.

    def test_variantes_impuesto_descuento_y_cantidad(self):
        """Verifica orden de ajustes, variantes opcionales y tarifa por unidad."""
        self.assertEqual(self.equipo.calcular_costo(2, "0.19", "0.10", unidades=2), Decimal("42840.00"))
        self.assertEqual(self.sala.calcular_costo(2, impuesto="0.19"), Decimal("119000.00"))
        self.assertEqual(self.sala.calcular_costo(2, descuento="0.10"), Decimal("90000.00"))
        self.assertEqual(self.sala.calcular_costo(2, descuento=1), Decimal("0.00"))  # Admite descuento total.

    def test_redondeo_y_horas_fraccionarias(self):
        """Se redondea al final, con una regla explícita de centavos."""
        servicio = ReservaSala("S2", "Sala", "0.05", 1)  # Tarifa útil para probar medio centavo.
        self.assertEqual(servicio.calcular_costo("0.5"), Decimal("0.03"))  # ROUND_HALF_UP.

    def test_duraciones_invalidas(self):
        """NaN, infinitos, booleanos y valores no positivos nunca son duraciones."""
        for valor in (None, True, 0, -1, "dos", "NaN", "Infinity", float("nan"), []):
            with self.subTest(valor=valor), self.assertRaises(ValidacionError):  # Cada dato se rechaza.
                self.sala.calcular_costo(valor)  # Intenta cotizar con duración inválida.

    def test_tasas_invalidas(self):
        """Impuestos y descuentos deben estar en el intervalo de cero a uno."""
        for campo in ("impuesto", "descuento"):  # Revisa ambas tasas por separado.
            for valor in (-0.1, "1.01", True, "NaN", None):  # Límites y tipos incorrectos.
                with self.subTest(campo=campo, valor=valor), self.assertRaises(ValidacionError):
                    self.sala.calcular_costo(1, **{campo: valor})  # Inyecta la tasa inválida.

    def test_parametros_de_cada_servicio(self):
        """No permite sobrepasar capacidad, stock o usar temas vacíos."""
        casos = [(self.sala, {"personas": 11}), (self.sala, {"personas": 1.5}),
                 (self.equipo, {"unidades": 4}), (self.equipo, {"unidades": 0}),
                 (self.asesoria, {"tema": " "}), (self.sala, {"persona": 1})]  # Incluye errata.
        for servicio, parametros in casos:  # Revisa las especialidades con la misma interfaz.
            with self.subTest(parametros=parametros), self.assertRaises(ValidacionError):
                servicio.calcular_costo(1, **parametros)  # Valida también antes de cotizar.
        self.assertEqual(self.sala.validar_parametros(personas=10), {"personas": 10})  # Límite válido.
        self.assertEqual(self.equipo.calcular_costo(1, unidades=3), Decimal("30000.00"))  # Límite válido.
        self.assertEqual(self.asesoria.validar_parametros(tema="POO"), {"tema": "POO"})  # Tema válido.

    def test_rechazo_de_limites_conserva_datos(self):
        """Un exceso de personas o de unidades no cambia la capacidad ni el stock."""
        self.assertEqual(self.sala.capacidad, 10)  # La sala de prueba admite diez personas.
        with self.assertRaises(ValidacionError):  # Once personas superan ese máximo.
            self.sala.validar_parametros(personas=11)  # El rechazo ocurre antes de cotizar.
        self.assertEqual(self.sala.capacidad, 10)  # La capacidad sigue siendo diez.
        self.assertEqual(self.sala.validar_parametros(personas=10), {"personas": 10})  # El máximo sí es válido.
        self.assertEqual(self.sala.capacidad, 10)  # Aceptar el límite tampoco la reduce.

        self.assertEqual(self.equipo.unidades_disponibles, 3)  # Hay tres unidades al empezar.
        with self.assertRaises(ValidacionError):  # Cuatro unidades superan el stock.
            self.equipo.calcular_costo(1, unidades=4)  # No llega a calcular el costo.
        self.assertEqual(self.equipo.unidades_disponibles, 3)  # El inventario no cambió.
        self.assertEqual(self.equipo.calcular_costo(1, unidades=3), Decimal("30000.00"))  # El máximo sí se cobra.
        self.assertEqual(self.equipo.unidades_disponibles, 3)  # Cobrar no descuenta unidades.

    def test_servicios_invalidos_y_parametros_faltantes(self):
        """Rechaza capacidades fraccionarias, tarifas nulas y especialidades faltantes."""
        constructores = [lambda: ReservaSala("S", "Sala", 1, 1.5),
                         lambda: AlquilerEquipo("E", "Equipo", 0, 1),
                         lambda: AsesoriaEspecializada("A", "Asesoría", 1), lambda: Cliente()]
        for constructor in constructores:  # Recorre distintas rutas de validación.
            with self.subTest(constructor=constructor), self.assertRaises(ValidacionError):
                constructor()  # Intenta construir un objeto con parámetros inválidos o faltantes.

    def test_disponibilidad_y_reactivacion(self):
        """Un servicio deshabilitado no cotiza; reactivarlo recupera su operación."""
        self.sala.disponible = False  # Simula mantenimiento.
        with self.assertRaises(ServicioNoDisponibleError):  # Debe bloquear la operación.
            self.sala.calcular_costo(1)  # Intenta operar durante mantenimiento.
        with self.assertRaises(ValidacionError):  # No admite cadenas como estado.
            self.sala.disponible = "sí"  # Evita conversión booleana implícita.
        self.sala.disponible = True  # Habilita nuevamente el servicio.
        self.assertEqual(self.sala.calcular_costo(1), Decimal("50000.00"))  # Opera normalmente.

    def test_encadenamiento_y_fallo_aritmetico(self):
        """La excepción propia conserva la causa técnica para la depuración."""
        with self.assertRaises(ValidacionError) as captura:  # Captura la excepción externa.
            self.sala.calcular_costo("dos")  # Provoca fallo de conversión.
        self.assertIsNotNone(captura.exception.__cause__)  # Comprueba el uso real de raise ... from.
        with self.assertRaises(CalculoError) as calculo:  # Rechaza costos imposibles de representar.
            self.sala.calcular_costo("1e999999")  # Fuerza exceso del contexto decimal.
        self.assertIsInstance(calculo.exception.__cause__, ArithmeticError)  # Conserva causa aritmética.

    def test_conversion_encadena_causa_y_queda_en_log(self):
        """La palabra 'dos' no es una duración: el error guarda la causa y se registra."""
        with self.assertRaises(ValidacionError) as captura:  # La cotización debe rechazarse.
            self.sala.calcular_costo("dos")  # Decimal no puede convertir esa palabra.
        error = captura.exception  # Este es el error que ve quien llama.
        self.assertEqual(str(error), "Duración: no se pudo convertir a número.")  # Mensaje del dominio.
        self.assertIsInstance(error.__cause__, InvalidOperation)  # La causa técnica queda encadenada.
        registro = RUTA_LOG.read_text(encoding="utf-8")  # El error se escribe al crearse.
        self.assertIn("ValidacionError: Duración: no se pudo convertir a número.", registro)
        self.assertEqual(self.sala.capacidad, 10)  # El rechazo no cambia la sala.
        self.assertEqual(self.sala.calcular_costo(1), Decimal("50000.00"))  # Después sí se puede cotizar.

    def test_errores_quedan_en_log(self):
        """El registro de archivo debe incluir los errores propios detectados."""
        with self.assertRaises(ValidacionError):  # Genera un error identificable por su mensaje.
            self.sala.calcular_costo(-1)  # Duración inválida.
        self.assertIn("Duración: debe ser mayor que 0", RUTA_LOG.read_text(encoding="utf-8"))

    def test_respaldo_si_log_no_tiene_permisos(self):
        """La aplicación conserva un manejador cuando no puede crear la carpeta."""
        alterno = logging.Logger("prueba_sin_archivo")  # Registrador aislado del proyecto.
        with patch("sistema_fj.registro.logging.getLogger", return_value=alterno), \
                patch("sistema_fj.registro.Path.mkdir", side_effect=PermissionError("sin permiso")), \
                redirect_stderr(io.StringIO()):  # Simula ausencia de permisos sin tocar archivos reales.
            self.assertIs(obtener_logger(), alterno)  # Obtiene un registrador operativo.
            self.assertEqual(len(alterno.handlers), 1)  # Conserva un manejador de respaldo.
            self.assertIsInstance(alterno.handlers[0], logging.StreamHandler)  # Usa la consola.

    def test_continuidad_ante_error_inesperado(self):
        """La frontera registra una excepción imprevista y permite otra operación."""
        with redirect_stdout(io.StringIO()):  # Evita salida de la prueba en consola.
            self.assertFalse(ejecutar_operacion(1, "Fallo simulado", lambda: 1 / 0))  # Error inesperado.
            self.assertTrue(ejecutar_operacion(2, "Operación posterior", lambda: "continúa"))  # Continúa.

    def test_demo_completa_sin_reservas(self):
        """Los rechazos de la demostración no impiden alcanzar su última operación."""
        salida = io.StringIO()  # Captura todo el recorrido de la demostración.
        with redirect_stdout(salida):  # Redirige la salida solo durante la ejecución.
            catalogo = main()  # Ejecuta la secuencia completa.
        self.assertIn("16 ejecutadas", salida.getvalue())  # Ningún error interrumpió el recorrido.
        self.assertEqual(len(catalogo.clientes), 1)  # Solo un cliente fue aceptado.
        self.assertEqual(len(catalogo.servicios), 3)  # Los tres servicios válidos permanecen.

    def test_continuidad_si_falla_descripcion(self):
        """Un error al describir el resultado tampoco debe detener el recorrido."""
        with patch.object(self.sala, "describir", side_effect=ValueError("descripción inválida")), \
                redirect_stdout(io.StringIO()):  # Simula un fallo al presentar el resultado.
            self.assertFalse(ejecutar_operacion(1, "Descripción fallida", lambda: self.sala))
            self.assertTrue(ejecutar_operacion(2, "Operación posterior", lambda: "continúa"))


if __name__ == "__main__":  # Permite ejecutar este módulo de pruebas de forma directa.
    unittest.main()  # Inicia el ejecutor estándar.
