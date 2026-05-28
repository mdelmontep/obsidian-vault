---
title: openai chat completions pdf → image_url no type:file
date: 2026-05-28
source: claude-code-session
tags: [openai, n8n, ocr, api]
---

`type:'file'` con `file_data` es formato exclusivo de la Responses API (`/v1/responses`).
Chat Completions (`/v1/chat/completions`) no lo acepta → 400 inmediato.

Para enviar PDFs a gpt-4o/gpt-4o-mini via Chat Completions:
```
{ type: 'image_url', image_url: { url: 'data:application/pdf;base64,' + b64 } }
```

Guards adicionales en el mismo nodo:
- Si `b64` es undefined → la URI queda `...base64,undefined` → 400. Guard explícito antes de la llamada.
- MIME `image/jpg` (sin 'e') → OpenAI rechaza. Normalizar: `mime === 'image/jpg' ? 'image/jpeg' : mime`.
- El catch de httpRequest en n8n traga el body real de OpenAI. Capturar `e.cause?.response?.data`.
