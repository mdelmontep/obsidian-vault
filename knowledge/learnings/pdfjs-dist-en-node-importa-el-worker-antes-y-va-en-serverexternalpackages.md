---
title: pdfjs-dist en node importa el worker antes y va en serverexternalpackages
date: 2026-09-25
source: facturaia
tags: [pdfjs, nextjs, pdf, standalone]
---
Leer la capa de texto de un PDF en un route handler de Next (standalone, Alpine) con `pdfjs-dist` falla sin error claro si no se hacen tres cosas:

- **Importar el worker a mano ANTES del módulo**: `await import('pdfjs-dist/legacy/build/pdf.worker.mjs')` y luego `pdf.mjs`. En Node no hay hilo aparte y pdfjs busca el manejador en `globalThis.pdfjsWorker`. La ruta literal además hace que el trazado del build lo meta en el standalone.
- **`serverExternalPackages: [..., 'pdfjs-dist']`** en `next.config.ts`: bundlearlo rompe la carga del worker.
- **Pasar una copia como `Uint8Array` llano** (`data: new Uint8Array(pdf)`): pdfjs transfiere el buffer y además **rechaza un `Buffer` de Node** («Please provide binary data as `Uint8Array`»). `pdf.slice()` sobre un `Buffer` sigue siendo `Buffer`: el candado del ticket 185 devolvió null en prod del 25-sep al 2-oct sin un solo error visible (#3209).
- **El test debe pasar lo mismo que la ruta**: los tests usaban el `Uint8Array` de pdf-lib y daban verde; la ruta pasaba `Buffer.from(blob)`. Un guard que nunca lanza y degrada a null esconde que nunca funcionó: medirlo en prod con un caso que DEBE disparar.

Usar el build `legacy/` y `isEvalSupported: false`. Envolver en try/catch y degradar: si pdfjs no carga, el resto del flujo debe seguir.

Caso: candado de cabecera del OCR del ticket 185 ([[facturaia]], PR #2980).
