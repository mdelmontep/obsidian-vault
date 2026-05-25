---
title: pipeline asset con fallback debe devolver razón del fallo no Buffer|null
date: 2026-05-25
source: claude-code-session
tags: [debugging, observabilidad, asset-pipeline]
---

Pipeline típico: bucket → render on-the-fly → cache. Si cada paso retorna `Buffer | null`, cuando el final es `null` se ha perdido la razón crítica (404 / sign url expired / puppeteer crash / red / cuota provider). El consumidor no puede decidir entre reintento, fallback alternativo o aviso al user.

Caso real FacturaIA 2026-05-25: email factura sin PDF adjunto. `downloadPdfFromStorage` retornaba `null` indistinguible para 4 causas: path migrado post-mig 026, sign url firmada expirada, http 5xx del storage, fetch threw. `renderPdfFallback` igual: factura no encontrada, org no encontrada, puppeteer no arranca en Alpine. Email se enviaba sin adjunto y sin warning — bug invisible durante semanas.

**Patrón fix**:

```ts
async function downloadX(...): Promise<{ buffer: Buffer | null; diag: Diag }>
type Diag = { reason: 'ok' | 'sign_failed' | 'http_error' | 'fetch_threw' | 'empty_body'; http_status?: number; error?: string }
```

- Log `console.warn` con diag completo en cada path fallido.
- `payload_meta` del audit log persiste `pdf_attached / pdf_size_bytes / pdf_fallback_used / pdf_storage_error / pdf_fallback_error / pdf_fallback_link`.
- UI/email: si todo falla, **warning visible** con signed URL alternativo (no email mudo).

Aplica a thumbnails, OCR, fetch externo con fallback, render HTML→PDF, image proxy.
