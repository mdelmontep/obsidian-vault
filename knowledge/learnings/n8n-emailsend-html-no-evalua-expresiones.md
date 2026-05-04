---
title: n8n emailsend html no evalúa expresiones embebidas
date: 2026-05-04
source: claude-code-session
tags: [n8n, email, expresiones]
---

El campo `html` del nodo emailSend trata cualquier sintaxis embebida como texto literal:
- `={{ $('Node').item.json.field }}` → literal
- `{{ $('Node').item.json.field }}` → literal
- `` =`...${expr}...` `` (template literal) → literal

**Fix**: Code node antes del email que construye el HTML con template literals JS reales.

```
Code node:
const d = $('Preparar Datos').item.json;
const html = `<html>...${d.nombre}...</html>`;
return [{ json: { html } }];

Email node:
html = ={{ $('Build Email HTML').item.json.html }}
```

El email node con `={{ expr }}` como valor entero SÍ se evalúa.
Caso real: Clínica Zen 2026-05, Code node "Build Emails HTML".
