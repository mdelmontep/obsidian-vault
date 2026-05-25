---
title: pdf como adjunto en email queda congelado en el inbox del destinatario
date: 2026-05-26
source: claude-code-session
tags: [email, ux, debugging, transactional]
---

Si el email se envía con el PDF como **adjunto base64** (`Resend.attachments`, SendGrid attachments, etc.), el destinatario conserva ese blob congelado en su inbox aunque el PDF de origen (Storage, CDN) se actualice. Solo el reenvío con buffer fresco refresca lo que ve el cliente. Si se envía como **enlace** (signed URL), el cliente al hacer clic descarga la versión actual del blob.

Trade-offs reales: adjunto funciona offline + sin token expiry + el cliente puede archivar y reabrir sin volver al servicio. Link siempre actualizado + bypass del límite spam-attachments + auditable (sabes quién abrió y cuándo). Para facturas/contratos legales, adjunto suele ganar (inmutabilidad + el cliente tiene copia propia). Para previews o documentos en revisión, link gana.

Caso real TuFacturaIA 2026-05-26: usuario regenera PDF de factura A2026-0028 con descripción nueva. Storage actualizado, abre en `/emitidas` y la ve correcta. El cliente que recibió el email original sigue viendo el PDF antiguo sin descripción — el adjunto en su correo es el blob de la emisión inicial. Solo "Reenviar email" lo arregla. `src/lib/email/send-factura.ts:233` descarga `pdfBuffer` de Storage en cada envío, así que el reenvío sí lleva la versión actual.

Ver [[cache-invalidation-artifacts-emitidos]] y [[etag-por-path-upsert-stale-304]].
