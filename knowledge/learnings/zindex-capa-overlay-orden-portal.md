---
title: popover portado debe superar el overlay del modal que lo contiene (no basta "una capa")
date: 2026-06-26
source: claude-code-session
tags: [frontend, css, z-index]
---

Popovers portados a `<body>` (Select/DatePicker via Floating UI) y overlays de modal conviven en UNA capa y el orden DOM decide quién gana **SOLO si comparten z-index**. Si el modal/drawer usa un z MAYOR (drawer 1100, modal 1200, overlay custom 1300), el popover a `--z-overlay`(1000) queda OCULTO bajo el overlay y no clicable.

Corrige el supuesto "tokenizar value-preserving" de la versión previa de esta nota: mantener el popover a 1000 cuando hay overlays a 1300 **perpetúa el bug**.

Fix: token propio `--z-popover` por encima de cualquier modal/drawer y bajo `--z-top` (confirm/tooltip). En TuFacturaIA `--z-popover: 1400` (PR #520). Síntoma: dropdown dentro de modal invisible, o que cierra el modal al clicar (esto último es OTRA causa → ver relacionado).

Capa "siempre encima" (confirm/tooltip/modal-sobre-modal) = `--z-top: 10000`. NO tokenizar z-index locales (badges, `::before`, dropdowns inline).
Relacionado: [[overlay-padre-onclick-close-sin-guarda-cierra-con-popover-portado]] · [[modal-portal-stacking-sticky-sidebar]] · [[no-forzar-base-en-paneles-divergentes]]
