# Bitácora de avances

Aquí se registra trabajo efectivamente realizado. El calendario propuesto está
en [PENDIENTES.md](PENDIENTES.md); una fecha programada no prueba que se ejecutó
una actividad. Se usa la fecha real de Colombia y la cuenta de cada participante.

El historial de GitHub complementa esta bitácora. Cada entrada debe describir
el cambio o la comprobación realizada y enlazar su evidencia cuando exista.
Los mensajes de coordinación, capturas y datos personales se conservan de forma
privada; no se copian enlaces de invitación ni documentos de identidad aquí.

## 9 de noviembre de 2026 — preparación del aporte inicial

- Repositorio de trabajo: `mariana-inco/software-fj-fase4`.
- Trabajo realizado: preparación del módulo de clientes y servicios, catálogo,
  validaciones, excepciones, registros de eventos, demostración y pruebas.
- Ajustes realizados: organización de módulos y rutas; simplificación de algunos
  bucles y condicionales; control de errores al describir los resultados.
- Última ejecución de pruebas realizada durante la preparación:
  `python3 -m unittest discover -s pruebas -v` — 21 pruebas, resultado OK.
- Última ejecución de la demostración realizada durante la preparación:
  `python3 -m sistema_fj.demo_base` — 16 casos ejecutados, 7 correctos y 9
  rechazados intencionalmente. Quedaron un cliente y tres servicios en memoria.
- Publicación: se comprobó acceso público sin iniciar sesión; se verificó que los
  PDF del curso, evidencias privadas y registros locales no estén publicados.
