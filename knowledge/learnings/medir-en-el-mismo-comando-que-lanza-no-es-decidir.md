---
title: una medición dentro del comando que lanza no gobierna nada si no hay un `if` detrás
date: 2026-09-07
source: facturaia — colisión de dos gates el 7-sep-2026
tags: [harness, concurrencia, gates, medicion]
---

Con varias sesiones compartiendo una máquina, la regla «mide la carga **en el
mismo comando que lanza**, no en un turno anterior» resuelve un problema real: la
foto caduca en menos de lo que tarda uno en decidir (medido: `load 5,48` y
`load 9,02` con un minuto de diferencia).

Pero resuelve solo la mitad. El 7-sep monté un push con `uptime`, `swapusage` y
un `ps` de gates vivos dentro del bloque que hacía el `git push`. **El log trae
impreso, tres líneas antes de arrancar, el gate ajeno con 3 segundos de vida** —
y arrancó igual. La medición estaba, era correcta y llegó a tiempo; lo que
faltaba era que ALGO dependiera de ella. Dos gates a la vez, colisión.

La regla completa: **el lanzamiento depende de la medición**, con un `if` que
salga sin hacer nada. Un `echo` de la medida es documentación, no control. Es la
misma familia que un trinquete que corre, imprime y no bloquea: no trinca.

Al abortar, por ÁRBOL (`kill -TERM -<pgid>`), nunca `pkill` por nombre — deja la
suite huérfana escribiendo en el mismo log. Y se verifica el EFECTO
(`git ls-remote`), no el código de salida, que devolvió 144.
Ver [[el-suelo-de-carga-de-una-maquina-compartida-no-lo-ponen-las-sesiones]].

**Y el `if` hay que probarlo con el caso que DEBE bloquear** (lo aplicó
`facturaia-72` el mismo día): lanzó su guardia nuevo con el gate ajeno corriendo
y comprobó que abortaba con `exit 17` nombrando los procesos que lo motivaron.
Un guardia probado solo en verde pasa trivialmente y no discrimina nada.

**Y la medición tiene que ser de la MÁQUINA, no del mensaje del vecino.** La otra
mitad del mismo día: una sesión disparó en cuanto la anterior avisó de que soltaba,
con `load 10,36` — porque la carga **tarda en bajar detrás de un gate que acaba**.
«Ha soltado» y «está libre» están separados por minutos. El aviso del que sale
sirve para saber que puedes mirar; no sustituye al `uptime`.
