---
title: rama de error de un bot no debe loguear respuestas conversacionales como error
date: 2026-06-28
source: claude-code-session
tags: [n8n, observabilidad, llm, gotcha]
---
El nodo "Log Bot Error → Error Agente" (n8n receptor `pqSWkDIHqmSVHotB`) posteaba SIEMPRE `error_kind:llm_error` a `bot_error_log`, incluso para respuestas normales del agente (pedir NIF, "no encuentro el cliente", confirmar, "este mes has emitido 25 facturas"). El flag que distingue éxito de error (`$json.conversacional`) YA existía en el payload, pero solo se usaba para cosmética (prefijo ⚠️ del texto), **no para gatear el side-effect de logging** → `bot_error_log` lleno de no-errores → falsa alerta "spike de errores del bot (backend/IA)".

Patrón: cuando un flag ya distingue éxito/error, debe gatear TODOS los side-effects (log, alerta, métrica), no solo el texto visible. Grep del anti-patrón: flag usado en un ternario de presentación pero no en el `if` que decide si se registra.

Fix n8n: guard al inicio del code node `if ($json.conversacional === true) return [{ json: {...} }]`. Clave: devolver **un item** (no `[]`), porque el logger está en serie en el path que responde al usuario; `[]` cortaría la respuesta. Ver [[codigo-error-de-dominio-es-estado-de-producto-no-error]] y [[n8n-webhook-tool-respond-no-hardcodear-exito-gatear-en-error-nodo]].
