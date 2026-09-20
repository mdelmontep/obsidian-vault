---
title: la cola de fia-gate miente en dos direcciones: encolado parece fallado y colgado parece en curso
date: 2026-09-21
source: agh-iberica
tags: [gate, harness, git, claude-code]
---
`fia-gate` serializa gates y pushes por un slot (`~/.claude/gate/state/slots/slot.N/pid`). Dos
lecturas falsas, las dos medidas el 21-sep:

1. **Fichero de salida VACÍO = encolado, no fallado.** Lancé el mismo gate dos veces creyendo que el
   primero no había arrancado. El segundo quedó en `sleep 7200` esperando un slot que sostenía **su
   propio ancestro** (el wrapper no lo suelta hasta que su hijo termina, y su hijo era el segundo):
   deadlock limpio, con el `git push` encolado detrás. Antes de relanzar: `pgrep -f gate.ts` y mirar
   quién tiene el slot.
2. **Un push «colgado» puede haber entrado ya.** 7 min con el `git` vivo; la red respondía al
   instante por fuera (`git ls-remote`), y al matarlo el remoto **ya estaba en mi commit**. Lo que
   colgaba era liberar el slot, no el push. Comprobar la punta remota ANTES de reintentar, nunca
   durante — ver [[verificar-un-push-mientras-sigue-en-vuelo-miente]].

Diagnóstico en un comando: `ps -ax -o pid=,ppid=,etime=,comm=` sobre el pid del slot; si su hijo es
un `sleep` largo, está esperando, no trabajando.
