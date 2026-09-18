---
title: una etapa nueva del embudo no entra sola en los gates que listan etapas
date: 2026-09-18
source: clinica-zen
tags: [kommo, n8n, embudo, gates]
---

Los gates que deciden por etapa llevan listas literales de `status_id` (cerrados, atendidos,
no-molestar). Cuando el cliente añade una etapa al embudo, esa etapa **no está en ninguna lista**, así
que cae en el «else» — que suele ser la rama que actúa.

Caso real (15-sep-2026, Clínica Zen): «ACUDE Y SE VA SIN CITA» (111224991) no estaba en `ATENDIDOS`
del gate de reenganche, así que a un paciente que ya había venido a la cita y acababa de valorar el
servicio le llegó «¿Sigues por ahí?» una hora después.

Al tocar cualquier flujo que dependa de etapas: listar las etapas REALES del embudo
(`GET /api/v4/leads/pipelines`) y cruzarlas contra cada lista del código. Y si el motivo de no actuar
es «esta conversación ya está cerrada por otro flujo», marcarlo en la tabla de dedupe desde ese otro
flujo, que no depende de la etapa.
