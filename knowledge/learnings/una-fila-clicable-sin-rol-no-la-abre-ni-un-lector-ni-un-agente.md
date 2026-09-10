---
title: una fila clicable sin rol no la abre ni un lector de pantalla ni un agente
date: 2026-09-10
source: facturaia
tags: [accesibilidad, frontend, agentes, qa]
---
Un `<tr>` con `onClick` y sin `role`/`tabIndex` **no existe en el árbol de accesibilidad**:
`read_page --filter interactive` de una tabla de 166 filas devolvió dos botones y ninguna
fila, y el clic sintético sobre sus coordenadas hizo scroll sin abrir nada. Medido en
`/admin/feedback` el 10-sep.

Importa por dos motivos que suelen mirarse por separado y son el mismo:

- **Accesibilidad real**: quien navega con teclado o lector no puede abrir esa fila. No es
  una molestia de automatización, es una función inalcanzable.
- **Automatizable = testeable**: lo que un agente no puede pulsar tampoco lo pulsa un E2E
  por rol, así que la vista se queda sin cobertura sin que nadie lo declare.

El arreglo es el mismo para los dos: `role="button"` + `tabIndex={0}` + `onKeyDown` en la
fila, o un control real dentro de ella. Y el tell para buscarlo: una tabla cuyo `filter:
interactive` no devuelve una entrada por fila. Ver [[el-arnes-se-mide-a-si-mismo]].
