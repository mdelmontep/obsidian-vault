---
title: table-layout fixed — % por variante deben sumar igual (gaps + última col px)
date: 2026-04-27
source: claude-code-session
tags: [css, tablas, frontend, facturaia]
---

Con `table-layout: fixed`, los anchos en % se gestionan por clase variante de la tabla (`has-vf`, `has-origen`) y deben sumar de forma consistente. Dos fallos del mismo origen:

1. **Gaps**: si los % no suman 100% (descontando las columnas de px fijo), el navegador reparte el sobrante entre las columnas porcentuales → una se infla y los elementos quedan desalineados. Ej: `13+19+10+10+9+10+9+10 = 90%` → 10% repartido.
2. **Última columna px se desplaza**: añadir una columna condicional (ej. "Origen" solo en recibidas) sin reajustar los % comprime la última columna de ancho fijo (acciones / menú ⋯), que aparece en distinta posición horizontal entre variantes.

**Fix (ambos)**: descontar las px fijas del 100% mental, repartir el resto en %, y que **cada variante sume exactamente lo mismo**:

```css
.fact-table .col-num { width: 13%; }            /* base */
.fact-table.has-origen .col-num { width: 12%; } /* variante: idéntico total */
.fact-table.has-origen .col-origen { width: 7%; }
```
