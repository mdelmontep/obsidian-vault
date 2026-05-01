---
title: signed URLs con TTL — exponer proxy endpoint, no cachear en BD
date: 2026-05-01
source: claude-code-session
tags: [storage, signed-urls, arquitectura, ttl, agency-portal, facturaia]
---

Supabase Storage / S3 firman URLs con TTL (1h-24h). Si guardas la signed URL en BD (`pdf_url`, `download_url`...) los enlaces caducan silenciosamente y la UI muestra "Expired Signature" sin error capturable por el código.

Patrón correcto: endpoint proxy que regenera la URL on-demand:

```ts
// /api/.../pdf/[id]/route.ts
export async function GET(_, { params }) {
  // 1. Auth + ownership check
  // 2. Llamar al proveedor → URL fresca con TTL corto (5min)
  // 3. return NextResponse.redirect(url, 302)
}
```

UI usa `<a href="/api/.../pdf/{id}">` — siempre actualizado, sin cache stale ni jobs de refresco.

Bug real: agency-portal guardaba `pdf_url` (signed 1h) en `facturaia_documents`. Tras 1h, enlaces rotos en el portal. Fix: endpoint `/api/facturaia/pdf/[shadowId]` que llama `GET /v1/{tipo}/{id}/pdf` y redirige.
