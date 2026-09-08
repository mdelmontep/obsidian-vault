---
title: contar turnos en vez de llamadas infla la significancia de un cambio de prompt
date: 2026-09-08
source: centro-elphis
tags: [retell, medicion, estadistica, agentes-voz]
---
Al medir si un cambio de prompt reduce un defecto (narrar el razonamiento, recitar guion), la unidad
natural parece el turno. No lo es: los turnos de una misma llamada **no son independientes** — 11 de
18 turnos defectuosos salían del mismo caso.

- Contando turnos salía 7/309 → 0/309 («lo hemos eliminado»). Contando corridas, 8,0 % → 1,2 %:
  mejora real y bien medida, pero no es cero.
- Corolario: un brazo con n=3 no distingue nada. 3/3 contra 0/3 parecía una regresión causada por el
  cambio; con n=9 salió 4/9 · 4/9 · 3/9, p=1,0 — era variabilidad del LLM.
- Antes de atribuir una regresión al cambio, comprobar si el brazo de control la tiene también.
- Intercalar los brazos en el tiempo: el modelo servido se mueve. Ver
  [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]].
