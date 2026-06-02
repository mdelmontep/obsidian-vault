---
title: usar {{current_time_[tz]}} y {{current_calendar_[tz]}} de Retell en vez de hardcodear la fecha
date: 2026-06-02
source: claude-code-session
tags: [retell, voz, fecha]
---

Retell inyecta variables de sistema **por llamada** (no estáticas): `{{current_time_Europe/Madrid}}` ("Tuesday, June 2, 2026 at 2:30 PM CEST") y `{{current_calendar_Europe/Madrid}}` (lista de 14 días con la línea "(Today)" marcada). Funcionan en global_prompt de conversation-flow.

Patrón: NUNCA hardcodear "HOY es viernes 29 de mayo" en el prompt (queda stale en días) ni montar un cron que parchee la fecha. Poner `{{current_time_Europe/Madrid}}` + el calendario de 14 días → el LLM mapea "el miércoles"/"mañana"/"la semana que viene" a la fecha real y ve los fines de semana. El output es en inglés pero el LLM en español lo parsea sin problema.

Caso EcoBox 2026-06-02 (sustituye el TODO del cron diario). Docs: https://docs.retellai.com/build/dynamic-variables. Relacionado: [[llm-current-date-debe-inyectarse-explicito-evita-alucinar-anyo]].
