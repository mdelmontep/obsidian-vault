---
title: OpenAI vision lee un PDF escaneado del revés si rotas sus páginas con pdf-lib
date: 2026-07-14
source: FacturaIA — auto-orientación OCR (#888)
tags: [ocr, openai, pdf, pdf-lib, facturaia]
---
Un escaneo a 180°/90° hace que OpenAI vision (PDF como `type:'file'`) devuelva
JSON válido pero todo `null` → NO es un fallo detectable, extrae "vacío".

Fix (verificado en prod): rotar las páginas del PDF con **pdf-lib** —
`page.setRotation(degrees((angle+deg)%360))` + `doc.save()` — y reenviarlo.
**OpenAI HONRA el `/Rotate` de cada página al rasterizar** → lee el documento.
pdf-lib es JS puro (Alpine-safe), a diferencia de rasterizar (canvas/pdfjs nativo).

Patrón de auto-orientación con coste controlado: si la 1ª lectura sale vacía,
reintentar `[180,90,270]` y quedarse con la 1ª no vacía — llamadas extra SOLO en
fallos. Para IMÁGENES el equivalente es `sharp(buf).rotate(deg)`; normalizar EXIF
siempre con `sharp().rotate()` sin argumento (gratis). Ver
[[dep-nativa-import-dinamico-defensivo-en-ruta-api]] · [[pdf-lib-funciona-en-nextjs-turbopack-donde-pdfkit-falla]].
