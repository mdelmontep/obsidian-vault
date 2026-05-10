---
title: useEffectEvent react19 no se llama desde setTimeout
date: 2026-05-10
source: claude-code-session
tags: [react, react19, hooks, lint]
---

`useEffectEvent` solo es invocable directamente desde Effects/Effect Events del mismo componente. Llamarlo desde `setTimeout`/`Promise.then`/event handler externo dispara `react-hooks/rules-of-hooks` error.

Patrón roto típico (debounce de fetch reactivo a filtros):
```ts
const load = useEffectEvent(async () => { ... })
useEffect(() => {
  const t = setTimeout(() => load(), 250)  // ← lint error
  return () => clearTimeout(t)
}, [filtros])
```

**Fix**: usar `useCallback` con deps explícitas, no `useEffectEvent`:
```ts
const load = useCallback(async () => { ... }, [search, onlyOverride])
useEffect(() => {
  const t = setTimeout(() => load(), 250)
  return () => clearTimeout(t)
}, [load])
```

`useEffectEvent` se diseñó para "leer state actual sin invalidar deps", no para encapsular callbacks invocables async. Si necesitas debounce + reactivo a filtros, useCallback es la herramienta.
