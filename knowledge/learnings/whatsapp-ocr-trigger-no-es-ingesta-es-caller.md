---
title: ocr whatsapp — ingesta almacena, el caller dispara ocr-process por separado
date: 2026-06-30
source: claude-code-session
tags: [whatsapp, ocr, n8n, arquitectura]
---

Al portar el flujo WhatsApp de n8n a Next.js, ingesta y OCR son dos llamadas separadas.

- `ingesta`: descarga media → Storage + BD (`bandeja_ingesta` estado=`procesando`) → devuelve IDs
- `ocr-process`: recibe base64 + IDs → OpenAI Vision → actualiza BD

n8n hacía las dos en secuencia. Next.js solo portó ingesta.
Resultado: bandeja queda en `procesando` indefinidamente → stale-sweep la marca `error` a los 30min.

Fix: en el caller (webhook/upload/email), tras ingesta exitosa (non-idempotent),
`void callOcrProcess({ org_id, org_nombre, factura_id, bandeja_id, media })` fire-and-forget.

El base64 ya está en memoria — no hace falta re-descargarlo de Storage.
