---
title: react-hooks/set-state-in-effect solo flagea llamar a una función nombrada, no un .then() inline
date: 2026-07-07
source: claude-code-session
tags: [react, nextjs, eslint, gotcha]
---
Complementa [[react-19-strict-bloquea-setstate-en-useeffect]] (esa cubre derived state durante render). Esta es sobre fetch-on-mount clásico.

```tsx
// ❌ dispara react-hooks/set-state-in-effect
async function load() { const d = await fetch(...); setData(d) }
useEffect(() => { load() }, [])

// ✅ pasa el lint — mismo efecto, sin función nombrada intermedia
useEffect(() => {
  let cancelled = false
  fetch(url).then(r => r.json()).then(d => { if (!cancelled) setData(d) })
  return () => { cancelled = true }
}, [])
```

El analizador estático solo mira si el CUERPO del efecto llama directo a `setState`/`.then(setState)`; si delega a una función nombrada (aunque esa función haga exactamente lo mismo), no la sigue y no detecta el patrón — false negative, no false positive, así que no lo confundas con "está bien hacerlo con función nombrada". Patrón confirmado ya en uso en `plans/page.tsx` del repo facturaia (con guard `cancelled`). La función nombrada sigue siendo útil para reusar el fetch tras una mutación (crear/borrar) desde un handler — ahí SÍ es correcta, el lint solo mira el cuerpo del `useEffect`.
