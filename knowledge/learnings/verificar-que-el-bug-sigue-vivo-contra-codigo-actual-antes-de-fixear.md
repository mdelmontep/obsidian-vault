---
title: verificar que un bug sigue vivo contra el código actual antes de fixear
date: 2026-07-14
source: claude-code-session
tags: [auditoria, evals, llm, debugging, proceso]
---
Un hallazgo (traza de auditoría, error-analysis, eval rojo) NO es accionable hasta confirmar que
sigue vivo en el CÓDIGO ACTUAL. Dos trampas reales (sesión AGH, auditoría de comunicación):

1. **Corpus caduco.** Trazas/logs de ANTES de merges recientes → el bug ya está arreglado. Cruzar
   la fecha de la evidencia contra la fecha de merge del área (`gh pr view N --json mergedAt`) + leer
   el path actual. Casi re-fixeo 3 bugs ya resueltos por PRs previas.
2. **Flaky/LLM.** Un eval "rojo" intermitente puede ser oscilación del modelo o **timeout de infra**
   (p. ej. 5003ms del gateway), no un gap estable. Medir N corridas AISLANDO el caso y separar
   timeout de misclasificación: un caso que da 32/32 al medirlo bien no necesita fix — un cambio de
   prompt encima sería placebo con riesgo de regresión.

Regla: **medir reproducibilidad antes de tocar**; un fix de menos no cuesta nada, uno "por si acaso"
mete riesgo y ruido. Relacionado: [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]] · [[structured-outputs-strict-garantiza-forma-no-veracidad]]
