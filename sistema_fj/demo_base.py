"""Demostración del aporte inicial; todavía no es la simulación final de reservas."""

from .catalogo import Catalogo  # Almacena objetos exclusivamente en listas internas.
from .cliente import Cliente  # Permite mostrar registros válidos e inválidos.
from .excepciones import ErrorSoftwareFJ  # Captura la jerarquía de errores del dominio.
from .registro import RUTA_LOG, logger  # Indica dónde consultar los eventos de la ejecución.
from .servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Tres especialidades.


def ejecutar_operacion(numero, titulo, accion):
    """Aísla una operación para que su error no detenga las siguientes."""
    print(f"\n{numero:02d}. {titulo}")  # Muestra qué operación se está verificando.
    try:  # Protege únicamente la operación actual.
        resultado = accion()  # Ejecuta una función que representa el caso.
        if hasattr(resultado, "describir"):  # Los clientes y servicios tienen descripción propia.
            salida = resultado.describir()  # También protege los errores al generar la descripción.
        else:  # Los importes y otros resultados pueden mostrarse directamente.
            salida = resultado  # Conserva el resultado para imprimirlo después.
    except ErrorSoftwareFJ as error:  # La excepción propia ya quedó registrada al crearse.
        print(f"Error controlado: {error}")  # Explica el rechazo sin cerrar la aplicación.
        return False  # Informa que la operación no se completó.
    except Exception:  # Frontera de la aplicación: registra también errores imprevistos.
        logger.exception("Error inesperado en operación %s", numero)  # Incluye traza técnica.
        print("Error inesperado registrado; continúa la siguiente operación.")  # Continúa el recorrido.
        return False  # No informa éxito cuando hubo un fallo inesperado.
    else:  # Se ejecuta solo si no hubo excepción.
        print(f"Correcto: {salida}")  # Presenta el resultado de la operación exitosa.
        return True  # Informa éxito al contador de la demostración.
    finally:  # Se ejecuta tanto al devolver True como al devolver False.
        logger.info("Fin de operación %s: %s", numero, titulo)  # Deja evidencia del cierre.


def main():
    """Ejecuta casos de clientes y servicios; todos los datos son ficticios."""
    catalogo = Catalogo()  # Empieza una ejecución con listas vacías.

    def cotizar_servicios():
        """Llama al mismo método de costo en cada tipo de servicio."""
        costos = []  # Reúne los importes sin guardar datos en archivos.
        for servicio in catalogo.servicios:  # Recorre sala, equipos y asesoría.
            costo = servicio.calcular_costo(1)  # Cada servicio aplica su implementación.
            costos.append(costo)  # Añade el importe a la lista de resultados.
        return costos  # Permite mostrar juntos los tres costos.

    operaciones = [  # El orden permite reutilizar registros válidos en los casos siguientes.
        ("Registrar cliente válido", lambda: catalogo.registrar_cliente(
            Cliente("C001", "Cliente de prueba", "cliente@example.com", "3001234567"))),
        ("Rechazar correo inválido", lambda: Cliente("C002", "Prueba", "sin-arroba", "3001234567")),
        ("Rechazar parámetros faltantes", lambda: Cliente("C003")),
        ("Rechazar cliente duplicado", lambda: catalogo.registrar_cliente(
            Cliente("C001", "Otro cliente", "otro@example.com", "3001234568"))),
        ("Registrar sala válida", lambda: catalogo.registrar_servicio(
            ReservaSala("S001", "Sala de reuniones", "50000", 10))),
        ("Rechazar sala sin capacidad válida", lambda: ReservaSala("S002", "Sala", "50000", 0)),
        ("Registrar equipos válidos", lambda: catalogo.registrar_servicio(
            AlquilerEquipo("E001", "Portátil", "10000", 3))),
        ("Rechazar tarifa negativa", lambda: AlquilerEquipo("E002", "Equipo", "-1", 2)),
        ("Registrar asesoría válida", lambda: catalogo.registrar_servicio(
            AsesoriaEspecializada("A001", "Asesoría Python", "80000", "Programación"))),
        ("Rechazar especialidad vacía", lambda: AsesoriaEspecializada("A002", "Asesoría", "80000", "")),
        ("Cotizar sala durante dos horas", lambda: catalogo.buscar_servicio("S001").calcular_costo(2)),
        ("Cotizar equipos con tasas de ejemplo", lambda: catalogo.buscar_servicio("E001").calcular_costo(
            2, impuesto="0.19", descuento="0.10", unidades=2)),
        ("Rechazar exceso de personas", lambda: catalogo.buscar_servicio("S001").calcular_costo(1, personas=11)),
        ("Rechazar duración no numérica y encadenar causa", lambda: catalogo.buscar_servicio("S001").calcular_costo("dos")),
        ("Rechazar búsqueda inexistente", lambda: catalogo.buscar_cliente("C999")),
        ("Cotizar por polimorfismo después de errores", cotizar_servicios),  # Ejecuta el recorrido anterior.
    ]  # Termina la definición de escenarios del módulo base.
    print("SOFTWARE FJ - aporte inicial: clientes y servicios (reservas pendientes)")  # Aclara alcance.
    exitos = 0  # Cuenta operaciones que terminaron sin errores.
    for numero, (titulo, accion) in enumerate(operaciones, start=1):  # Ejecuta secuencialmente los casos.
        fue_correcta = ejecutar_operacion(numero, titulo, accion)  # Ejecuta la operación actual.
        if fue_correcta:  # Cuenta únicamente los casos que terminaron sin errores.
            exitos += 1  # Incrementa el contador de operaciones correctas.
    print(f"\nResumen: {exitos} correctas, {len(operaciones) - exitos} rechazadas, {len(operaciones)} ejecutadas.")
    print(f"Clientes en memoria: {len(catalogo.clientes)}; servicios: {len(catalogo.servicios)}.")  # Estado final.
    print(f"Log habitual: {RUTA_LOG}")  # Permite localizar el registro para revisión.
    return catalogo  # Facilita inspeccionar el estado final en pruebas.


if __name__ == "__main__":  # Evita ejecutar la demostración al importarla.
    main()  # Inicia la demostración cuando se usa python3 -m sistema_fj.demo_base.
