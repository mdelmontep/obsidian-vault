---
title: theming scoped a un componente via --comp-* CSS vars con fallback a token global
date: 2026-06-09
source: claude-code-session
tags: [css, theming, design-system, facturaia]
---

## Patrón

Para theming scoped (que afecte SOLO a un componente, no al global), añadir variables `--comp-*` con fallback al token canónico en el módulo CSS del componente. Los overrides `[data-theme-attr]` solo redefinen las vars `--comp-*`, dejando el token global intacto.

```css
/* estado-pill.module.css */
.brand {
  background: var(--pill-brand-soft, var(--brand-soft));
  color: var(--pill-brand-fg, var(--brand-fg));
}
```

```css
/* globals.css */
[data-pill-theme="pastel"] {
  --pill-brand-soft: oklch(93% 0.04 253);
  --pill-brand-fg: oklch(44% 0.10 253);
  /* ... */
}
```

El atributo `data-pill-theme` se pone en `document.documentElement`, persistido en localStorage.

## Por qué funciona

CSS custom properties con fallback: si `--pill-brand-soft` no existe, usa `--brand-soft`. Los overrides solo existen en el scope `[data-pill-theme]`, nunca contaminan el UI global (botones, nav, inputs).

## Cuándo usar

- El componente tiene muchas variantes de color que el usuario puede personalizar
- No quieres tocar los design tokens globales
- Necesitas que el preview en la UI de settings muestre cada tema localmente (el preview puede tener `data-pill-theme` en su propio div sin afectar el resto)

## Cuándo NO usar

- Si el token global también necesita cambiar → cambiar el token directamente
- Si son <3 variantes → usar clases CSS directamente
