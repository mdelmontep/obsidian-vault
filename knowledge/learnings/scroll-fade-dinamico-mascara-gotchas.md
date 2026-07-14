---
title: scroll-fade dinámico con mask-image — 3 gotchas (transition/@property, box-shadow, portal)
date: 2026-07-14
source: claude-code-session
tags: [css, react, frontend, facturaia, mask, scroll]
---

Fade en el borde de un riel scrollable SOLO donde hay contenido oculto: hook
marca `data-fade-left/right` según `scrollLeft`/`scrollWidth`, y una máscara
CSS difumina 26px en el lado marcado. En FacturaIA = clase `.scroll-fade-x` +
`useScrollFade` (PR #889). Tres trampas que el build NO caza, solo el QA real:

1. **`transition` sobre custom property de `@property` la clava en initial-value.**
   Registré `--sf-l/--sf-r` como `<length>` y les puse `transition` para animar
   el fade → en Chromium el valor se quedaba pinneado en 0px (initial), estático,
   → el fade nunca aparecía. Quitar la `transition` → funciona (snap al cruzar el
   umbral, imperceptible al arrastrar). Si necesitas suave, verifica en el browser
   objetivo antes de fiarte.
2. **`mask-image` recorta el `box-shadow` que sobresale del border-box.** No
   enmascares un elemento cuyo glow/sombra sale fuera (ej. thumb activo de un
   segmented) — lo corta. Pon la máscara en el CONTENEDOR de scroll externo, no
   en el elemento con glow.
3. **`useEffect + useRef` no engancha fiable en portales/montaje condicional**
   (drawer de notificaciones): el listener de scroll no se conectaba. Usar
   **callback ref** (React lo invoca en el commit al montar/desmontar el nodo).

Ver [[scroll-shadows-komarov-con-css-variable-dark-mode]] (técnica alternativa con
sombras de fondo) · [[scroll-snap-no-recomendado-para-filter-chips]].
