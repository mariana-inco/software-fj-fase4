# Integración de reservas

Esta interfaz corresponde al aporte inicial. La compañera puede añadir módulos
nuevos sin sustituir clientes, servicios ni sus pruebas.

## Preparar el entorno de la compañera

Mariana debe dar acceso desde Settings → Collaborators del repositorio privado.
El usuario de GitHub de la compañera está pendiente de informar; todavía no se
ha enviado ninguna invitación.

```bash
git clone https://github.com/mariana-inco/software-fj-fase4.git
cd software-fj-fase4
git switch -c aporte/reservas
python3 -m unittest discover -s tests -v
```

## API disponible

```python
from software_fj.catalogo import Catalogo
from software_fj.cliente import Cliente
from software_fj.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

catalogo = Catalogo()
cliente = catalogo.registrar_cliente(
    Cliente("C001", "Cliente ficticio", "cliente@example.com", "3001234567")
)
sala = catalogo.registrar_servicio(ReservaSala("S001", "Sala A", "50000", 10))
equipo = catalogo.registrar_servicio(AlquilerEquipo("E001", "Portátil", "10000", 3))
asesoria = catalogo.registrar_servicio(
    AsesoriaEspecializada("A001", "Asesoría", "80000", "Programación")
)

cliente = catalogo.buscar_cliente("C001")
sala = catalogo.buscar_servicio("S001")
parametros = sala.validar_parametros(personas=4)
costo = sala.calcular_costo(2, impuesto="0.19", descuento="0.10", **parametros)
# costo es Decimal('107100.00'): 50000 × 2 × 0.90 × 1.19.
```

Firmas públicas comunes:

```text
Cliente(identificador, nombre, correo, telefono)
ReservaSala(identificador, nombre, tarifa_hora, capacidad)
AlquilerEquipo(identificador, nombre, tarifa_hora, unidades_disponibles)
AsesoriaEspecializada(identificador, nombre, tarifa_hora, especialidad)

servicio.validar_parametros(**parametros) -> dict
servicio.calcular_costo(duracion, impuesto=0, descuento=0, **parametros) -> Decimal
servicio.describir() -> str
servicio.disponible -> bool; admite asignar solo True o False
```

Parámetros específicos: `personas` para salas (por defecto 1), `unidades` para
equipos (por defecto 1) y `tema` para asesorías (por defecto su especialidad).
Se rechazan argumentos desconocidos. El catálogo expone tuplas mediante
`catalogo.clientes` y `catalogo.servicios`; sus listas privadas no deben manipularse.

## Contrato propuesto de la siguiente parte

Añadir `software_fj/reserva.py` y, si resulta necesario,
`software_fj/gestor_reservas.py`, `software_fj/demo_integrada.py` y
`tests/test_reservas.py`. No se han creado archivos vacíos que aparenten cumplirlos.

Propuesta de diseño, ajustable por acuerdo entre ambas:

```text
Reserva(identificador, cliente, servicio, duracion, impuesto=0, descuento=0, **parametros)
reserva.confirmar()
reserva.cancelar()
reserva.procesar()
reserva.estado
reserva.costo
```

Validar tipos de cliente y servicio, duración, parámetros específicos y estados.
Propuesta de transiciones: PENDIENTE → CONFIRMADA → PROCESADA y
PENDIENTE/CONFIRMADA → CANCELADA. Rechazar confirmación repetida, procesamiento
sin confirmación, cancelación repetida y cambios desde estados finales. Una
operación fallida debe conservar el estado anterior. El enunciado no fija estos
nombres ni su orden: documentar el diseño que finalmente acuerden.

Las reservas se conservan en una lista interna, con identificadores únicos.
Como el anexo no define fechas ni horarios, se puede acordar un modelo sencillo
de ocupación simultánea: las confirmadas retienen recursos hasta procesarse o
cancelarse. En ese modelo, salas y asesores aceptan una reserva activa; equipos
no pueden superar su stock acumulado. También puede elegirse un calendario,
pero la política debe ser explícita, probada y coherente en todas las transiciones.

Reutilizar `ReservaError`, `ValidacionError` y
`ServicioNoDisponibleError`; todas derivan de `ErrorSoftwareFJ` y se registran
al crearse. Para eventos adicionales usar `from .registro import logger`.
No repetir el mismo error en varios logs. Conservar la frontera de recuperación
para que una operación fallida no termine la simulación.

## Antes de integrar

1. Añadir casos de reserva exitosa, falta de cliente/servicio, duración inválida,
   servicio no disponible, capacidad/stock insuficiente y transición no permitida.
2. Probar que un error no altera el estado previo ni consume recursos parcialmente.
3. Ejecutar todas las pruebas: `python3 -m unittest discover -s tests -v`.
4. Ejecutar la demo integrada y verificar al menos 10 operaciones completas,
   incluidas reservas válidas e inválidas y una operación exitosa posterior a los errores.
5. Hacer commit con la cuenta propia, subir la rama y abrir un pull request.
6. Revisar entre ambas y actualizar README con el comando de ejecución final.

El PDF grupal se elabora cuando la integración esté terminada. Debe reflejar lo
que realmente funciona y las personas que participaron.
