---
name: float-exp-underflow-asintota-tests
description: Math.exp(-N) vale 0 exacto en IEEE 754 cuando N ≥ ~38 — la asíntota llega al tope exacto y rompe expect(v).toBeLessThan(cap)
metadata:
  type: feedback
---

## El bug

`estimateProgresoOcr` usa `OCR_EXPECTED_MS = 5_000` (τ pequeño, curva ágil). Un test verificaba `expect(v).toBeLessThan(60)` para t=300_000ms. Con N = 300_000/5_000 = 60, `Math.exp(-60) = 0` exacto en IEEE 754 → `1 - 0 = 1` exacto → la curva llega al tope exacto (60) → `toBeLessThan(60)` falla.

## Fix

Clamp explícito que preserve la invariante:

```ts
const raw = INICIO + (CAP - INICIO) * (1 - Math.exp(-Math.max(0, elapsedMs) / TAU))
return Math.min(raw, CAP - 0.001)
```

## Regla

Toda curva asintótica `1 - Math.exp(-t/τ)` tiene underflow a 0 exacto cuando `t/τ ≥ ~38`. Si el dominio de t es abierto (tiempo real), añadir `Math.min(raw, cap - epsilon)` antes de devolver. Documentar que la asíntota no es matemáticamente alcanzable pero IEEE 754 lo hace posible.
