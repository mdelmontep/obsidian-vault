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

**El scorecard agregado no sirve para VERIFICAR la corrida** (2026-07-30): guarda `passed/failed` y
nada más, así que un caso que nace rojo **a propósito** (eje de cobertura con suelo `minRate: 0`) y
una caída del gateway se ven **idénticos**. Antes de publicar un `0/N` como medición, correr el
fichero aparte con `--reporter=verbose` y comprobar que los fallos son de **aserción** (con el
`got {…}` del modelo), no de red. Si no, publicarías «el proveedor estaba caído» como línea base.

Relacionado: [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]]

**n=10 NO basta para comparar dos variantes, y el agregado es estructuralmente ciego a un caso**
(4-ago, AGH). Medí un caso sospechoso con n=10: `10/10 vs 8/10`, Fisher p≈0,47 — se lee como ruido.
Con n=25: `24/25 vs 12/25`. La caída era **real (96 % → 48 %)** y n=10 la habría dejado mergear.
Y el `evals:check` completo imprimió **`✓ sin regresiones` con esa caída dentro**: un caso son 3
muestras de 651 = **1,4 puntos** contra una tolerancia de **10**, así que ninguna tasa por eje puede
moverse — no es afinar el umbral, corras ×3 o ×30 sigue siendo ciego. **Lee los CASOS, no la tasa.**
Peor aún, el agregado puede tapar dos cambios que se cruzan: un eje marcó 81,8 % antes y después
mientras un caso se ponía verde y otro rojo. Arreglado en ese repo imprimiendo el **diff caso a caso
contra la corrida anterior** (coste 0 $: los datos ya estaban en el artefacto).
