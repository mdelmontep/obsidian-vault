---
title: color-mix() para sombras y tints sin hardcodear rgba por tema
date: 2026-05-18
source: claude-code-session
tags: [css, theming, dark-mode]
---

En vez de `box-shadow: 0 1px 2px rgba(61,123,245,.25)` (hardcoded brand) usar `box-shadow: 0 1px 2px color-mix(in srgb, var(--brand) 25%, transparent)`. La sombra recoge automáticamente el brand del tema activo, sin declarar `--brand-rgb` aparte.

Baseline 2023: Chrome 111, Safari 16.2, Firefox 113. Sustituye el patrón antiguo:
- `rgba(var(--brand-rgb), .25)` (requería dos tokens, uno rgb y otro hex)
- Variables tipo `--brand-soft-{8,12,18}` (hardcoded por nivel)

Combina con tints de hover: `background: color-mix(in srgb, var(--brand) 5%, var(--bg-elev))`. Funciona con cualquier token CSS, no solo brand.

Ver [[scroll-shadows-komarov-con-css-variable-dark-mode]]
