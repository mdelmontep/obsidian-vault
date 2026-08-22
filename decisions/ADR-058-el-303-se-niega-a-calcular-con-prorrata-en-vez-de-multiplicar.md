---
title: ADR-058 — con prorrata, el 303 se niega a calcular en vez de multiplicar por el porcentaje
date: 2026-08-23
status: accepted
tags: [adr, facturaia, fiscal]
---

## Contexto
`perfil_fiscal.prorrata_deduccion_pct` (mig 426) se pedía en el asistente y se aplicaba en el libro
registro, pero el motor del 303 no lo leía: deducía el IVA íntegro. Dos papeles nuestros, dos cifras
—una org al 40 % veía 10.000 € en el impreso y 4.000 € en su propio libro—. Ninguna org de prod está
hoy por debajo del 100 %, así que no hay declaración presentada dañada.

## Opciones consideradas
- **A · Multiplicar** la cuota deducible por el porcentaje — dos líneas, y el 303 parece correcto.
- **B · Bloquear** el cálculo de 303 y 390, exportar libros y remitir al asesor.
- **C · Calcular y avisar** con un cuadre crítico, dejando presentar bajo responsabilidad del usuario.

## Decisión
**B**, porque la prorrata no es una multiplicación: el porcentaje del año es provisional (art. 105) y
exige regularizar con el definitivo (c43) y los bienes de inversión 5-10 años (c42, art. 107-110); con
prorrata especial (art. 103) la deducción va por sectores, dato que el perfil ni recoge. **A** daría un
impreso igual de incorrecto pero mucho más creíble, que es peor: nadie lo revisaría. **C** traslada al
usuario una decisión que no puede tomar con lo que la pantalla le enseña. Mismo criterio que el 131.

## Consecuencias
Nos compromete a que el motor **declare lo que no sabe hacer** en vez de aproximarlo, y a que libro y
303 no puedan divergir (trinquete `prorrata-libro-vs-303`). Una org en prorrata no verá tampoco el
aviso de recibidas sin aprobar en el 303, porque la guarda corta antes; asumido, no tiene declaración.
El campo queda **fuera del hash del perfil** a propósito: incluirlo habría movido la huella de todas
las declaraciones ya selladas y el canario habría acusado de manipulación a cada cliente.
Abre la puerta a implementar prorrata de verdad (c42/c43/especial) como trabajo propio, no como parche.
