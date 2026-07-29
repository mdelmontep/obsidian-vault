---
title: grid en el li manda el texto suelto a la columna del bullet (una palabra por línea)
date: 2026-07-29
source: claude-code-session
tags: [css, grid, maquetacion]
---

Patrón que parece limpio y rompe: bullet propio con `::before` + rejilla de dos columnas.

```css
li{display:grid;grid-template-columns:8px 1fr;gap:14px}
li::before{content:"";width:6px;height:6px;border-radius:50%}
```

Con `<li><strong>Título.</strong> resto del texto…</li>` el `<strong>` ocupa la celda `1fr` y el
**texto suelto de después se convierte en un ítem anónimo de rejilla** que cae en la siguiente
celda: la columna de 8 px. Resultado, una palabra por línea durante párrafos enteros.

Todo contenedor `grid`/`flex` convierte cada corrida de texto en ítem anónimo. La regla: **un
contenedor grid/flex no lleva texto suelto entre sus hijos**, o lo envuelves en un `<span>`, o
no usas grid ahí.

Fix sin rejilla, inmune al problema:

```css
li{position:relative;padding-left:22px}
li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;border-radius:50%}
```

Se ve **solo abriéndolo en el navegador**: el HTML es válido, el CSS es válido y no hay warning
en ninguna parte. Caso 2026-07-29: artifact publicado y entregado con la sección final ilegible.
