---
title: tour spotlight in-modal con tourBlocker + z-index elevation
date: 2026-06-30
source: claude-code-session
tags: [frontend, ux, onboarding, facturaia]
---

Tutorial guiado dentro de un modal sin librerías externas:

**Estructura de capas (panel position:relative):**
- `tourBlocker` — `position:absolute; inset:0; z-index:5; background:rgba(8,12,28,0.62)` → oscurece todo
- Sección activa → clase `tourHighlight`: `position:relative; z-index:10; outline:2px solid var(--brand)`
- `tourTooltip` — `position:absolute; z-index:20` + `style={TOUR_TOOLTIP_POS[step]}`

**Posicionamiento del tooltip por step:**
```ts
const TOUR_TOOLTIP_POS: Record<number, CSSProperties> = {
  0: { top:'50%', left:'50%', transform:'translate(-50%,-50%)' }, // intro centrado
  1: { top:'100px', right:'24px' },   // izq activo → tooltip a la derecha
  2: { top:'100px', left:'24px' },    // der activo → tooltip a la izquierda
  3: { bottom:'76px', left:'50%', transform:'translateX(-50%)' },
}
```

**Gate localStorage:**
```ts
const TOUR_KEY = 'fia:conciliar-tour-v1'
useEffect(() => { if (!localStorage.getItem(TOUR_KEY)) setTourStep(0) }, [])
const skipTour = () => { localStorage.setItem(TOUR_KEY,'1'); setTourStep(-1) }
```

**ESC:** cierra tour primero, luego modal (handler único con priority check).  
**Step 0:** sin blocker (panel completo visible), solo tooltip centrado.  
**Steps 1+:** blocker activo + sección elevada.
