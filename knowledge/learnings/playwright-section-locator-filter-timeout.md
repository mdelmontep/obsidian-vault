---
title: playwright filter({ has: locator }) + waitFor puede timeout en páginas complejas
date: 2026-06-09
source: claude-code-session
tags: [playwright, testing, visual-regression]
---

## Qué pasa

`page.locator('section').filter({ has: page.getByRole('heading', { name: 'X' }) })` seguido de `.waitFor({ state: 'visible' })` puede timeout (15s) aunque el elemento exista visualmente. Ocurre cuando la página tiene muchos elementos dinámicos, transiciones CSS activas, o hay discrepancia entre el árbol de accesibilidad y el DOM durante la hidratación.

## Por qué

`filter({ has })` evalúa el selector repetidamente hasta encontrar el elemento o timeout. Si las transiciones CSS o el estado de fuentes (`document.fonts.ready`) bloquean la evaluación del aria-tree, el locator puede no resolver aunque el elemento esté visible.

## Fix / patrón

Para regresión visual de páginas enteras, usar `fullPage: true` directamente en `toHaveScreenshot` en lugar de locators por sección. Los tests full-page son más estables y suficientes para detectar regresiones:

```typescript
await expect(page).toHaveScreenshot(`page-${theme}.png`, {
  maxDiffPixelRatio: 0.01,
  animations: 'disabled',
  fullPage: true,
})
```

Si se necesitan secciones específicas, usar `locator.screenshot()` con un selector CSS directo (no `filter({ has })`), y solo después de `waitForLoadState('networkidle')` + `document.fonts.ready`.
