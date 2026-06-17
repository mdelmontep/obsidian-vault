---
title: cron dokploy con expresión */N en hora fija no se recupera tras caída del scheduler
date: 2026-06-17
source: claude-code-session
tags: [dokploy, cron, scheduler]
---
Si el control-plane de Dokploy cae durante la ventana de un cron, al revivir
RECUPERA los crons de disparo único (`0 4 * * *`, `15 3 * * *`) pero NO los de
step de minutos dentro de hora fija (`*/30 4 * * *`) → se quedan sin correr y
saltan a ámbar/rojo sin que nadie lo note.
Caso real: tras el OOM del 17-jun (control-plane 7h caído), `module-events-purge`
(`*/30 4`) fue el único de su tanda que no se recuperó; el resto (disparo único)
corrió tarde al revivir el scheduler.
Fix: convertir a disparo único (`0 4 * * *`). El 2º disparo `*/30` era redundante
(borraba 0). Evidencia empírica, no documentado en Dokploy.
Ver [[dokploy-api-schedule-update-requiere-payload-completo-no-patch]] · [[dokploy-api-schedule-runmanually-trigger-cron-on-demand]]
