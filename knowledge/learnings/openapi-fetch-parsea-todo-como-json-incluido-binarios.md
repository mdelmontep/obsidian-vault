---
title: openapi-fetch parsea todo como JSON, también binarios
date: 2026-05-20
source: claude-code-session
tags: [openapi-fetch, http, pdf, binary, content-type]
---

## Síntoma
Endpoint OpenAPI que antes devolvía JSON `{url}` ahora devuelve PDF binario directo (Content-Type: `application/pdf`) → `openapi-fetch` revienta:
`Unexpected token '%', "%PDF-1.4\n%"... is not valid JSON`

## Causa
`openapi-fetch` asume JSON y hace `await response.json()` independientemente del Content-Type real. No respeta cambios de tipo de respuesta.

## Fix
Bypass `openapi-fetch` con `fetch` nativo + negociación por Content-Type cuando el endpoint **puede** devolver binario:
- `application/pdf` → stream con `Content-Disposition: inline`
- `application/json` con `{url}` → 302 redirect (compat retro)

## Apply check
Cualquier endpoint `/.../pdf`, `/.../export`, `/.../download` — sospechar y leer doc del proveedor antes de usar `client.GET(...)` tipado.
