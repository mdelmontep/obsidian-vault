---
title: op read — el secreto nunca debe aparecer literal en un comando bash, ni copiado desde memoria
date: 2026-07-04
source: claude-code-session
tags: [seguridad, 1password, credenciales, claude-code]
---
El clasificador de seguridad de Claude Code bloquea cualquier comando bash que contenga un secreto en texto plano — incluso un simple `curl` de solo lectura — si el JWT/API key aparece literal en el comando, venga de donde venga (pegado a mano, o copiado de un memory file de sesiones previas).

Fix: consumir SIEMPRE `op read "op://vault/item/campo"` inline dentro del mismo comando que lo usa (`TOKEN=$(op read ...) && curl -H "X-KEY: $TOKEN" ...`), nunca en dos pasos donde el valor quede visible en un comando intermedio o en el transcript.

Si `op` da `authorization timeout` (desktop app sin aprobar), NO caer en el atajo de usar un token guardado en memoria del agente pegándolo literal — vuelve a fallar igual, más la reautorización sigue pendiente. Pedir al usuario que reautorice 1Password antes de reintentar.
