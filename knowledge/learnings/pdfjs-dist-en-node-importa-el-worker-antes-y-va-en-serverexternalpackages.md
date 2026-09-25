---
title: pdfjs-dist en node importa el worker antes y va en serverexternalpackages
date: 2026-09-25
source: facturaia
tags: [pdfjs, nextjs, pdf, standalone]
---
Leer la capa de texto de un PDF en un route handler de Next (standalone, Alpine) con `pdfjs-dist` falla sin error claro si no se hacen tres cosas:

- **Importar el worker a mano ANTES del módulo**: `await import('pdfjs-dist/legacy/build/pdf.worker.mjs')` y luego `pdf.mjs`. En Node no hay hilo aparte y pdfjs busca el manejador en `globalThis.pdfjsWorker`. La ruta literal además hace que el trazado del build lo meta en el standalone.
- **`serverExternalPackages: [..., 'pdfjs-dist']`** en `next.config.ts`: bundlearlo rompe la carga del worker.
- **Pasar una copia del buffer** (`data: pdf.slice()`): pdfjs lo transfiere y deja inservible el original para quien lo use después (p. ej. el OCR).

Usar el build `legacy/` y `isEvalSupported: false`. Envolver en try/catch y degradar: si pdfjs no carga, el resto del flujo debe seguir.

Caso: candado de cabecera del OCR del ticket 185 ([[facturaia]], PR #2980).
