---
title: playwright getByText().first() puede resolver en elemento oculto dentro de <details> cerrado
date: 2026-06-10
source: claude-code-session
tags: [playwright, testing, e2e, selectores]
---

## Síntoma

`page.getByText(texto, { exact: true }).first()` en una lista de previsiones
resuelve al `.bullet-concepto` dentro de un `<details>` cerrado (no visible),
en vez de la `.forecast-row` visible → el test falla porque el elemento
encontrado está oculto en el DOM pero Playwright lo considera matchable.

## Por qué

`getByText` busca en TODO el árbol DOM, incluyendo elementos no visibles.
`.first()` devuelve el primero en orden DOM, que puede ser el interior
de un `<details>` cerrado (renderizado pero invisible). El `<details>` puede
aparecer antes en el DOM que la lista paginada de filas visibles.

## Fix / patrón

Scopear el locator al contenedor visible antes de llamar `getByText`:

```typescript
// MAL: busca en todo el DOM
await page.getByText(concepto, { exact: true }).first()

// BIEN: acota al contenedor de la lista visible
await page.locator('.forecast-list').getByText(concepto, { exact: true })
```

Aplica siempre que haya `<details>`/`<summary>` o elementos con
`display:none`/`visibility:hidden` que contengan el mismo texto que el
elemento target. Regla: en tests de listas, scopear siempre al contenedor.
