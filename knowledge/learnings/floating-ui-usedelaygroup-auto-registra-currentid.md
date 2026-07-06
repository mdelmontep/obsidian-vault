---
title: floating-ui useDelayGroup registra currentId solo si le pasas el context de useFloating
date: 2026-07-06
source: claude-code-session
tags: [frontend, react, floating-ui, tooltip]
---

`useDelayGroup(context)` de `@floating-ui/react` (para que un grupo de
tooltips en un toolbar abra el primero con delay y los siguientes al
instante) YA registra `setCurrentId(id)` internamente en un efecto propio
cuando `context.open` pasa a `true` — no hace falta un `useEffect` manual
llamando a `setCurrentId`. Basta con pasarle el `context` que devuelve
`useFloating()` de ESE tooltip; el id por defecto es `context.floatingId`.

Gotcha: sin un `<FloatingDelayGroup>` proveedor por encima, `useDelayGroup`
devuelve `delay: 0` (contexto por defecto), no un delay razonable — un
Tooltip suelto fuera de grupo abriría instantáneo al primer hover si no se
aplica un fallback propio (`delay || DEFAULT_DELAY`).

Caso: TuFacturaIA `src/components/ui/tooltip.tsx` (componente Tooltip nuevo).
Ver [[react-hooks-refs-falso-positivo-floating-ui]] (mismo paquete, otro gotcha).
