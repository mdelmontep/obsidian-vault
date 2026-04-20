---
title: pdf-lib funciona en next.js turbopack donde pdfkit falla
date: 2026-04-20
source: claude-code-session
tags: [nextjs, pdf, turbopack, facturaia]
---

PDFKit depende de archivos `.afm` en `node_modules/pdfkit/js/data/` que Turbopack no incluye en el bundle → error `ENOENT: no such file or directory, open '/ROOT/node_modules/pdfkit/js/data/Helvetica.afm'`.

`pdf-lib` embebe fuentes estándar en JS puro, funciona sin archivos externos.

```ts
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib'

const doc = await PDFDocument.create()
const page = doc.addPage([595.28, 841.89]) // A4
const helvetica = await doc.embedFont(StandardFonts.Helvetica)
const helveticaBold = await doc.embedFont(StandardFonts.HelveticaBold)

page.drawText('FACTURA', { x: 50, y: 780, size: 22, font: helveticaBold })
// ...
const pdfBytes = await doc.save() // Uint8Array, listo para subir a Storage
```

Descubierto en FacturaIA al intentar generar 60 PDFs de facturas seed. pdfkit falló en los 60; pdf-lib generó los 60 sin errores.
