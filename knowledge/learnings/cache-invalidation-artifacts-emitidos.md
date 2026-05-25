---
title: artifacts emitidos no se regeneran al cambiar dato fuente
date: 2026-05-25
source: claude-code-session
tags: [debugging, cache, ux, arquitectura]
---

Cuando el user reporta "X no aparece en Y" sobre un artifact ya emitido/cacheado (PDF de factura, email enviado, HTML estático, thumbnail procesado, PDF firmado eIDAS), el primer reflejo debe ser **comprobar si Y es regenerable o está cacheado**, no buscar bug en el código de render.

Caso real FacturaIA 2026-05-25: user sube logo en `/settings → Branding`. Genera factura nueva → logo aparece OK. Abre factura YA EMITIDA antes del upload → logo NO aparece. Causa: el PDF se generó al EMITIR (vía `renderAndUploadFacturaPdf`) y quedó cacheado en Supabase Storage `facturas/{orgId}/factura/{num}.pdf`. Cambiar `organizations.logo_url` afecta a emisiones futuras, no re-renderiza PDFs históricos.

**Patrón general**: cambiar dato fuente ≠ regenerar artifacts derivados. Aplica a:
- PDFs de facturas, presupuestos, abonos (cacheados en Storage al emitir).
- Emails enviados (ya en el servidor del destinatario).
- HTML estático/SSG pre-renderizado.
- Thumbnails procesados, imágenes redimensionadas.
- PDFs firmados eIDAS / sellados TSA (timestamp no se recalcula).
- Documentos AEAT registrados (RD 1619/2012: factura inmutable, solo rectificable vía abono).

**Fix UX**: ofrecer botón "Regenerar" en el detalle del artifact + mensaje preventivo en el upload ("facturas emitidas conservan el original"). NO regenerar automáticamente — la inmutabilidad puede ser requisito legal (fiscal AEAT) o auditoría (eIDAS).

**Fix debug**: antes de tocar render, pedir al user que regenere y reporte si persiste.
