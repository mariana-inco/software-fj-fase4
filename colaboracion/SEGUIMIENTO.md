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
