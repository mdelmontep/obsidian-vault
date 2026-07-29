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

**Lo que sí funciona (2026-07-29):** `fill @ref "<texto>"` dispara la búsqueda y pinta las opciones;
entonces `click "#<id-real-de-la-opción>"` (id del DOM, no `@ref`) sí selecciona. Dos trampas:
(1) las opciones solo existen mientras el input tiene foco, y cada llamada intermedia lo quita —
`fill` y el `eval` que las lista van en la MISMA invocación o parecerá que nunca se pintaron;
(2) `type`/`keyboard type` sobre un `@ref` puede no enfocar y las pulsaciones caen en el `Segmented`
de la página, que cambia el tipo de documento y navega solo. Si acabas en una URL que no pediste,
es esto.

**Síntoma que engaña (2026-07-29):** el click sintético deja el combobox con el texto tecleado y
la app sin cliente seleccionado, así que lo que se ve es "elegí un cliente con 60 días pactados y
el vencimiento sigue en 30" — idéntico a un bug de producción recién desplegado. Antes de reportar,
comprobar que el valor del combobox es el de la opción, no el que escribiste: si no lo es, no hubo
selección y no hay bug que reportar.
