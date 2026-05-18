---
title: mobile — restore-focus tras inert en requestAnimationFrame
date: 2026-05-18
source: facturaia FASE 2 mobile polish
tags: [frontend, a11y, react, ios, safari, inert, focus]
---

Al cerrar un drawer modal con `inert={open}` en `<main>`, devolver foco al trigger en el mismo tick **no funciona en WebKit**:

```jsx
// NO funciona — el target sigue inert cuando se llama focus()
setOpen(false)
trigger.focus()
```

WebKit descarta silenciosamente `.focus()` sobre un elemento aún `inert`. React no ha re-renderizado todavía y el atributo no se ha quitado.

**Patrón correcto** — `useRef` previo + `useEffect` con `requestAnimationFrame`:

```jsx
const wasOpenRef = useRef(false)
useEffect(() => {
  if (wasOpenRef.current && !open) {
    requestAnimationFrame(() => trigger?.focus())
  }
  wasOpenRef.current = open
}, [open])
```

El `rAF` espera al próximo frame, momento en que React ya retiró `inert` del DOM.

Ver [[mobile-inert-plus-aria-hidden-ios-15-fallback]].
