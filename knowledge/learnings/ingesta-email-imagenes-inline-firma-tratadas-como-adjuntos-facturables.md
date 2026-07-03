---
title: ingesta de email por MIME allowlist mete logos de firma como si fueran facturas
date: 2026-07-03
source: claude-code-session
tags: [email, ocr, gmail, microsoft-365, imap]
---
Un filtro de adjuntos por MIME+tamaño (PDF/JPG/PNG) no basta: las imágenes de firma/logo embebidas en el HTML del correo (`src="cid:..."`) llegan con `filename` igual que un adjunto real, y pasan el mismo filtro. Resultado: entran a la cola de ingesta/OCR y quedan "sin datos extraídos".

Señal específica por proveedor para descartarlas:
- **Gmail API**: header de la parte `Content-Disposition: inline` (pedir `format=full` para tener headers por parte).
- **Microsoft Graph**: campo `isInline: true` en el objeto de attachment.
- **IMAP genérico**: `disposition === 'inline'` en el `bodyStructure`. Ojo: no basta con excluir solo por eso — hay adjuntos reales sin `Content-Disposition` explícito que sí hay que aceptar si tienen `filename`; el fix es "excluir inline explícito", no "exigir attachment explícito".

Caso real: TuFacturaIA, 3 providers (`google-workspace`, `microsoft-365`, `icloud-mail`), PR #673.
