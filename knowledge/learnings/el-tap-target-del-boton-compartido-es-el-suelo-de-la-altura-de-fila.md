---
title: el tap target del botón compartido es el suelo de la altura de fila
date: 2026-07-29
source: claude-code-session
tags: [css, design-system, accesibilidad, frontend]
---

Fila de tabla que no baja por mucho que recortes el `padding` de la celda: el
suelo no es el texto, es el elemento más alto, y en un listado con acciones ese
elemento suele ser el botón. Si alguien subió `size="sm"` a `min-height: 44px`
por tap target, cada fila con acción arrastra 44 px + padding — y `sm` acaba
siendo **más alto que `md`**, que no tiene mínimo. Nadie lo nota al hacerlo,
porque el cambio se revisa en formularios, no en tablas densas.

No lo quites: es una decisión de accesibilidad. Sepáralo por tipo de puntero.

```css
.xs { min-height: 44px; min-width: 44px; }      /* táctil: objetivo completo */
@media (pointer: fine) { .xs { min-height: 28px; min-width: 0; } }
```

28 px va holgado sobre los 24×24 que exige WCAG 2.5.8 AA con ratón, y el táctil
queda igual o mejor que antes (subir solo el alto deja el objetivo en 38×44).

Antes de tocar padding, mide quién manda: recorre los hijos de la fila y quédate
con el más alto (`getBoundingClientRect().height`). Ahí sale el culpable en un
vistazo, y te ahorra el commit inútil de "bajar el padding" que no mueve nada.

**Redescubierto de cero el 8-ago** en la rejilla de presupuestos de obra (50 → 34
px) sin que esta nota apareciera: solo la enlazaban `frontend-css-mobile` y un
histórico. Un learning al que no apunta el hub del proyecto donde nació no se
recupera navegando, solo por búsqueda difusa — y nadie busca en difuso un problema
cuyo nombre no conoce. Enlázalo desde el hub el mismo día que lo escribas.
Corolario del ANCHO: [[columna-que-aloja-un-control-necesita-un-ancho-por-tipo-de-puntero]].
