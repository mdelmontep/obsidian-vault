---
title: eslint react-hooks/static-components bloquea selección dinámica de componente en JSX
date: 2026-07-17
source: claude-code-session
tags: [react, eslint, frontend]
---
`const Cmp = MAP[key]; return <Cmp />` dentro de render dispara `react-hooks/static-components` ("component created during render") si `Cmp` sale de un lookup por variable, aunque el mapa sea estático a nivel de módulo.

Fix: envolver el lookup en un ÚNICO componente estable con el lookup dentro, y consumir siempre ese componente (nunca extraer el resultado del lookup a una variable tipo componente en el sitio de uso):

```tsx
function BrandIcon({ slug, size }: { slug: string; size?: number }) {
  const Cmp = BRAND_ICON[slug]
  if (!Cmp) return null
  return <Cmp size={size} />
}
```

Caso real: `src/lib/integrations/providers/brand-icons.tsx` (TuFacturaIA, PR #973).
