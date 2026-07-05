---
title: op read — el secreto nunca debe aparecer literal en un comando bash, ni copiado desde memoria
date: 2026-07-04
source: claude-code-session
tags: [seguridad, 1password, credenciales, claude-code]
---
El clasificador de seguridad de Claude Code bloquea cualquier comando bash que contenga un secreto en texto plano — incluso un simple `curl` de solo lectura — si el JWT/API key aparece literal en el comando, venga de donde venga (pegado a mano, o copiado de un memory file de sesiones previas).

Fix: consumir SIEMPRE `op read "op://vault/item/campo"` inline dentro del mismo comando que lo usa (`TOKEN=$(op read ...) && curl -H "X-KEY: $TOKEN" ...`), nunca en dos pasos donde el valor quede visible en un comando intermedio o en el transcript.

Si `op` da `authorization timeout` (desktop app sin aprobar), NO caer en el atajo de usar un token guardado en memoria del agente pegándolo literal — vuelve a fallar igual, más la reautorización sigue pendiente. Pedir al usuario que reautorice 1Password antes de reintentar.

**Extraer/mover secretos (no solo usarlos):** al SACAR secretos de un sitio (p.ej. `docker exec <cont> env` de un Dokploy) para consolidarlos en 1Password, nunca a stdout — redirige a un fichero temporal (`> f`), `op` lo consume inline, y borra el fichero al final. Trampa: el fallback habitual cuando el clasificador bloquea un SSH read-only («que el usuario lo corra con `! comando`») **volcaría el `env` entero al transcript** → expone los secretos. Ese fallback solo vale para comandos SIN valores (un `docker ps`). Para el `env`: o autorizas el SSH y rediriges a fichero, o el usuario extrae/pega los valores él (exposición cero).
