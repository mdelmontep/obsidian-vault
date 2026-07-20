---
title: botón de design-system con overflow:hidden — borde/halo animado va en pseudos del botón, no en un hijo
date: 2026-07-20
source: claude-code-session
tags: [css, design-system, frontend, qa]
---
Un `<Button>` de design-system suele (a) envolver los children en spans posicionados (`.stack`/`.layer`, `position:relative`) y (b) llevar `overflow:hidden` (para su sheen/keycap).

Si metes un `<span class="glow">` como CHILD para el halo/borde animado:
- se ancla al CONTENIDO (offsetParent = `.stack`), no al botón → el halo rodea texto+icono POR DENTRO;
- `overflow:hidden` recorta cualquier cosa fuera del botón → no hay halo exterior posible desde un hijo.

Fix: borde/línea + halo van en los PSEUDO-elementos del botón (`::before`/`::after`, anclan al botón) + `button.ai-btn{overflow:visible}` (especificidad de tipo para ganar al CSS-module, que carga después y pisa). Halo exterior sin sangrado = pseudo a `inset:-N` con máscara de hueco redondeado aplicada TRAS el `blur`; se desvanece hacia fuera con un `radial-gradient` en la capa exterior de la máscara.

Solo hay 2 pseudos: si necesitas borde+línea+halo, funde el borde estático en un `box-shadow inset` (rim) y libera el pseudo.

Caso real (botón «Ask» FacturaIA, #1077/#1080/#1083/#1085): 3 PRs fallidos por QA-ear en un HTML-harness que NO replicaba el wrapper `<Button>` (todo se veía bien) → verificar SIEMPRE en la app real (login E2E), no en harness aislado. Ver [[worktree-qa-next-standalone-symlink-node-modules]] · [[css-border-beam-conic-property-playbackrate]].
