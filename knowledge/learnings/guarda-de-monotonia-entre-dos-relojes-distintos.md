---
title: una guarda de monotonía entre dos relojes distintos es un no-op silencioso y permanente
date: 2026-09-05
source: mandadm
tags: [postgres, concurrencia, maquina-de-estados, testing]
---
`update … where $at > last_event_at` protege de reentregas SOLO si las dos marcas salen del MISMO
reloj. En MandaDM `last_event_at` lo escribía la transición 6 con la marca de **Meta**
(`entry.time`), y la 7 comparaba contra `new Date()` del worker: dos relojes sin orden garantizado.
Si el ajeno va por delante —o cae en el mismo milisegundo— el UPDATE no toca fila, la función
retorna antes de cerrar, y la conversación queda `open` con el enlace ya enviado. Corre una vez por
fila de cola, sin reintento: un solo fallo es permanente. Con réplicas (`for update skip locked`),
la marca puede venir de otro contenedor con otro reloj.

**El síntoma engaña:** se presenta como test intermitente. Y el "arreglo" de acercar los dos relojes
(poner la marca con el reloj de Node) lo empeora: los deja a ~0 ms, que es justo el valor que rompe
un `>` estricto — el fichero entero falla con el pool caliente y el test aislado pasa.

**Patrón:** separar las dos guardas, que nunca fueron la misma. El CAS de estado (`where step=$2 and
status='open'`) es incondicional y es lo que serializa; la de monotonía solo aplica cuando el `at` es
la marca del sistema externo. Y hacerlo **explícito en el tipo** (`atClock: 'meta-event' | 'process'`
obligatorio), no en un comentario: una llamada nueva sin clasificar no compila. Ver
[[test-verde-puede-codificar-el-bug-como-esperado]].
