---
title: en kommo, un status_id de otro pipeline mueve el lead a ese pipeline sin avisar
date: 2026-09-21
source: simarro
tags: [kommo, crm, n8n, pipelines]
---
`PATCH /api/v4/leads/{id}` con solo `{"status_id": X}` —o con `pipeline_id` fijo— no falla si el lead
vive en otro pipeline: lo **traslada** al pipeline dueño de X. Un automatismo escrito pensando en
Ventas se lleva así a los leads de cualquier otro embudo, y como responde 200, nadie lo ve.

Caso: Simarro, 13-21 sep. Recordatorios 48h (`Post-visita`) y la anulación/cambio de cita forzaban
Ventas; 9 valoraciones reales acabaron en Ventas (algunas en "Cancelado"), sin error en ninguna ejecución.

Fix: leer el `pipeline_id` actual antes de escribir (GET del lead) y mapear la etapa por pipeline; si la
lectura falla, NO mover. Para encontrar los ya afectados: `GET /api/v4/events?filter[type]=lead_status_changed`
y filtrar `value_before.lead_status.pipeline_id != value_after...pipeline_id`.
Los estados 142/143 (ganado/perdido) existen en todos los pipelines: con ellos `pipeline_id` es obligatorio.
