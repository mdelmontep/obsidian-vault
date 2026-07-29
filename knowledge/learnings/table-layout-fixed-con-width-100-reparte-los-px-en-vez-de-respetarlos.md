---
title: table-layout fixed reparte los px declarados salvo que la tabla mida width 0
date: 2026-07-29
source: claude-code-session
tags: [css, tablas, frontend]
---

Con `table-layout: fixed`, si el ancho de la tabla NO coincide con la suma de
los anchos de columna, el navegador reparte la diferencia **en proporción** a
los px declarados: dejan de ser anchos y pasan a ser pesos.

`width: 100%` reparte el ancho del contenedor (2230 px declarados en 1090 de
sitio → la columna de 260 se queda en 164 y recorta con "…"). **`max-content`
no lo arregla**: reparte el del contenido, que con textos largos es aún mayor
(2280 px), así que arrastrar una columna a 81 px la dejaba en 232 y no había
forma de estrecharla. Firma inconfundible: TODAS las columnas escaladas por el
mismo factor (medido 1,43).

```css
.tablaResizable { table-layout: fixed; width: 0; min-width: 100%; }
```

`width: 0` es el único valor sin diferencia que repartir: en layout fixed la
tabla no puede ser más estrecha que sus columnas, así que adopta su suma exacta.
`min-width: 100%` exige un `<th aria-hidden>` spacer final SIN ancho declarado —
el sobrante va primero a las columnas sin ancho, así se lo queda entero y las
demás conservan el suyo. Sin spacer, vuelve el reparto.

Al medir el recorte, mide el nodo del texto, no el `<th>`: si lleva tirador de
resize, su `scrollWidth` es 3 px mayor siempre. Distinto de
[[table-layout-fixed-columnas-porcentaje]], que va de % por variante.
