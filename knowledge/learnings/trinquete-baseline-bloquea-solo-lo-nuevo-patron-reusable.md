---
title: trinquete de baseline (bloquea solo lo NUEVO) — patrón reusable para deuda que no se puede cerrar de golpe
date: 2026-07-22
source: claude-code-session
tags: [ci, gates, deuda-tecnica, facturaia]
---
Patrón ya usado 3 veces en TuFacturaIA (inline-styles, design-debt, y ahora
vulnerabilidades npm): cuando una categoría de deuda tiene hallazgos
preexistentes que NO se pueden (o no toca) arreglar todos de golpe —algunos
bloqueados upstream, otros necesitan QA aparte—, un gate que bloquea sobre
CUALQUIER hallazgo deja el repo permanentemente rojo. La solución es un
trinquete: baseline commiteado (JSON) de lo ya aceptado + motivo, el checker
solo falla si aparece algo NUEVO fuera del baseline.

Estructura común (ver `scripts/inline-style-ratchet.mjs` y
`scripts/audit-ratchet.mjs`):
- `--write` regenera el baseline desde el estado actual (con `PENDIENTE:` a
  rellenar a mano si el motivo no estaba ya documentado).
- El check normal compara contra el baseline; permite que baje (arreglado
  sin tocar el baseline) pero bloquea que suba o aparezca algo nuevo.
- Wireado en pre-commit, condicionado al tipo de archivo que dispara la
  categoría (staged `.css`/`.tsx` para inline-style, `package-lock.json`
  para audit).

Antes de confiar en un checker nuevo: probarlo con un caso que DEBERÍA
fallar (quitar una entrada del baseline a mano, confirmar exit 1) — no basta
con que corra sin errores. Regla homóloga a la disciplina de loops/checkers
en general (ver memoria del agente `feedback_loop_engineering_disciplina`).
