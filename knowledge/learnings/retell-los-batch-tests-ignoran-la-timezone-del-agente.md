---
title: los batch tests de retell ignoran la timezone del agente
date: 2026-10-01
source: simarro
tags: [retell, voz, conversation-flow, testing]
---
`{{current_hour}}` y `{{current_time}}` siguen el `timezone` del agente (por defecto America/Los_Angeles: sin fijarlo, «estamos abiertos» se evalúa con 9 h de desfase). Pero los batch tests ejecutan el flow **sin la config del agente**: con `timezone: Europe/Madrid` ya puesto, una rama horaria seguía saliendo siempre «fuera de horario» en simulación.

Fix para probar: inyectar `system_timezone` como dynamic variable del caso (`Europe/Madrid` para dentro de horario, `Asia/Tokyo` para forzar fuera). 7/7 tras inyectarlo.

Además, para decidir por hora usa un nodo `branch` con **ecuaciones** (`{{current_hour}} >= 10 && < 14`, `{{current_time_Europe/Madrid}}` not_contains `Saturday`). La misma condición escrita como prompt acertó 1/3.

Caso real: Simarro, v47 (1-oct-2026), transferencia a humano solo en horario de oficina. Ver [[retell-el-nodo-end-no-habla-la-despedida-necesita-nodo-propio]] · [[retell-la-condicion-del-edge-manda-sobre-el-prompt]].
