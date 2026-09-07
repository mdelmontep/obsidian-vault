---
title: una rectificación que cambia la decisión de otro tiene que llevar el estado del recurso dentro
date: 2026-09-07
source: facturaia — cuatro sesiones compartiendo una máquina el 7-sep-2026
tags: [multiagente, coordinacion, concurrencia, harness]
---

Con varias sesiones compartiendo una máquina, un consejo correcto entregado en
mal momento provoca la colisión que el consejo pretendía evitar.

Medido el 7-sep: `facturaia-38` había dicho a `facturaia-76` que no relanzara un
test («no cabe»). Al descubrir que su número era malo, le mandó la rectificación
—«sí puede merecer la pena relanzar»— **sin decirle que él estaba entrando en la
máquina en ese mismo minuto**. 76 actuó de forma razonable sobre lo que le
dijeron. Resultado: dos suites a la vez y `load 3,40 → 15,34`, justo la condición
que echó a perder la única toma limpia del día, que era la que iba a decidir el
asunto.

La regla: **si tu mensaje cambia lo que otro va a hacer con un recurso
compartido, el estado de ese recurso va DENTRO del mensaje** — «relanza, pero yo
entro ahora, espera a que suelte». Sin eso mandas la mitad útil y la otra mitad
la rellena el que lee, con lo único que tiene: su propia foto, ya caducada.

Corolario para el que recibe: una rectificación no es una autorización de turno.
Ver [[medir-en-el-mismo-comando-que-lanza-no-es-decidir]] — el aviso del vecino
nunca sustituye al `ps` y al `uptime` del que va a lanzar.
