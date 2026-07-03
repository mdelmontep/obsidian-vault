---
title: agent-browser — click en opción de Select custom (ARIA combobox) no selecciona; usar teclado
date: 2026-07-03
source: claude-code-session
tags: [agent-browser, e2e, react, select]
---
Componente `Select` custom con patrón ARIA combobox (trigger `role="combobox"` +
`listbox` portado a body vía Floating UI, ver [[playwright-custom-components-e2e-selectors]]).
En **agent-browser** (CDP), `click @ref` sobre un `option` del listbox NO actualiza
el valor del combobox (se queda mostrando la opción anterior) — el componente espera
navegación por teclado (type-ahead), no un click sintético sobre la opción.
Fix: abrir el combobox (`click` en el trigger) → `keyboard type "<texto búsqueda>"`
para filtrar a 1 opción → `press Enter`. Confirmar con `snapshot -i` que el combobox
muestra el nuevo valor antes de continuar (no asumir que el click bastó).
En Playwright sí funciona el click directo sobre `[role="option"]" (comportamiento distinto entre herramientas).
