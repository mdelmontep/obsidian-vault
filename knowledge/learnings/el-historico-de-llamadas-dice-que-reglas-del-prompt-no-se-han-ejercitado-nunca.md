---
title: el histórico de llamadas dice qué reglas del prompt no se han ejercitado nunca
date: 2026-09-10
source: laserys-las-rozas
tags: [retell, agentes-voz, prompt, medicion]
---

Antes de dar por buena una regla del prompt, cuenta cuántas llamadas reales la han pisado:
`POST /v2/list-calls` con `filter_criteria.agent_id`, y agrupa por hora, por
`disconnection_reason` y por tool usada.

Sobre 242 llamadas: **49 (20 %) entraban fuera del horario de apertura** —incluidas las 00:48 y las
02:00— y el prompt no lo distinguía, así que "cliente existente → transferir" habría llamado a una
centralita cerrada y el plan B habría dicho "las tengo a todas ocupadas" a las once de la noche.
La misma consulta demostró que `transfer_call` sí funciona (36 usos, 34 con
`disconnection_reason: call_transfer`, así que el pendiente "sin probar" era falso) y que las 90
llamadas cortadas por `no_valid_payment` eran de tres días de junio: incidente cerrado, no problema
abierto.

Detalle de API: `transcript_object` **no** trae las tool calls; para contarlas, mirar
`transcript_with_tool_calls` o `disconnection_reason`.
