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

Casos reales facturaia (commit 02bdf36): `AIAssistant` prefill, `ModuloConfig` carga al cambiar dependency.
