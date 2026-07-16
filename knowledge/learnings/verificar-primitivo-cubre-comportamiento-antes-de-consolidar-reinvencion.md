---
title: una "reinvención" puede ser un diseño distinto a propósito — verifica que el primitivo cubre el comportamiento antes de consolidar
date: 2026-07-16
source: claude-code-session
tags: [frontend, refactor, design-system, ui]
---
Al planear "migrar reinvención X → primitivo Y" para unificar, NO asumas que X
es una copia naíf de Y. Lee X entero y compara COMPORTAMIENTO, no solo nombre/
apariencia. Casos reales (FacturaIA Fase 4 unificación UI):
- `feedback-modal` era un panel flotante ARRASTRABLE no-bloqueante (aria-modal=false, sin backdrop), no un modal.
- `notifications-drawer` era flotante-redondeado con Escape que cierra el submenú primero; `ingesta/details-panel` coordinaba Escape con un modal hijo (`blockEscape`).
- `.card-grid` era un grid de LAYOUT y `.card-detail` un bloque key-value — ninguno un "card".
Forzarlos al primitivo = regresión de UX o pérdida de comportamiento. Si el
primitivo NO cubre (nav teclado, coordinación de Escape, variante visual): o lo
extiendes a superset primero (como se hizo con `Segmented`), o lo dejas bespoke
y lo documentas. El coste de leer < el coste de romper un feature de alto tráfico.
Ver [[migrar-submodal-a-modal-choca-con-escape-del-contenedor]] · [[migracion-invisible-de-primitivo-alinear-geometria-al-legacy]].
