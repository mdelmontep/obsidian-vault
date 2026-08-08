---
title: el objetivo táctil de un control compuesto es su hijo, no el control
date: 2026-08-08
source: claude-code-session
tags: [css, accesibilidad, design-system, testing]
---

En un control con riel + opciones (Segmented, tabs, toggle group) lo que se pulsa
es la OPCIÓN, no el riel. El riel medía 28 px y cumplía; la opción medía
`28 − 2×borde − 2×padding = 20`, por debajo de los 24×24 de WCAG 2.5.8 AA con
puntero fino. La excepción por separación no salva: las opciones son adyacentes.

Arreglo sin mover el layout de los 58 sitios donde sale el control: extender el
área pulsable **sin tocar la caja visible**, con un pseudo del hijo que se coma
el padding del riel.

```css
.btn::after { content:''; position:absolute; inset-inline: 0;
              inset-block: calc(-1 * var(--seg-pad, 0px)); }
```

`inset-inline: 0` no es cosmético: si dos opciones adyacentes extendieran a lo
ancho se pisarían y el clic iría a la de encima. Y no lo estires a 44 px en
táctil: un área que desborda la caja del control le roba el toque al vecino de la
misma fila; si hace falta la AAA, se usa la talla grande ahí.

**Y el guard**: medir la altura del riel NO mide el objetivo. Deriva la cuenta de
las declaraciones reales y **resuelve el alto desde lo que la talla DECLARA, no
desde el token que se supone que usa** — poner un literal dejaba el test verde
midiendo una altura que ya no existía. Comprueba los DOS ejes: una opción de un
carácter no tiene más ancho que su relleno.

TuFacturaIA #1549. Relacionado:
[[el-tap-target-del-boton-compartido-es-el-suelo-de-la-altura-de-fila]] ·
[[columna-congelada-se-tapa-con-altura-y-con-apilado]]
