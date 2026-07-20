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

Corolario toast (PR #1107, 2026-07-21): un toast/notificación **inline** (no portado, p.ej. contenedor de `ToastProvider`) a `--z-overlay` queda TAPADO por cualquier modal portado (empata y el modal se monta después en `<body>` → gana). Subirlo a `--z-top` TAMPOCO basta: hay modales que viven en `--z-top` (ajuste-stock, factura emitida, confirm) y disparan toasts → vuelven a empatar y taparlo. El toast necesita capa propia por ENCIMA de todo: `--z-toast: 10001`. Justificación: es transitorio y no bloquea interacción, debe verse siempre. Prueba: `elementFromPoint` sobre la zona del toast con un modal `--z-top` montado después.
Relacionado: [[overlay-padre-onclick-close-sin-guarda-cierra-con-popover-portado]] · [[modal-portal-stacking-sticky-sidebar]] · [[no-forzar-base-en-paneles-divergentes]]
