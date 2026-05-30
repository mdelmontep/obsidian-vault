---
title: css background:white hardcoded rompe dark mode silencioso
date: 2026-05-30
source: claude-code-session
tags: [css, dark-mode, theming, gotcha]
---

`background: white` (o `#fff`) en CSS de cards, inputs, modales rompe dark mode sin error visible — las superficies aparecen blancas sobre fondo oscuro. Detectable solo visualmente, lint y typecheck no avisan.

**Fix**: sustituir por `var(--bg-elev)` (white en light, color elevación en dark — convención común: `--bg` fondo página, `--bg-elev` superficie card, `--bg-elev2` superficie elevada).

**Bonus toast invisible**: `background: var(--fg); color: white` da contraste correcto en light pero blanco-sobre-blanco invisible en dark. Fix: `color: var(--bg)` — el inverso del fg garantiza contraste en ambos temas automáticamente.

**Auditoría rápida**: `grep -rE "background:\s*(white|#fff|#ffffff)" src/` lista candidatos. Casi todos son falsos positivos solo si vienen de gradientes oscuros decorativos (ej. tarjeta visual de pago, que SÍ debe ser oscura siempre).

Caso real TuFacturaIA PR #113: 6 reglas `.pb-*` con background:white → captura del user reveló cards "Método de pago" + "Historial" blancas en dark.
