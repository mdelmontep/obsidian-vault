---
title: visor pdf en next — iframe nativo da cromo feo, usar react-pdf con dynamic ssr:false
date: 2026-05-30
source: claude-code-session
tags: [next, pdf, frontend]
---

`<iframe src="*.pdf">` usa el visor nativo de Chrome: barra de herramientas oscura, panel de miniaturas y bandas grises alrededor de la hoja. No se puede estilar (es plugin del navegador) y no llena el recuadro.

Fix: renderizar con `react-pdf` (pdf.js) a `<canvas>` — `<Document file={url}><Page width={ancho} renderTextLayer={false} renderAnnotationLayer={false}/>`. La hoja llena el ancho edge-to-edge.

Inviolables:
- **Cargar con `next/dynamic { ssr: false }`** — pdf.js referencia `DOMMatrix` en module-eval → `ReferenceError` en SSR (Node). Wrapper aparte para que react-pdf solo entre en el chunk client.
- Worker: `pdfjs.GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url).toString()`.
- Verificación: headless Chromium NO pinta iframes PDF (sale blanco) pero SÍ el canvas de pdf.js → testeable con Playwright.
