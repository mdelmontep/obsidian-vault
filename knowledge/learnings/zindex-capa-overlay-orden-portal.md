---
title: z-index de overlays — una capa + orden de portal, tokenizar value-preserving
date: 2026-06-18
source: claude-code-session
tags: [frontend, css, z-index]
---

Los overlays portados a `<body>` (modal base, popovers Select/DatePicker, toast, menús) suelen convivir en UNA capa (p.ej. `z-index: 1000`) y el **orden de inserción en el DOM** decide quién queda encima (el último montado gana). Por eso un Select abierto dentro de un modal sale por encima del modal sin necesitar un z mayor.

Implicaciones al tokenizar una escala z-index:
- Que **refleje el stacking real medido**, NO un ideal "limpio". Un ideal inventado rompe: subir el modal por encima del popover ocultaría el Select abierto dentro de él.
- Tokenizar **value-preserving** (cada token = el valor mágico que sustituye) = cero cambio de comportamiento.
- Capa "siempre encima" (confirm dialog, tooltip, modal-sobre-modal) = token aparte (p.ej. `--z-top: 10000`).
- NO tokenizar z-index **locales** (apilado interno de un componente, badges, `::before`, dropdowns inline) — no son capas globales.

Relacionado: [[no-forzar-base-en-paneles-divergentes]]
