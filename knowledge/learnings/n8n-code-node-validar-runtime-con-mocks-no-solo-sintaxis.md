---
title: validar un n8n code node en runtime con mocks antes de desplegarlo, no solo la sintaxis
date: 2026-06-04
source: claude-code-session
tags: [n8n, deploy, testing]
---
Editar un Code node y validar solo que parsea (`new Function(code)`) NO caza
`ReferenceError`: una variable usada pero no definida (p.ej. tras eliminar un
`const`) compila bien y revienta en ejecución. Caso real: recableé el OCR del bot
WhatsApp prod, eliminé `const bandeja = bandejaRow` pero el `return` seguía usando
`bandeja` → sintaxis OK, prod roto (`bandeja is not defined`), bot caído ~10 min.

Fix antes de cualquier PUT a un workflow en producción: ejecutar el jsCode con un
harness `AsyncFunction` y mocks de `$env` (Proxy), `$()` (devuelve `{first:()=>({json})}`),
`$input`, `this.helpers.httpRequest` (registra llamadas) y `require`. Correr el flujo
y aserir: no lanza, el payload saliente trae todos los campos, el `return` tiene el
shape esperado. Eso reproduce el ReferenceError en local. Mantener backup + revert listo.
Relacionado: [[n8n-api-put-workflows-rechaza-settings-desconocidos]].
