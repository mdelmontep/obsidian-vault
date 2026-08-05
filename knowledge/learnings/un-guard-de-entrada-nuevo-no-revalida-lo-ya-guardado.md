---
title: un guard de entrada nuevo no re-valida lo ya guardado, y el scanner que nadie corre no cuenta
date: 2026-08-06
source: claude-code-session
tags: [datos, validacion, prod, metodo]
---
El saludo de todas las llamadas de un usuario decía **«Soy Aquí está, tu asistente»** — el STT había
transcrito una muletilla como nombre del asistente. El guard **existía y era correcto**: la muletilla
estaba literalmente en la lista de rechazo. Pero el guard entró el 27-jul y **la fila se había escrito
el 21-jul**: seis días antes. **Endurecer la entrada no toca lo ya persistido.**

Y no es que nadie lo pensara. La sesión del guard dejó escrito un scanner read-only, con esta nota en su
docstring: *«solo se deja escrito para que un humano decida cuándo correrlo»*. **Nadie lo corrió en 9
días**, y el defecto siguió saliendo en cada llamada.

**Regla: un guard de entrada nuevo trae su barrido de lo ya guardado EN EL MISMO PR**, o el barrido se
queda como issue con dueño. Un script sin ejecutar no es una mitigación, es una intención — la misma
trampa que «una decisión que vive en la prosa de un cierre no está en ninguna cola».

Mejor todavía si el barrido no depende de que alguien se acuerde: que el arranque **loguee** (no borre)
las filas que hoy fallarían la validación. Así el drift es visible sin intervención humana.

Al medirlo, el alcance era **una fila de nueve** — barato de arreglar, y por eso más absurdo el retraso.
