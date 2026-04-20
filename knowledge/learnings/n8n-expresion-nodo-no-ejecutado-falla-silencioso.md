---
title: n8n expresion referenciando nodo no ejecutado falla silencioso
date: 2026-04-20
source: claude-code-session
tags: [n8n, expresiones, bug]
---

En workflows con ramas IF, si un nodo referencia otro que no se ejecutó en esa rama, la expresión falla:

```
={{ $('Create new contacts1').item.json._embedded.contacts[0].id }}
```

Si el contacto ya existía, el flujo va por la rama TRUE → `Create new contacts1` nunca se ejecuta → error.

**Fix**: usar `$if` con `.isExecuted`:

```
={{ $if($('Create new contacts1').isExecuted, 
    $('Create new contacts1').item.json._embedded.contacts[0].id, 
    $('Code in JavaScript1').item.json.primer_contacto.id) }}
```

**Regla**: cualquier expresión que referencia un nodo en una rama condicional debe tener fallback con `$if(...isExecuted, ..., ...)`.

**Caso real**: Leads Entrantes CZ — Append row in sheet1 fallaba para contactos existentes porque referenciaba `Create new contacts1` (rama FALSE) sin fallback.
