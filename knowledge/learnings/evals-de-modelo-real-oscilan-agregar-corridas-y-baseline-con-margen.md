---
title: evals de modelo real con pocas muestras oscilan → agregar N corridas + baseline con margen
date: 2026-07-10
source: claude-code-session
tags: [evals, llm, testing, agh]
---
Un banco de casos-oro contra el modelo REAL (temp 0 incluido) NO es determinista: un fichero
de 3 casos puede dar 100% en una corrida y 33% en la siguiente por jitter del proveedor. Un
gate de "una corrida vs umbral fijo" da falsos positivos constantes.

Fix (infra de medición AGH, `scripts/eval-score.ts`):
- **Agregar N=3 corridas** por defecto y sumar los tallies → tasa estable (3 ficheros ×3 = 9
  muestras). `mergeScorecards`.
- **Baseline committeado** derivado de una corrida real menos un **margen** (0.1), y el check
  compara con una **tolerancia** extra (0.1) → ~20 pts de colchón: no salta por jitter, sí por
  caída real.
- No es "todo verde": captura la realidad actual; una mejora estable → regenerar baseline
  (queda en git "subió de X% a Y%"). Es el gate para tocar el prompt sin regresiones invisibles.
- Coverage-miss: si un eje que el baseline ESPERA deja de correr (0 casos), es regresión, no
  verde silencioso.

Relacionado: [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]]
