---
title: n8n code nodes no interpolan {{ }} — al migrar http→code el body va como objeto
date: 2026-06-01
source: claude-code-session
tags: [n8n, code-node, refactor]
---
Al convertir un nodo **HTTP Request → Code** (p.ej. para firmar HMAC), su `jsonBody`
(`={ "x": {{ $('Nodo').first().json.y }} }`) NO se puede copiar tal cual al `jsCode`:
los Code nodes **no evalúan `{{ }}`**. El string literal (incl. `={` y `{{ }}`) se
manda como body → JSON inválido → el endpoint responde 400.

Fix: construir el body como **objeto JS real**:
`const body = { x: $('Nodo').first().json.y };` (el helper hace `JSON.stringify`).

Síntoma **silencioso**: lo que depende del response (un IF sobre `ok===true`) cae
SIEMPRE a la rama false; nada peta visiblemente. Puede pasar desapercibido si otra
ruta enmascara el efecto.

Caso real: `Cambiar Sticky Org`/`Cambiar Sticky Auto` (`pqSWkDIHqmSVHotB`) — el
refactor HTTP→Code para HMAC v2 dejó el body como literal → **toda la selección
multi-org del bot rota ~2 semanas**, enmascarada por una sticky de otra fuente
(`web_switch`). Relacionado: [[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]] · [[n8n-emailsend-html-no-evalua-expresiones]].