- Soporte en GitHub:
  [módulo inicial](https://github.com/mariana-inco/software-fj-fase4/commit/9d38f23),
  [organización de rutas](https://github.com/mariana-inco/software-fj-fase4/commit/842c1e3),
  [simplificación y continuidad](https://github.com/mariana-inco/software-fj-fase4/commit/e175fed),
  [documentación pública](https://github.com/mariana-inco/software-fj-fase4/commit/f6ca8e4).
- Organización: se prepararon una lista de pendientes y esta bitácora para los
  próximos avances. Las fechas futuras son metas, sin actividades dadas por realizadas.
- Pendiente al cerrar: acordar la colaboración; desarrollar reservas; completar
  integración, simulación, pruebas de reservas y PDF grupal.

## 10 de noviembre de 2026 — revisión de Cliente

Fecha real: 10 de noviembre de 2026, 07:56, hora de Colombia.
Participante y cuenta de GitHub: Mariana Gomez, `mariana-inco`.
Actividad del calendario: revisión de `Cliente` prevista para el 11 de noviembre.
Se adelantó y queda registrada en la fecha real. El acuerdo de integración
previsto para el 10 de noviembre sigue pendiente: todavía no hay usuario de
GitHub de la compañera ni acceso de colaboración habilitado.

Qué se hizo o revisó: se leyeron los setters de nombre, correo y teléfono.
Se creó un cliente válido y se rechazó una actualización de correo y otra de
teléfono. El comentario del correo decía que solo se conservaban las mayúsculas
de la parte local; el ejemplo mostró que también se conserva el dominio. Se
corrigió ese comentario.

Archivos modificados o revisados: `sistema_fj/cliente.py` y las pruebas de
cliente en `pruebas/test_base.py`.

Comando o procedimiento de comprobación: ejemplo directo con datos ficticios y
`python3 -m unittest` de las tres pruebas de cliente.

Resultado observado:

- `" C10 "` se guardó como `C10`; `" Ana Pérez "` quedó `Ana Pérez`.
- `"Ana@Example.com"` se conservó con las mayúsculas del nombre y del dominio.
- `"0123456789"` siguió siendo texto, con el cero inicial.
- `describir()` mostró `Cliente C10: Ana Pérez`, sin correo ni teléfono.
- `correo = "sin-arroba"` lanzó `ValidacionError: Correo: formato inválido.`
  y el correo siguió siendo `Ana@Example.com`.
- Después, `nuevo@example.com` sí reemplazó el correo.
- `telefono = "12"` lanzó `ValidacionError` y el teléfono siguió siendo
  `0123456789`.
- Las tres pruebas de cliente terminaron OK.

Commit: [2b60e7a](https://github.com/mariana-inco/software-fj-fase4/commit/2b60e7a).

Pendientes y siguiente paso: acordar con la compañera su usuario, el acceso y
los estados de reserva. El 12 de noviembre corresponde comprobar una cotización
de cada servicio. La clase `Reserva` sigue a cargo de ella.

## 10 de noviembre de 2026 — cotización de los tres servicios

Fecha real: 10 de noviembre de 2026, hora de Colombia, después de las 10:30.
Participante y cuenta de GitHub: Mariana Gomez, `mariana-inco`.
Actividad del calendario: cotización de cada tipo de servicio, prevista para el
12 de noviembre. Se adelantó y queda registrada en la fecha real.

Qué se hizo o revisó: se crearon una sala, un alquiler de equipos y una asesoría.
Se llamó `calcular_costo` y `describir` sobre cada uno. Los tres son subclases de
`Servicio`, así que la misma llamada usa la implementación de cada tipo.

Archivos revisados: `sistema_fj/servicios.py` y las pruebas de polimorfismo y
variantes de costo en `pruebas/test_base.py`. No se modificó el cálculo.

Comando o procedimiento de comprobación: ejemplo directo con datos ficticios y
`python3 -m unittest` de `test_polimorfismo_y_costos` y
`test_variantes_impuesto_descuento_y_cantidad`.

Resultado observado:

- Sala, tarifa 50000 por hora: una hora cuesta `50000.00` y dos horas, `100000.00`.
  El número de personas no cambia el precio.
- Equipo, tarifa 10000 por unidad y hora: una unidad durante una hora cuesta
  `10000.00`. Dos unidades durante dos horas, con descuento `0.10` e impuesto
  `0.19`, cuestan `42840.00` (`10000 × 2 × 2 × 0.90 × 1.19`).
- Asesoría, tarifa 80000 por hora: una hora cuesta `80000.00` y hora y media,
  `120000.00`.
- Las dos pruebas terminaron OK.

Commit: [1875851](https://github.com/mariana-inco/software-fj-fase4/commit/1875851).

Pendientes y siguiente paso: la confirmación de reservas sigue a cargo de la
compañera. El 13 de noviembre corresponde revisar los límites de personas y de
unidades. La clase `Reserva` todavía no está implementada.

## 11 de noviembre de 2026 — límites de personas y unidades

Fecha real: 11 de noviembre de 2026, hora de Colombia.
Participante y cuenta de GitHub: Mariana Gomez, `mariana-inco`.
Actividad del calendario: revisión de límites de personas y unidades, prevista
para el 13 de noviembre. Se adelantó y queda registrada en la fecha real.

Qué se hizo o revisó: se creó una sala de capacidad 10 y un alquiler de 3
unidades. Se rechazó una solicitud de 11 personas y otra de 4 unidades. Después
de cada rechazo se volvió a leer la capacidad y el stock. También se aceptó el
máximo permitido y se comprobó que ni el rechazo ni la cotización cambian esos
datos. En este módulo la cotización no descuenta inventario.

Archivos modificados o revisados: `sistema_fj/servicios.py`,
`pruebas/test_base.py` y `README.md`. Se añadió
`test_rechazo_de_limites_conserva_datos` y el conteo de pruebas pasó de 21 a 22.
No se cambió la regla de capacidad ni la de unidades.

Comando o procedimiento de comprobación: ejemplo directo con datos ficticios y
`python3 -m unittest discover -s pruebas -v`.

Resultado observado:

- Sala `S10`, capacidad inicial `10`. `personas=11` lanzó
  `ValidacionError: Personas: se supera la capacidad de la sala.`
  La capacidad siguió en `10`.
- `personas=10` devolvió `{'personas': 10}` y la capacidad siguió en `10`.
- Equipo `E10`, unidades iniciales `3`. `unidades=4` lanzó
  `ValidacionError: Unidades: se supera la cantidad disponible.`
  Las unidades siguieron en `3`.
- Cotizar 3 unidades durante una hora costó `30000.00` y las unidades
  siguieron en `3`.
- Las 22 pruebas terminaron OK, incluida la nueva.

Commit: [c1ac85a](https://github.com/mariana-inco/software-fj-fase4/commit/c1ac85a).

Pendientes y siguiente paso: el 14 de noviembre corresponde seguir un error de
conversión, su causa encadenada y su registro. La clase `Reserva` sigue a cargo
de la compañera.

## 11 de noviembre de 2026 — error de conversión y su registro

Fecha real: 11 de noviembre de 2026, hora de Colombia, después de las 22:00.
Participante y cuenta de GitHub: Mariana Gomez, `mariana-inco`.
Actividad del calendario: seguir un error de conversión, su causa encadenada y
su registro, prevista para el 14 de noviembre. Se adelantó y queda registrada
en la fecha real.

Qué se hizo o revisó: se cotizó una sala con duración `"dos"`. `numero` intenta
convertir ese texto con `Decimal`. La conversión falla, se lanza `ValidacionError`
y la causa técnica queda encadenada con `raise ... from`. Al crearse, el error
propio se escribe en el log. La causa técnica no se copia al archivo: el log
guarda el tipo y el mensaje del dominio. Después del rechazo, la sala sigue
pudiendo cotizar.

Archivos modificados o revisados: `sistema_fj/validaciones.py`,
`sistema_fj/excepciones.py`, `sistema_fj/registro.py`, `pruebas/test_base.py`
y `README.md`. Se añadió `test_conversion_encadena_causa_y_queda_en_log`.
No se cambió la conversión ni el formato del log.

Comando o procedimiento de comprobación: ejemplo directo con datos ficticios y
`python3 -m unittest discover -s pruebas -v`.

Resultado observado:

- Sala `S20`, tarifa `50000` y capacidad `10`.
- `calcular_costo("dos")` lanzó `ValidacionError: Duración: no se pudo convertir a número.`
- La causa encadenada fue `InvalidOperation: [<class 'decimal.ConversionSyntax'>]`.
- El log añadió `2026-11-11 22:01:43,002 | ERROR | ValidacionError: Duración: no se pudo convertir a número.`
- La capacidad siguió en `10` y la tarifa en `50000`.
- Las 23 pruebas terminaron OK, incluida la nueva.

Commit: [c9362fb](https://github.com/mariana-inco/software-fj-fase4/commit/c9362fb).

Pendientes y siguiente paso: el 15 de noviembre corresponde integrar reservas
con clientes y servicios. Esa parte sigue a cargo de la compañera mientras
`Reserva` no esté implementada.

## Plantilla para una nueva entrada

Copiar el siguiente bloque únicamente después de realizar una actividad. No
rellenar resultados, participantes ni enlaces con datos que no se hayan comprobado.

```text
Fecha real:
Participante y cuenta de GitHub:
Actividad del calendario:
Qué se hizo o revisó:
Archivos modificados o revisados:
Comando o procedimiento de comprobación:
Resultado observado:
Commit, pull request o ubicación de la evidencia:
Pendientes y siguiente paso:
```

Si una actividad se hizo en una fecha distinta de la planeada, conservar la fecha
real y señalar el cambio. Si no se pudo avanzar, explicar el bloqueo y dejar la
casilla abierta. Revisar una clase o ejecutar una prueba no debe presentarse como
si ese día se hubiera creado todo el módulo.
