---
title: un test de render no ve una colisión visual — hay que rasterizar y mirar
date: 2026-07-31
source: claude-code-session
tags: [testing, pdf, frontend, qa]
---
47 tests verdes sobre el HTML renderizado (contiene el texto, respeta el orden, no duplica
el bloque, escapa el XSS) y el documento salía **roto**: los descendentes de la última línea
del párrafo ("p", "q", "j", "y") TOCABAN el filete superior de la tabla. En la plantilla que
pinta esa cabecera sobre una banda de color, quedaban encima de ella.

Ninguna aserción sobre el DOM puede cazar eso: la colisión existe en el layout, no en el
markup. La única evidencia es la imagen — `pdftoppm -r 150 -png` y mirarla.

Causa raíz reutilizable: **un valor de espaciado copiado de otro renderizador no lleva su
contexto**. En los PDFs de Obras `paddingBottom: 0` vale porque el elemento siguiente trae
su propio margen; al portar el bloque a facturas el siguiente elemento era el `<thead>`.
Al copiar espaciado, mirar **quién va debajo**, no solo cómo se veía en el origen.

Y el fixture importa: con un texto de una línea no se reproduce. Hacen falta 3-4 líneas y
descendentes en la última. Caso FacturaIA ticket e5dc74e7 (PR #1403), 4 de 5 plantillas.
Ver [[la-aguja-de-una-asercion-sobre-el-documento-entero-debe-ser-unica-de-la-feature]]
