---
title: parse roto de una respuesta 200 se confunde con fallo y duplica el POST
date: 2026-08-24
source: elphis-psicologia
tags: [shell, zsh, api, idempotencia]
---
`echo "$json" | jq` en zsh expande `\n`/`\t` del contenido (echo de zsh interpreta
backslash-escapes por defecto) → jq revienta con "control characters must be escaped"
aunque el JSON fuera válido. Si eso pasa sobre la RESPUESTA de un POST que devolvió
200, el script concluye "falló" y el reintento crea un duplicado silencioso
(caso: workflow n8n creado 2 veces; el 200 estaba ahí, el parse no).

Fix doble:
- `printf '%s' "$var" | jq` siempre; nunca `echo` para datos.
- Ante "el POST falló", separar transporte de parse: mirar `-w "%{http_code}"` o el
  raw ANTES de reintentar. Un parse roto no es un request fallido.
