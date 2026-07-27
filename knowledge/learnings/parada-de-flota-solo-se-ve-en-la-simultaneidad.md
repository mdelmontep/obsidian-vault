---
title: una flota de workers parada no se ve por worker, solo en la simultaneidad
date: 2026-07-27
source: claude-code-session
tags: [monitoring, cron, alerting, facturaia, incidentes]
---
Patrón "skip limpio por lock": worker con UNIQUE parcial de concurrencia que, si ya
hay uno en vuelo, **sale sin escribir fila**. Si la base cae y el run en vuelo se
cuelga, cada tick siguiente skipea sin registro → **no hay fallos que contar** y
ningún contador por racha crece. La salud por historial de CADA worker devuelve
'ambar' (colgado sobre histórico sano) y tras el reapeo también (racha = 1). Nunca
rojo, nunca email: cero avisos con la flota parada 2 h 41 min.
La señal NO está en ningún worker aislado: está en que caen VARIOS A LA VEZ, y de
eso solo se entera quien libera los locks (el reaper). Emitir aviso cuando libera
≥N en una pasada. **Saca N de la distribución histórica, no a ojo**: en 8.653
pasadas → 0 zombies ×8.614, 1 ×23 (rutina de deploy), 2 ×1, 9 ×1 (el incidente).
Con N=3, un aviso en toda la historia y era el correcto.
Y ojo con la media: p50 de 200 ms con `max` de 2 h 42 min daba media de 8 s, que
me hizo inventar un problema de carga inexistente. Mirar la distribución primero.
Corrige [[cron-alta-frecuencia-exigir-2-fallos-consecutivos-antes-de-paginar]].
Es post-mortem, no detección en vivo: eso es del dead-man's switch EXTERNO — ver
[[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]]. FacturaIA PR #1241.
