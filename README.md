# Software FJ — Fase 4 de Programación (213023)

Proyecto académico de gestión de clientes, servicios y reservas, sin base de datos.
El aporte de clientes y servicios está en `sistema_fj`. La clase `Reserva`,
el gestor y una simulación de 10 operaciones quedaron organizados en ese mismo
paquete a partir de los archivos que subió Marianita82J-m.

## Ejecutar

Desde la carpeta raíz de este repositorio, con Python 3:

```bash
python3 -m sistema_fj.demo_base
python3 -m sistema_fj.demo_integrada
python3 -m unittest discover -s pruebas -v
```

En Windows puede utilizarse `py` en lugar de `python3`. Solo se usa la biblioteca
estándar; no hay paquetes que instalar. Validado localmente con Python 3.14.7.

`demo_base` recorre 16 casos de clientes y servicios: 7 aceptados y 9 rechazados.
`demo_integrada` recorre 10 operaciones de reserva: 5 procesadas y 5 rechazadas.
Los rechazos son intencionales y el recorrido sigue después de cada error.

El registro se crea en `registros/sistema_fj.log`. Si no se puede abrir el archivo,
se informa la causa y se registra en consola. Los datos de clientes y servicios
solo existen en objetos y listas durante la ejecución. No se usa JSON, CSV,
pickle ni archivos para guardar información del negocio.

## Reparto propuesto entre las dos participantes

La distribución es una propuesta para coordinar a quienes están participando;
no equivale a una autorización del tutor para modificar el grupo de cinco
estudiantes que indica el anexo.

- Mariana: `Entidad`, `Cliente`, `Servicio`, sus tres especialidades,
  catálogo de clientes y servicios, validaciones, excepciones, registros y pruebas de
  estos componentes. Revisar, entender y ajustar el aporte antes de sustentarlo.
- Compañera, cuenta `Marianita82J-m`: `Reserva`, estados y transiciones, gestor
  de reservas en una lista interna y la simulación de 10 operaciones. Esos
  archivos se subieron en la carpeta `Programacion Fase 4` y luego se organizaron
  dentro de `sistema_fj`. Puede añadir un menú de consola como apoyo; la guía no
  lo exige expresamente.
- Ambas: revisión final, comprobación de aportes reales en GitHub y PDF grupal.

Cada participante debe trabajar con su propia cuenta y realizar commits de su
trabajo real. No se deben atribuir aportes a personas que no los han realizado.

## Organización del código

- `sistema_fj/entidad.py`: clase abstracta general con identificador de solo lectura.
- `sistema_fj/cliente.py`: campos privados, propiedades y validaciones de contacto.
- `sistema_fj/servicios.py`: `Servicio` abstracto, `ReservaSala`,
  `AlquilerEquipo` y `AsesoriaEspecializada`.
- `sistema_fj/catalogo.py`: altas y búsquedas en listas privadas de objetos.
- `sistema_fj/validaciones.py`: texto, enteros y números finitos.
- `sistema_fj/excepciones.py`: errores personalizados, incluidos los que puede usar Reserva.
- `sistema_fj/registro.py`: archivo común de eventos y errores.
- `sistema_fj/demo_base.py`: recorrido secuencial de clientes y servicios.
- `sistema_fj/reserva.py`: estados de la reserva y transiciones permitidas.
- `sistema_fj/gestor_reservas.py`: lista interna de reservas, sin identificadores repetidos.
- `sistema_fj/demo_integrada.py`: 10 operaciones de reserva, con aciertos y rechazos.
- `pruebas/test_base.py`: 27 pruebas de clientes y servicios.
- `pruebas/test_reservas.py`: pruebas de estados, duplicados y de la demo integrada.
- `colaboracion/INTEGRACION.md`: interfaz que utilizará la compañera.
- [Pendientes](colaboracion/PENDIENTES.md): actividades propuestas hasta la entrega.
- [Bitácora](colaboracion/SEGUIMIENTO.md): avances realizados y evidencias verificables.

`ReservaSala` es el **tipo de servicio** que alquila una sala. La clase
`Reserva` es la operación que relaciona cliente, servicio, duración y estado.

## Decisiones de diseño que no fija el enunciado

Las tarifas de la demostración son ficticias y se expresan por hora. Los equipos
se cobran por unidad y hora. Una sala no cambia de precio por número de asistentes.
Las duraciones pueden ser fraccionarias y deben ser positivas. Se utiliza
`Decimal` para importes y se redondea al final a dos decimales, con `ROUND_HALF_UP`.

