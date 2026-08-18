---
title: matar un proceso no lo para si detrás hay un servicio que lo resucita
date: 2026-08-18
source: learn-agentesia
tags: [macos, launchd, procesos, gotcha, operacion]
---

`pkill -f runner/index.mjs` → «runners vivos: 3». Cada vez que moría, volvía en segundos con **PPID 1**, que es la pista: su padre ya no existe y lo adoptó `launchd`.

**Causa.** Un LaunchAgent con `KeepAlive: true` (`~/Library/LaunchAgents/*.plist`). El proceso no es un proceso: es un **servicio**.

**Comprobar antes de pelearte con el `kill`:**

```sh
ps -o ppid= -p <pid>                    # PPID 1 = huérfano adoptado, sospecha
ls ~/Library/LaunchAgents | grep <algo> # y en /Library/LaunchDaemons
launchctl list | grep <label>
```

Pararlo de verdad es `launchctl unload <plist>`; en Docker, el equivalente es `restart: unless-stopped`.

**El corolario útil, que compensa el susto:** si hay servicio, **reiniciar es matar**. No hace falta relanzar a mano —y hacerlo duplica el proceso—, que es justo lo que había pasado: dos runners a la vez, uno con **28 h** de antigüedad ejecutando una versión vieja del código.

**Y al matar:** si el proceso no libera lo que tenía reclamado (aquí, trabajos en `ejecutando`), queda colgado. Comprobarlo forma parte de pararlo.

Ver [[un-agente-muerto-puede-dejar-un-motor-desacoplado-vivo]] · [[contenedor-que-no-vuelve-tras-reboot-dos-causas-que-se-confunden]]
