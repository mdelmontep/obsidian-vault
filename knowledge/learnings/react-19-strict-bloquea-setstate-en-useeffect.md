---
title: react 19 strict bloquea setstate en useeffect, usar derived state pattern
date: 2026-05-06
source: claude-code-session
tags: [react, nextjs, gotcha]
---

React 19 + Next 16 strict marca `react-hooks/set-state-in-effect` cuando hay `setState` directo dentro de `useEffect`. NO silenciar con `eslint-disable` — el lint acertado.

`useEffectEvent` también marca el mismo error si el callback hace `setState`.

Patrón válido (state mirror durante render comparando dependencias):
```tsx
const [seen, setSeen] = useState<T>(undefined)
if (cond && val !== seen) {
  setSeen(val)
  setX(val)
}
```

No es cascada — es derived state documentado en React docs. El render con setState durante render es OK desde React 18+: React lo agrupa.

**Corolario `react-hooks/refs`** (regla del React Compiler): el valor previo de la comparación NO puede ir en `useRef` — leer/escribir `.current` en render está prohibido. Usa `useState` para el previo (como arriba). Para RE-disparar una animación CSS en cada cambio, incrementa un `key` con ese patrón y ponlo en el nodo a re-montar (el resto del subárbol que NO debe re-montarse —p.ej. un `<input>` con foco— va FUERA de ese nodo).

Casos reales facturaia: `AIAssistant` prefill, `ModuloConfig` (commit 02bdf36); shake de `otp-boxes.tsx` re-disparado por `key` con previo en state (PR #254, 2026-06-15).