El importe se calcula así:

```text
tarifa_por_hora × horas × cantidad × (1 − descuento) × (1 + impuesto)
```

`cantidad` vale uno salvo en equipos. Las tasas se expresan entre cero y uno.
El impuesto y descuento predeterminados son cero; el 0.19 de la demostración
es un parámetro de ejemplo, no una regla tributaria del ejercicio.

Las variantes de `calcular_costo` se implementan mediante argumentos opcionales:
costo simple, con impuesto, con descuento o con ambos. Es la alternativa
permitida por el ejemplo del anexo. No se simula una sobrecarga de firmas
redefiniendo varias veces el mismo método: Python conservaría la última definición.

El correo usa una validación básica de formato; no se consulta la existencia del
buzón. El teléfono admite de 7 a 15 dígitos ASCII y `+` inicial opcional. Los
identificadores son internos y no corresponden a documentos reales.

La disponibilidad actual es general (`True`/`False`). El calendario, el inventario
ocupado y las restricciones entre reservas no están implementados. Al integrar,
debe definirse y documentarse una política consistente para evitar sobreasignación.

## Dónde se evidencia el manejo de excepciones

- `validaciones.numero`: `try/except` y encadenamiento con `raise ... from causa`.
- `Servicio._calcular_total`: `try/except/else` y error propio de cálculo.
- `demo_base.ejecutar_operacion`: `try/except/else/finally`, errores de dominio
  y una captura general en la frontera para registrar fallos imprevistos.
- `registro.obtener_logger`: recuperación si no puede crearse el archivo.

Los errores propios se registran al construirse. La frontera registra la traza
de los errores inesperados. Los eventos de creación, registro, costo,
disponibilidad y finalización de operaciones también quedan en el log.

El código contiene comentarios y docstrings para facilitar la revisión línea por
línea que pide la guía. Cada integrante debe verificar las explicaciones de sus
propios cambios y poder explicar el funcionamiento de forma autónoma.

## Pendientes para la entrega grupal

La distribución por días está en [PENDIENTES.md](colaboracion/PENDIENTES.md).
Registrar cada actividad realizada en la [bitácora](colaboracion/SEGUIMIENTO.md)
y cerrar las casillas únicamente cuando se haya comprobado el resultado.

- Completar en `Reserva` la validación de disponibilidad y parámetros al confirmar,
  el costo de la reserva y la política de ocupación. La confirmación, la cancelación
  y el procesamiento básicos ya están organizados.
- La demo integrada ya recorre 10 operaciones de reserva. Falta ampliarla con
  clientes y servicios inválidos dentro de ese mismo recorrido, si el grupo lo acuerda.
- Mantener los datos del negocio en listas y usar archivos únicamente para eventos y errores.
- Compartir en el foro el enlace de GitHub y comprobar que el tutor tenga acceso.
- Elaborar un único PDF con portada, introducción, enlace al repositorio,
  conclusiones y referencias en normas APA, según la guía.
- Comprobar novedades del curso y cualquier precisión adicional del tutor.

El repositorio es público para facilitar la revisión del tutor. La compañera
necesita una invitación como colaboradora para subir cambios directamente;
también puede contribuir desde una copia propia mediante un pull request.

La guía disponible indica cierre el **22 de noviembre de 2026** y valor de 150
puntos. No se encontró una rúbrica específica de Fase 4 entre los archivos
locales; la rúbrica de Fase 2 no se ha utilizado como si fuera la de esta actividad.

## Material local y fuentes

`material_curso/` contiene copias locales del anexo y la guía para su consulta
local. Esos PDF no se suben a GitHub. `evidencias_privadas/`, cuando exista,
tampoco se publica: la captura del foro contiene un enlace de invitación a WhatsApp.

Documentación oficial consultada para contrastar la implementación:

- Python Software Foundation. (s. f.). *Errores y excepciones*. Documentación de
  Python 3.12. https://docs.python.org/es/3.12/tutorial/errors.html
- Python Software Foundation. (s. f.). *Más herramientas para control de flujo:
  valores por omisión para los argumentos*. Documentación de Python 3.12.
  https://docs.python.org/es/3.12/tutorial/controlflow.html#default-argument-values
- Python Software Foundation. (s. f.). *abc — Clases de base abstracta*.
  Documentación de Python 3.12. https://docs.python.org/es/3.12/library/abc.html

Las referencias de los documentos del curso deben completarse en el PDF a
partir de sus datos reales. No inventar autores, fechas, páginas ni fuentes.
