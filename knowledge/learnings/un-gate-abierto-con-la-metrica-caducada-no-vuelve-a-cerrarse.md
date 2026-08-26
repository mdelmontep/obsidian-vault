---
title: un gate abierto con la métrica caducada no vuelve a cerrarse
date: 2026-08-26
source: facturaia
tags: [facturaia, agentic, gates, medicion, histeresis]
---

`evaluarGate` (`src/lib/agentic/gate.ts`) empieza con «sin accuracy → mantener»,
comentado como *defensa anti-auto-activación*. Es cierto, y también es lo
contrario: es defensa anti-auto-**desactivación**.

Medido en prod el 26-ago-2026: **ninguna org tiene una sola decisión verde
resuelta en los últimos 30 días**, así que `auto_accuracy` es `null` para todas y
el cron `agentic-gate-sweep` devuelve `mantener/sin_volumen_medido` cada día.
`AgentesiaLab SL` sigue en `activo` con `gate_abierto=true` **por una medición del
23-jul** — 34 días de permiso concedido por un acierto que ya nadie mide. La
histéresis 95/90 mira volumen para abrir y para cerrar, pero nada mira la EDAD de
la última medición.

Regla: un permiso que se concede midiendo tiene que caducar cuando la medición
caduca. Si el mismo `null` significa «no abras» y «no cierres», el estado abierto
es absorbente: se entra midiendo y se sale sin poder medir.

Va con [[un-gate-cuyo-denominador-es-la-zona-que-sus-candados-vetan-nunca-abre]] y
[[el-camino-en-bloque-cierra-la-medicion-pero-no-aprende]] (por qué el denominador
se secó).
