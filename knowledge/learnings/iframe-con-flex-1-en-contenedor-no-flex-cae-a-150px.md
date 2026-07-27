---
title: un iframe con flex 1 en un contenedor que no es flex cae a 150px y parece contenido recortado
date: 2026-07-27
source: claude-code-session
tags: [css, frontend, modal, iframe]
---

`flex: 1` en un iframe NO le da altura si el padre no es un flex container: la propiedad
la ignora todo el mundo y el iframe se queda en su **alto intrínseco por defecto: 150px**
(300×150 del estándar). No hay error, no hay warning: se ve la franja superior del
documento y el resto del contenedor en blanco.

Caso real TuFacturaIA (#1261): la vista previa de PDF en `/generar` enseñó 150px de un A4
durante **dos meses**. El `.body` del `<Modal>` es un bloque con `overflow-y: auto`, no un
flex column, así que el `flex: 1` del iframe no lo aplicaba nadie.

Trampa añadida: `min-height` en el diálogo NO es altura definida, así que un hijo con
`height: 100%` tampoco resuelve. Hace falta que el ancestro tenga `height` fija (en el
Modal, el tier `xl`).

Reglas:
- Altura explícita SIEMPRE en iframes: `height` + un `min-height` de suelo. El patrón bueno
  del mismo repo era `.email-preview-iframe { min-height: 400px }`.
- Si un embed se ve "recortado" y el hueco de debajo está vacío, mide: 150px exactos =
  esto, no un problema de scroll ni de carga.
- Un visor incrustado no lo caza ningún test unitario. Ver [[camino-critico-sin-smoke-se-pudre-meses]].
