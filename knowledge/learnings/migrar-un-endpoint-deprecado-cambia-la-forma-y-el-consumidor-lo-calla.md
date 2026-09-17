---
title: migrar un endpoint deprecado cambia la FORMA de la respuesta, y el consumidor defensivo lo convierte en verde
date: 2026-09-14
source: centro-elphis
tags: [retell, n8n, api, deprecacion, guardianes]
---

El sustituto no es un alias: `POST /v2/list-calls` devolvía un array y `/v3` devuelve
`{items, pagination_key, has_more}`, y el filtro de fecha pasa de `{lower_threshold}` a
tipado (`{type:'number',op:'ge',value}`) — el estilo viejo da **400**, no se ignora.

Cambiar solo la URL rompe **en silencio, y justo en los guardianes**:
- `Array.isArray(body) ? body : (body.calls ?? null)` → `null` → la rama «sin respuesta
  útil, no avisar» del propio guardián, con el latido escribiéndose igual.
- En n8n un array de respuesta se parte en items y un objeto va como **1 item**: el código
  aguas abajo filtra por `call_id`, ve 0 candidatas y marca la corrida como buena.

Fix: URL + cuerpo + parser en **el mismo PUT**, nunca por fases. Y se ensaya en seco antes
de tocar prod: extraer el `jsCode` real del nodo, correrlo en Node con `$`/`$input`
simulados contra respuestas **reales** de las dos versiones y exigir salida idéntica; más
el control negativo (código viejo + respuesta nueva) para ver de qué color es el fallo.

Ver [[un-verificador-se-estrena-contra-el-estado-de-antes-del-cambio]] ·
[[clientes/centro-elphis/index|centro-elphis]]
