---
title: n8n jsonbody stringify evita control characters
date: 2026-04-29
source: claude-code-session
tags: [n8n, http-request, error-handler]
---

En `HTTP Request.jsonBody`, NO interpolar valores entre comillas literales:

```
"stack": "{{ $json.error_stack }}"   ❌ rompe con \n, comillas, controls
```

Usar `JSON.stringify` (sin comillas externas, ya las pone):

```
"stack": {{ JSON.stringify($json.error_stack) }}   ✅
```

Síntoma: `Bad control character in string literal in JSON at position N`.

Caso típico: error handlers que pasan `stack`, `message`, `description` o cualquier valor que pueda contener saltos de línea, comillas o caracteres de control.

Aplica también a LITERALES con `\n` dentro de la expresión (fallbacks
`{{ x || 'línea1\n\nlínea2' }}`), no solo a valores de `$json`. Síntoma
alternativo: body vacío → API destino rechaza campo requerido (Meta
`text.body is required`), sin error de control character.
