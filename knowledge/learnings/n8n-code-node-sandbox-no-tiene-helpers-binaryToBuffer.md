---
title: n8n code node sandbox no tiene helpers.binaryToBuffer
date: 2026-04-20
source: claude-code-session
tags: [n8n, facturaia, ocr]
---

En modo task runner (default en n8n reciente), el sandbox del Code Node no tiene acceso a `this.helpers.binaryToBuffer()` ni otras helpers de binario. Error: "helpers.binaryToBuffer not supported in Code Node".

**Solución**: mover la conversión binario→base64 al caller que tenga Node.js completo. En FacturaIA, el API route de Next.js (`/api/upload`) convierte el archivo a base64 con `Buffer.from(arrayBuffer).toString('base64')` y lo envía en el body JSON del webhook a n8n. El Code Node de n8n solo construye el request para OpenAI Vision usando ese base64 ya listo.

**Patrón general**: si n8n necesita procesar binario pesado, hacerlo ANTES de que llegue al Code Node — ya sea en el caller o usando nodos nativos de n8n (HTTP Request con binary, Move Binary Data, etc.).
