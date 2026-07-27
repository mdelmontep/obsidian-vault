---
title: para validar un salto de Chromium se compara A/B con el mismo código, no se mira si el build pasa
date: 2026-07-27
source: claude-code-session
tags: [pdf, puppeteer, docker, qa, verificacion]
---

Subir de Node obliga a subir de Alpine, y con Alpine sube Chromium (131 → 149 en el caso
real). Que el build pase no dice NADA del render: el riesgo es la paginación, las fuentes y
los saltos de página del documento que se le manda al cliente.

Método que funcionó (TuFacturaIA #1257), reproducible en cualquier proyecto con PDF:

1. Construir DOS imágenes, la de `main` y la nueva. Mismo código, misma fuente, la única
   variable es el motor.
2. Payload del propio repo (aquí `SAMPLE_DATA` + `DEFAULT_TEMPLATE_CONFIG`), no inventado.
   Añadir una variante larga (60 líneas) que fuerce multipágina: ahí es donde muerde.
3. Comparar, en este orden de valor:
   - nº de páginas y tamaño de página (`pdfinfo`) — un cambio aquí es un bug seguro;
   - texto extraído con `pdftotext -layout` — diff exacto, caza reflow y contenido;
   - píxeles: `pdftoppm -gray -r 100` a PGM y diff propio (el formato P5 se parsea en 15
     líneas de Node, no hace falta ImageMagick).
4. Un 0,0x % de píxeles distintos con delta bajo (<20/255) concentrado en bordes y glifos es
   antialiasing: mirar el recorte a 200 dpi antes de darlo por bueno. Un desplazamiento real
   da deltas cercanos a 255.

Corolario: los PDF de Chromium 149 pesaban ~25 % menos con contenido idéntico (mejor
subsetting). El tamaño del fichero no es señal de nada.

Ver [[dependabot-no-avisa-de-eol-de-runtime]] · [[colima-solo-monta-home-el-bind-mount-de-tmp-crea-un-directorio]]
