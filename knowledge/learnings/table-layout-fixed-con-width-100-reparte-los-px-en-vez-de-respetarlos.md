---
title: table-layout fixed con width 100% reparte los px declarados en vez de respetarlos
date: 2026-07-29
source: claude-code-session
tags: [css, tablas, frontend]
---

Columnas redimensionables con anchos en px (`<th style="width:260px">`) y
`table-layout: fixed`: si la tabla lleva `width: 100%`, esos px NO son anchos,
son **proporciones**. El navegador ajusta la suma al ancho del contenedor, así
que con 2230 px declarados en 1090 de sitio la columna de 260 se queda en 164 y
recorta con "…" mientras cinco columnas de guiones conservan sus 120-150.

Síntoma que despista: "hay sitio de sobra al lado y aun así pone puntos
suspensivos". No es el padding ni el `text-overflow`.

```css
.tabla { width: 100%; }                 /* la culpable */
.tablaResizable { table-layout: fixed; width: max-content; min-width: 100%; }
```

`max-content` respeta cada ancho y el wrapper (`overflow-x: auto`) desplaza;
`min-width: 100%` evita que quede corta si sobra sitio. El precio es scroll
horizontal permanente en catálogos anchos: si no lo quieres, esconde columnas
por defecto, no reduzcas anchos.

Al medir el recorte, mide el nodo del texto, no el `<th>`: si lleva tirador de
resize, su `scrollWidth` es 3 px mayor siempre y da falso positivo en todas.
Distinto de [[table-layout-fixed-columnas-porcentaje]], que va de % por variante.
