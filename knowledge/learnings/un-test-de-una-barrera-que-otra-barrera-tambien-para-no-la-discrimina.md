---
title: un test de una barrera que otra barrera más ancha también para no la discrimina
date: 2026-09-13
source: agh-iberica
tags: [testing, mutacion, metodo, defensa-en-capas]
---
Con defensas en capas (tope declarado → tope real al procesar), el caso «bomba honesta» sale rojo sin la
primera barrera igual que con ella: lo para la segunda. El test pasa y la barrera no tiene cobertura.
Caso (AGH #1692): zip bomb con tamaño declarado verdadero; quitando el tope DECLARADO, lo cortaba
`maxOutputLength` al inflar → 400 igual. `mutate` dio SIN VÍCTIMA en 2 barreras con los tests en verde.
Fix: un fixture que SOLO esa barrera puede parar — p. ej. bytes comprimidos que zlib rechaza
(`Buffer.alloc(n, 0xff)`) con un tamaño declarado abusivo: sin la barrera, la respuesta cambia de forma
(500 en vez de 400), así que el caso ya no puede quedar verde por la capa de detrás.
Regla: una mutación por barrera, no por feature; si hay capas, cada una necesita su víctima propia.
Relacionado: [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[un-mutante-con-victima-puede-haber-muerto-en-otra-etapa-del-gate]]
