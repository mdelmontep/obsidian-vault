---
title: postgrest .or() con + en valor requiere URL-encoding manual
date: 2026-05-18
source: claude-code-session
tags: [supabase, postgrest, gotcha]
---

PostgREST `.or(whatsapp_phone.eq.+34611111111,...)` con `+` literal en el
valor falla en match porque `+` se interpreta como espacio en query string
HTTP. Necesita ser `%2B`.

- Cliente JS de Supabase: lo hace automáticamente. Sin acción.
- Llamadas REST manuales con curl/fetch: hay que URL-encodear el `+` como `%2B`.
- Helper bash: `--data-urlencode` o `python3 -c "import urllib.parse; print(urllib.parse.quote('+34611...'))"`.

Síntoma del bug: query devuelve 0 filas aunque la fila existe en BD.
Detección: probar con número sin `+` primero y luego con `+` para confirmar
que el encoding es la causa.

Aplicable a cualquier `.eq()`, `.ilike()`, `.or()` con valores que contengan
`+`, `&`, `=`, `#`, espacios, o caracteres no-ASCII.
