---
title: signed URL del fetch server-side no se reutiliza como href de email
date: 2026-05-25
source: claude-code-session
tags: [storage, signed-urls, email, ttl, facturaia]
---

Cuando descargas un PDF server-side para adjuntarlo al email (`getDocumentSignedUrl(path, 60)` + fetch inmediato), esa misma URL NO sirve como href del CTA del email — caduca en 60s y el receptor abre el mail minutos/horas después → `InvalidJWT: exp claim timestamp check failed`.

Patrón correcto: firmar DOS URLs distintas.
- TTL corto (60s) para el fetch interno (la consume el server inmediatamente).
- TTL largo (7d) independiente para el cuerpo del email.

Bug real (TuFacturaIA `send-factura.ts`): `downloadPdfFromStorage` propagaba la URL de 60s vía `r.diag.signed_url` al `pdf_url` del template → botón "Descargar factura" caducado en cuanto el cliente abría el mail. Fix `52b2ab9`: separar firmas, igual que `send-presupuesto.ts:174` ya hacía. Relacionado [[signed-url-proxy-endpoint-vs-cached-en-bd]] (mismo problema de TTL, contexto distinto: aquel es persistir en BD, éste es reusar intra-request).
