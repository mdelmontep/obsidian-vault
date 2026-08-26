---
title: el umbral de un retry sale de medir la distribución real, no de estimarlo
date: 2026-08-26
source: agency-portal
tags: [heuristicas, retry, evidencia, flota-ia]
---
Al decidir cuándo NO reintentar un `get-call` que trae el transcript, escribí
`MIN_TRANSCRIBABLE_DURATION_SECONDS = 5` con el razonamiento "una llamada de
menos de 5 s no puede tener turnos". Suena obvio y es falso: medido contra prod,
de las 179 interacciones de voz sin transcript **176 son de duración cero**
(168 `failed`, 8 `completed`) y solo 3 tienen duración — y una de esas 3 dura
menos de 5 s, así que el umbral inventado se habría comido justo a una de las
víctimas que el fix existía para recuperar. El corte correcto era el que la
distribución ya dibujaba: `duration === 0` no reintenta, `> 0` o `null` sí.
Patrón: una constante mágica en un guard de reintento es una hipótesis sobre la
forma de los datos. Si los datos están en una BD a la que tienes SELECT, la
hipótesis se mide antes de escribirla (un `group by` basta), y el comentario del
código cita la medición con fecha. Ver
[[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
