---
title: insertar en batch da el mismo created_at y ordenar por fecha deja de desempatar
date: 2026-08-15
source: claude-code-session
tags: [postgres, orden, datos, ui]
---
`now()` es constante dentro de una transacción, así que un `insert` de N filas
les pone el MISMO `created_at` al microsegundo. Cualquier `ORDER BY created_at`
sobre ese grupo devuelve el orden físico de las filas: no es aleatorio, pero
tampoco es un criterio — cambia con un vacuum o un plan distinto.

Lo peligroso es el comentario que suele acompañarlo. Caso real (TuFacturaIA):
«el más reciente, determinista: enseñar el primero que venga era una lotería».
Escrito de buena fe, y falso desde el día en que el productor pasó a subir sus
6 clips de una vez. La UI enseñaba uno arbitrario y nadie lo notó porque los
seis eran plausibles.

Regla: si el dato tiene un orden propio del dominio (escena, línea, secuencia),
**persistirlo en su columna** aunque el productor ya lo sepa; no reconstruirlo
del JSON del run ni deducirlo de la fecha. Y cuando la fecha sea el único
criterio disponible, añadir `id` como último desempate para tener orden total.
Señal de alarma: la palabra «determinista» en un comentario sobre un `sort` por
timestamp.
