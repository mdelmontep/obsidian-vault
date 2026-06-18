---
title: ADR-033 — Posicionamiento de popovers anclados con @floating-ui/react
date: 2026-06-18
status: accepted
tags: [adr, facturaia, frontend]
---

## Contexto
~10 componentes (menús de fila, sidebar, select, date-picker) repetían un patrón casero
(`createPortal` + `getBoundingClientRect` + cálculo manual de top/left/right + flip por altura
estimada). Fallaba: flip prematuro/descolgado y menús saliéndose por el borde derecho.

## Opciones consideradas
- **A — @floating-ui/react** — ~3 kB, flip/shift/size reales, 100% navegadores hoy; +1 dependencia.
- **B — CSS Anchor Positioning** — nativo, sin JS; pero Baseline 2026 = solo ~80,7% soporte global → rompería ~1/5 usuarios sin fallback (= mantener dos caminos).
- **C — seguir con el patrón casero** — cero deps; perpetúa la deuda y el bug en 10 sitios.

## Decisión
**A**, encapsulado en el hook `useAnchoredMenu`. CSS Anchor Positioning se revisará cuando
sea "widely available" (no "newly available").

## Consecuencias
Floating UI es la primitiva única para popovers anclados; nuevos menús/dropdowns la usan, no
cálculo manual. Charts/modales/drawers quedan fuera (no son popovers anclados a trigger).
