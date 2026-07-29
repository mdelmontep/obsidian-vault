---
title: pdf escaneado sin capa de texto — renderizar páginas con pdftoppm, no insistir con grep
date: 2026-07-29
source: claude-code-session
tags: [pdf, herramientas, lectura-documentos]
---

`pdftotext -layout` que devuelve **0 líneas** en un PDF de 40 MB = escaneo de papel, no hay capa
de texto. Ni grep ni `--filter` van a encontrar nada nunca. No hay tesseract instalado en este
Mac (ni PIL ni ImageMagick), así que la vía es **renderizar y leerlo como imagen**:

- `pdftoppm -jpeg -r 130 -f <desde> -l <hasta> in.pdf out/prefijo` — 130 dpi basta para leer
  prosa y capturas de pantalla; 80 dpi vale solo para localizar en el índice.
- **Recortar sin ImageMagick**: `pdftoppm` acepta `-x -y -W -H` en píxeles del render. Es la
  única forma de sacar una figura suelta (`sips` solo recorta centrado).
- Comprimir para incrustar: `sips -s format jpeg -s formatOptions 68 -Z 900 a.png --out a.jpg`.

**Gotcha que cuesta 3 renders**: el número impreso en el pie NO es el índice físico de página.
Aquí el desfase era +1 al principio y +3 a partir de la mitad (páginas sin numerar intercaladas).
Localiza por el índice, salta a `física ≈ impresa + 1`, lee el pie de esa página y recalibra.

Ver [[la-copia-durable-de-una-fuente-efimera-se-hace-el-mismo-dia-o-no-se-hace]]
