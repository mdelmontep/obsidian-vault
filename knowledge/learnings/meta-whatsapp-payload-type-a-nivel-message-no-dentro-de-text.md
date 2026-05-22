---
title: Meta WhatsApp Cloud payload — type está a nivel del message, no dentro de text
date: 2026-05-22
source: claude-code-session
tags: [meta, whatsapp, payload]
---

El campo `type:"text"|"image"|"audio"|"document"` está en el objeto `message`, NO dentro de `message.text`. Estructura real:

```json
"messages": [{
  "from": "34600000095",
  "id": "wamid.X",
  "timestamp": "1716397200",
  "type": "text",
  "text": { "body": "Hola" }
}]
```

Si tu payload de test pone `text.type` (mal ubicado), el parser legítimo descarta el mensaje como non-text y `Parse Meta payload` devuelve `_outcome:"ignored_non_text"` aunque el body sea correcto.

Heurística: capturar 1 payload real desde el sandbox Meta antes de codificar el parser. No fiarse del JSON de ejemplo de la doc (cambia entre v18 y v21).

Caso real Elphis 2026-05-22: smoke E2E del wa-inbound-bridge fallaba silenciosamente con `ignored_non_text` porque mi simulación del payload Meta tenía `type` mal ubicado.
