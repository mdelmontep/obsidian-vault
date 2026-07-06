---
title: tabla con overflow-x:auto y scrollbar overlay de macOS parece rota, no scrolleable
date: 2026-07-06
source: claude-code-session
tags: [frontend, css, table, overflow, scrollbar, a11y]
---

En una tabla con `overflow-x: auto` sobre un wrapper, si el contenido excede el
contenedor a un ancho intermedio (~1280px, ni mobile ni desktop ancho), la
última columna (pill de estado, importe) se ve cortada a media celda. La
scrollbar overlay de macOS solo aparece al interactuar — no hay ninguna señal
de que hace falta hacer scroll, así que parece un bug de layout, no un
"scrollea para ver más".

**Fix**: forzar scrollbar fina y permanente en el wrapper:
```css
.wrap { scrollbar-width: thin; scrollbar-color: var(--line) transparent; }
.wrap::-webkit-scrollbar { height: 7px; }
.wrap::-webkit-scrollbar-thumb { background: var(--line); border-radius: 999px; }
```
Definir `::-webkit-scrollbar` hace que Chrome/Safari abandonen el estilo
overlay y rendericen una barra clásica con espacio reservado, siempre visible.

**Diagnóstico preciso, no a ojo**: medir `elemento.scrollWidth - elemento.clientWidth`
en vivo (devtools o `agent-browser eval`) para saber CUÁNTOS px sobran antes de
tocar CSS — en este caso 44px, resueltos bajando el `max-width` de la columna
flexible (con ellipsis) en esa cantidad exacta.

También: celdas de importe/moneda necesitan `white-space: nowrap` explícito —
si no, el símbolo de moneda se parte a su propia línea en cuanto la columna
se aprieta, incluso en `table-layout: auto`.

Caso real: TuFacturaIA PR #775, tabla de conciliación bancaria.
