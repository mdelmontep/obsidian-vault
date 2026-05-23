---
title: Playwright getByLabel falla sin htmlFor — usar placeholder o filter by option
date: 2026-05-23
source: smoke E2E cashflow v2 contra app.tufacturaia.com
tags: [playwright, e2e, selectores, a11y]
---

## Síntoma

`page.getByLabel('Frecuencia').selectOption('trimestral')` lanza `TimeoutError: locator.selectOption: Timeout 15000ms exceeded` aunque el `<label>Frecuencia</label>` está visible en el DOM.

## Causa

El componente usa labels visuales sin asociación ARIA explícita:

```tsx
<div>
  <label>Frecuencia</label>
  <select value={...}>...</select>
</div>
```

Sin `htmlFor` + `id` (o anidación `<label><input/></label>`), el algoritmo accessible-name de Playwright no enlaza label↔control. `getByLabel` retorna locator vacío.

## Solución (preferida)

1. **Por placeholder cuando es único en la página**:
   ```ts
   await page.getByPlaceholder('Ej: IBI 2026').fill(concepto)
   ```

2. **Por filtro de contenido cuando es un select**: identificar el control por una de sus opciones únicas:
   ```ts
   const sel = page.locator('select').filter({
     has: page.locator('option', { hasText: 'Trimestral' })
   })
   await sel.selectOption('trimestral')
   ```

3. **Por atributo de tipo cuando es único**:
   ```ts
   await page.locator('input[type="date"]').fill('2026-07-01')
   await page.locator('input[type="number"][step="0.01"]').fill('123.45')
   ```

## Cuándo NO usar el ancestor-of-label (anti-patrón)

```ts
// Anti-patrón: matchea TODOS los ancestros que contienen el label
// (tabpanel, edit-row-2col, dialog, body...) y `.first()` puede caer en cualquiera.
page.locator('div', { has: page.locator('label', { hasText: 'Frecuencia' }) })
  .locator('select').first()
```

Funciona a veces, falla cuando hay otro `<select>` (p.ej. "Categoría") en un div ancestro compartido. La heurística de Playwright `.first()` no garantiza qué se queda.

## Solución a futuro (fix raíz)

Reescribir el componente con `htmlFor` + `id`:

```tsx
<div>
  <label htmlFor="freq">Frecuencia</label>
  <select id="freq">...</select>
</div>
```

Esto cumple WCAG 1.3.1 y desbloquea `getByLabel` en Playwright + screen readers. Considerar PR en `src/components/ui/add-forecast-modal.tsx` y similares.
