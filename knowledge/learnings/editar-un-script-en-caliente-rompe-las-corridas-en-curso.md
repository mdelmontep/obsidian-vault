---
title: editar un script en caliente rompe las corridas ajenas, aunque el resultado final sea válido
date: 2026-08-24
source: facturaia
tags: [bash, harness, concurrencia]
---
Un push mío murió con `syntax error near unexpected token 'do'` sobre un `printf` del arnés.
El fichero no estaba roto: `bash -n` salía limpio. Lo que pasó es que **bash lee el script
mientras lo ejecuta**, y otra sesión lo estaba reescribiendo en ese momento, así que mi proceso
leyó media versión de cada.

Coste real: el hook tradujo aquello a «Push bloqueado: build con errores», o sea que **un fallo
del arnés se disfrazó de fallo del código** — el mismo disfraz que el watchdog matando la suite.

Regla: un script que otros pueden estar ejecutando se actualiza escribiendo a un temporal y
haciendo `mv` encima. El rename es atómico: quien esté dentro termina con la versión vieja
entera. Aplica igual a hooks, wrappers y cualquier `.sh` compartido entre sesiones.

Misma familia que dos agentes escribiendo en el mismo árbol de trabajo a la vez.
Ver [[semaforo-que-envuelve-un-comando-que-vuelve-a-pedirle-slot-se-interbloquea]].
