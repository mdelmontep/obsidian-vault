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

**Tercera trampa, y la más barata de evitar: el REGISTRO de hallazgos va por detrás del código.**
Un `estado.json` / backlog / issue tracker refleja lo que era verdad cuando alguien lo escribió, y
si entre medias hubo un barrido de arreglos, el registro **miente en la dirección cara** (te manda a
trabajar en lo hecho). FacturaIA 11-ago: los DOS hallazgos abiertos de la sección `cobros` estaban
ya arreglados —el recordatorio de la API v1 usaba `importe_cobrable` y era fail-closed, y el opt-out
de RGPD vivía en la costura compartida de los cuatro emisores—; el primer paso del método
(«verificar antes de darlo por abierto») ahorró la sección entera en la primera a la que se aplicó.

Señal para desconfiar del registro: el hallazgo dice **«auditoría estática (agente); NO medido»**.
Eso no es un hallazgo, es una hipótesis con formato de hallazgo — y algunos ni tenían caso real.
Corolario para quien ESCRIBE el registro: anotar siempre si está medido y contra qué, y **cerrar la
entrada en la misma tanda en que se arregla** (igual que un ticket, [[feedback_ticket_mergeado_pasa_a_resuelto]]).
