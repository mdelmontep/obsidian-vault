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

Tercera variante (1-sep-2026): `(cmd > log 2>&1 &)` o `nohup cmd &` **dentro de una llamada en
background**. El arnés reporta «exit code 0» a los pocos segundos y es el del shell que desasió,
no el del comando, que sigue corriendo. El tell es el **tiempo**: un gate que canta verde en 3 s no
ha compilado nada. Esperar por el PID (`while kill -0 $PID; do sleep 5; done`) o por el `EC=` del log.

Cuarta variante (5-sep-2026), la que rompe el gate entero: **`set -e` + `cmd > log 2>&1; a=$?`
nunca asigna `a`**. Con errexit, un comando simple que falla aborta el script en el acto, antes de
llegar al `; a=$?` de su misma línea. Efecto: el paso rojo mata el gate sin llegar nunca al `echo`
final, y quedan en pie los logs de una corrida anterior como si fueran de esta — un gate que solo
sabe cantar verde. `cmd || a=$?` sí contiene el fallo (el último comando de la lista `||` es la
asignación, no `cmd`), y el script siempre llega a imprimir sus cuatro exit codes.

Regla: si un número decide si algo pasa o falla, **tiene que viajar con la evidencia**. Un exit code
que vive solo en el terminal se pierde en cuanto hay un wrapper, un background o un resumen por medio.
Ver [[un-gate-por-pipe-da-verde-con-el-push-abortado]].
