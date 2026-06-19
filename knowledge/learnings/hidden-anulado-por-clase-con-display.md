---
title: el atributo html `hidden` lo anula cualquier clase con `display:`
date: 2026-06-19
source: claude-code-session
tags: [css, a11y, cascade]
---
`hidden={!open}` en el TSX no oculta nada si una clase del mismo elemento declara
`display` (flex/grid/block). La regla de la hoja UA `[hidden]{display:none}` tiene
especificidad de atributo (0,1,0)... pero `.clase{display:flex}` también (0,1,0) y,
a igual especificidad, gana la del autor por orden de fuente. Resultado: el `display`
de la clase manda y `hidden` queda muerto.

Síntoma: acordeón / disclosure / panel SIEMPRE visible, no se puede cerrar.

Fix: subir especificidad combinando clase+atributo → `.clase[hidden]{display:none}` (0,2,0).

Caso real: FacturaIA #387 (lista glass integraciones) el panel de detalle salía siempre
abierto; fix #389 con `.int-row-detail[hidden]{display:none}`. Aplica a cualquier
patrón `hidden` + clase con `display` en otros proyectos.
