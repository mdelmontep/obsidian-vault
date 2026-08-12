---
title: una expresión que evalúa a null viaja como el texto "null" y revienta el cast
date: 2026-08-12
source: claude-code-session
tags: [n8n, postgres, expresiones, elphis]
---
`chatwoot-event` fallaba en 1 de cada 5 ejecuciones desde hacía nueve días:
`invalid input syntax for type bigint: "null"`. La causa, en el nodo Postgres:

```
queryReplacement: ={{ $('Build attrs patch').first().json.attributes.clientify_deal_id || null }}
query:            COALESCE($3::bigint, clientify_deal_id)
```

Cuando el lead no traía deal, la expresión evaluaba a null y n8n interpolaba la **cadena**
`"null"` en la lista de parámetros. El `COALESCE` no llega a actuar: el cast `$3::bigint`
casca antes. Y el hermano silencioso: `$4` iba a una columna `text`, así que ahí el `'null'`
**se guardaba** — cinco filas con la cadena literal en vez de NULL.

Fix sin tocar las expresiones: `COALESCE(NULLIF(NULLIF($3,'null'),'')::bigint, columna)`.
Neutraliza el texto y la cadena vacía, y conserva el camino bueno.

Probarlo **contra la BD real con `BEGIN; … ROLLBACK;`** demostrando el rojo con la query vieja
y el verde con la nueva: no hace falta esperar a que entre tráfico para saber si el fix vale.
Aplica a cualquier plantilla que interpole a texto (URLs, headers, cuerpos JSON), no solo n8n.
