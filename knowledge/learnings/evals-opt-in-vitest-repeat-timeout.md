---
title: correr evals opt-in con modelo real — vitest --repeat no es flag CLI y el timeout 5s da falsos timeouts
date: 2026-07-13
source: claude-code-session
tags: [testing, vitest, evals, llm]
---
- `vitest run --repeat=N` NO existe como flag CLI (vitest 2.x) → "Unknown option". Para
  repetir N veces: bucle bash (`for i in 1 2 3; do vitest run ...; done`), el runner propio
  del repo (`--repeat=N`) o `test.repeats` en config.
- Tests que llaman a un gateway LLM real (`*.opt.test.ts`) con el testTimeout default (5s)
  dan FALSOS timeouts cuando el gateway tarda → `--testTimeout=25000` o usar el runner.
- El full de evals ×1 amplifica la varianza del baseline (calibrado agregando ×3): ejes
  ruidosos (entity/recall) dan falsos rojos. El ×3 es el comparable al baseline.
