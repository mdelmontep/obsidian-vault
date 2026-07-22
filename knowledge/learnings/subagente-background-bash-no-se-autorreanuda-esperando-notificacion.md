---
title: subagente que backgroundea un bash largo (npm run gate) no se autorreanuda al terminar — se queda "esperando notificación" para siempre
date: 2026-07-22
source: claude-code-session
tags: [claude-code, agentes, workflow]
---
Un subagente (Agent tool) que lanza un comando largo (`npm run gate`) con Bash `run_in_background:true` y luego cierra su turno diciendo "esperaré la notificación" NO se autorreanuda cuando ese proceso termina — la notificación de background-bash es para el loop que la lanzó en vivo, no sobrevive a que el propio agente ya haya devuelto el control. Resultado: el agente queda "colgado" indefinidamente esperando algo que nunca llega, aunque el proceso ya terminó hace rato.

Detectarlo: el `<result>` del `task-notification` dice literalmente "esperando la notificación de X" y no hay progreso real (mismo git status en dos notificaciones seguidas).

Fix: desde el padre, `ps aux | grep <comando>` para comprobar si el proceso de background ya terminó; si terminó, `SendMessage` al agente diciéndole explícitamente "ya terminó, compruébalo tú mismo y sigue en el mismo turno sin backgroundear" — no vale limitarse a "sigue", hay que decirle que corra el comando en primer plano o compruebe el resultado ya, porque repetirá el mismo patrón si el prompt es ambiguo.

Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]] (caso hermano: agente muerto por session limit vs. agente vivo pero colgado esperando una notificación fantasma).
