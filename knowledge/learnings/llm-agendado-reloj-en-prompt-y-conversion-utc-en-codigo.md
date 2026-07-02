---
title: agendar por LLM — reloj en el prompt, hora local del modelo, conversión UTC en código
date: 2026-07-02
source: claude-code-session
tags: [llm, scheduling, timezone, hitl]
---

Para que un LLM programe recordatorios/citas ("recuérdame el jueves", "en 30 min"):

1. **Inyecta "ahora" en el prompt** (`message.timestamp`) o el modelo NO puede resolver relativos
   ("el jueves" → qué fecha). Fallo silencioso fácil: sin el reloj, alucina la fecha.
2. **El LLM emite hora LOCAL estructurada** (`{localDate, localTime?}` o `{inMinutes}`), NUNCA el
   instante UTC: el modelo es malo con offset/DST. La conversión wall-clock→UTC es código
   determinista y testeable (doble pasada por DST). Ver [[graph-calendarview-ventana-utc-no-prefer-timezone]].
3. **Resuelve el instante ANTES del HITL** (en `prepare`, e inyéctalo en los fields) para que lo que
   el usuario confirma == lo que se ejecuta; valida futuro/parseable → si no, pregunta (no programes
   un fire pasado/NaN, el scheduler lo dispara al instante).
4. El **canal de entrega** lo decide el adaptador (dato de dominio), no el LLM (el user no lo dice).

Caso AGH #11 (cabo write): `reminder.schedule` como WriteExecutor sobre `resolveReminderInstant`.
