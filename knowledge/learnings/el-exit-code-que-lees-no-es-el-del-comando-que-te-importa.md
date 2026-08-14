---
title: el `$?` de un comando compuesto no es el del comando que te importa
date: 2026-08-14
source: claude-code-session
tags: [bash, gates, ci, verificacion]
---

Hermano del pipe (`git push … | tail` devuelve el exit del pipe). La variante que cuesta más ver:

```bash
npm run gate > gate.log 2>&1; echo "exit=$?"   # ← el $? es del REDIRECT+comando… pero si lo lees
                                               #   desde el resumen de la herramienta, lo que ves
                                               #   es el exit del ÚLTIMO comando de la línea
```

Al correr esto en background y leer «exit code 0» del reporte, el 0 era del `echo`. **El gate había
fallado** (`✗ FALLÓ: agente:test`) y yo canté verde en voz alta.

Fix: que el exit quede **dentro del artefacto que vas a leer**, no en la salida del shell.

```bash
npm run gate > gate.log 2>&1; echo "EXIT_DEL_GATE=$?" >> gate.log
```

Regla: si un número decide si algo pasa o falla, **tiene que viajar con la evidencia**. Un exit code
que vive solo en el terminal se pierde en cuanto hay un wrapper, un background o un resumen por medio.
Ver [[un-gate-por-pipe-da-verde-con-el-push-abortado]].
