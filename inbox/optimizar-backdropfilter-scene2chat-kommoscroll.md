---
title: optimizar backdropFilter en Scene2Chat si el jank persiste
date: 2026-04-15
source: claude-code-session
tags: [pendiente, agentesia-web, performance]
---

Contexto: el 15-04-2026 optimicé KommoScrollSection (página `/solucion`) contra jank de scroll aplicando el skill `fixing-motion-performance` — throttle del scroll handler con refs, quitar `willChange: opacity` de 6 layers full-viewport, añadir `contain: layout paint size`, y neighbor-only rendering (`|active - i| <= 1` → máximo 3 escenas vivas en vez de 6).

Si después de esos fixes la página sigue yendo a tirones en móvil, el siguiente sospechoso son dos elementos con glassmorphism en `src/components/sections/kommo/scenes/Scene2Chat.tsx`:

- línea 391: `backdropFilter: "blur(18px)"`
- línea 502: `backdropFilter: "blur(16px)"`

Rule 7 del skill motion-performance: "never animate blur on large surfaces". Aunque aquí son estáticos, durante scroll el contenido detrás cambia por transforms de otros elementos, forzando repintados continuos del glass effect en el compositor.

Fix propuesto: reemplazar por `background: rgba(...)` sólido sin blur. Cambio visual pequeño pero visible en el mock de iPhone de la Scene 2 → pedir luz verde al usuario antes de aplicar.

**Update 2026-04-15**: Scene2 se ha dividido en dos escenas separadas para mobile (`Scene2Chat.tsx` + `Scene2bCall.tsx`). El iPhone con glass effect ahora vive en una de las dos — los números de línea del aviso original ya no aplican. Si el jank reaparece, buscar `backdropFilter` en ambos archivos antes de tocar nada.
