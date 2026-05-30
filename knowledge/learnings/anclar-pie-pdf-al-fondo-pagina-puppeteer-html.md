---
title: anclar pie de factura al fondo de página en pdf html→puppeteer
date: 2026-05-30
source: claude-code-session
tags: [pdf, puppeteer, css]
---

Plantilla HTML renderizada a PDF con Puppeteer (`page.pdf({ format:'A4', margin:0 })`, contenedor 794px). El bloque de pie (datos bancarios / contacto / notas) flotaba justo tras los totales, dejando hueco blanco hasta el fondo.

Fix (facturas de 1 página):
- Raíz de la plantilla: `display:flex; flex-direction:column; min-height:1122px; box-sizing:border-box` (A4 @96dpi = 794×1122).
- Spacer antes del pie: `<div style={{flexGrow:1, minHeight:0}} />` → empuja el pie al fondo.

`minHeight:0` (no >0) en el spacer: si la factura desborda a 2+ páginas el spacer colapsa y el pie fluye tras el contenido (anclar a CADA página requeriría running-footer de Puppeteer, más complejo). Verificable midiendo `rootH===1122` y posición del pie.
