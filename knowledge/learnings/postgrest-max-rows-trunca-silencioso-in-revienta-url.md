---
title: postgrest trunca a 1000 filas en silencio y .in() grande revienta la url
date: 2026-07-03
source: claude-code-session
tags: [supabase, postgrest, paginacion, bugs-silenciosos]
---
Dos límites de PostgREST que fallan sin error visible en queries "sacar todo":
1. `db-max-rows` (Supabase hosted: 1000) corta el resultado SIN señal — un
   export/agregado sobre >1000 filas devuelve importes de menos y nadie se
   entera. Los embedded selects (`lineas:tabla(...)`) NO cuentan para el cap.
2. `.in(col, ids)` viaja en la URL del GET (~39 bytes/UUID): a partir de
   ~400-840 ids el edge corta la request → 500.
Patrón fix (FacturaIA `load-facturas-contables.ts` + `admin-connections.ts`):
chunkear ids a ≤150-500 por request y paginar con `.order(pk).range(from, to)`
en bucle hasta `page.length < PAGE_SIZE` (el order estable es obligatorio o
range salta/repite filas). Test: cliente fake que simula el cap de 1000.

Señal de diagnóstico: si pides `{ count: 'exact' }` el count SÍ es exacto (lo
calcula la BD), pero el importe (reduce en JS sobre filas truncadas) sale de
menos → count y cifra €/ quedan incoherentes entre sí; esa discrepancia delata
el truncado. Como las filas no van ordenadas, además el corte es no determinista.

**Barrido 02-ago: no es puntual, son ~55 sitios en 12 áreas**, escritos por gente
que conocía el límite (3 helpers paginan bien, con comentarios citando
`db-max-rows`, y al lado el patrón reintroducido). Lo peor: **cuatro avisos de
truncado son matemáticamente inalcanzables** porque comparan contra un cap de
5.000 que PostgREST nunca deja alcanzar (`truncated` en informes de ventas y
gastos, `capped` en copiloto-purge, el `break` de logs-retention-sweep — que sale
siempre en la 1ª vuelta y deja 11.158 filas sin purgar). Alarmas que no suenan.
Medido: el informe de presupuestos agrega 1.000 de 122.432 líneas y muestra <1 %
del importe; el universo fiscal comparte tope con los cuadres C-0x, así que
validarían en verde una declaración incompleta. Corolario: caso por caso no
cierra esto — hace falta guard (lint contra `.limit(n>1000)` + helper que
devuelva `{rows, complete}`).

**Hecho el 02-ago (#1475, #1477), y con dos correcciones al diagnóstico:**
1. **El caso peor no lleva `.limit()`**, así que un guard que busque límites
   grandes no lo ve: una query sin límite se corta a 1.000 igual. Era el
   informe de presupuestos — tres lecturas sin límite sobre 122.432 líneas.
2. **No mostraba «<1 % del importe», mostraba 0 €.** El `.in()` con ~1.000 ids
   devolvía **400** y el `(await …).data ?? []` de al lado lo convertía en cero
   filas. Medido: 500 ids (18,5 KB de URL) pasan, 700 (25,9 KB) no → chunk 300.
   El `?? []` sobre una lectura sin mirar `error` es el multiplicador del daño.
3. **Los fakes de test tienen que reproducir los dos límites** (servir 1.000
   como máximo, 400 con ids largos). Sin eso el test no distingue paginar de
   truncar y pasa con el bug dentro: por eso llevaba tanto sin verse. Los dos
   tests nuevos fallan sin el fix (`1000 to be 1200`, `+0 to be 12000`).

**Y el corolario que más ahorra: paginar + trocear por `.in()` es CORRECTO y
carísimo.** El informe pasó de rápido-y-falso a correcto-en-56,6 s con 222
peticiones. Como los embebidos no cuentan para el cap, pedir los hijos ANIDADOS
(`presupuestos?select=…,nodos(…,lineas(…))`) baja lo mismo en **3 peticiones y
5,7 s** — solo pagina la tabla raíz. Mismos 2.380/37.139/122.432 y **el mismo
importe al céntimo** (223.295.013,78 €, comparado camino contra camino). Regla:
si la relación es padre→hijos, embebido; `.in()` troceado solo cuando los ids
vienen de otra consulta que no se puede expresar como relación.

**Y el `.in()` también rompe los DELETE, con error visible que nadie mira.**
`logs-retention-sweep` llevaba TRES días en `error` (`api_request_log_delete_
failed: Bad Request`) con 15.006 filas sin purgar; se vio leyendo `cron_runs`,
no por una alerta. Trampa en la que caí: bajar el tope de SELECCIÓN de 5.000 a
1.000 —necesario para que el `break` del bucle funcione— **no arregla el
borrado**, porque la URL del DELETE sigue llevando mil ids. Dos límites, dos
arreglos. Corolario para clasificar: un `.limit()` grande solo es bug si además
AGREGA; en un listado muestra menos filas. Y si no quieres paginar, saca el aviso
de un `count: 'exact'` (como `/cobros/aging`), nunca de comparar con el cap.

**18-ago, la clase que faltaba: a veces no devuelve MENOS, devuelve MAL.** Hasta aquí el daño
se describía como "importes de menos". Barrido de inventario en TuFacturaIA: un `MAX(created_at)`
calculado en JS sobre las 1.000 primeras filas **en orden indefinido** daba una fecha cualquiera,
no la última; y un contador de alarmas sobre filas truncadas salía **cero** cuando las alarmas
caían más allá de la fila 1.000. Un importe corto se huele; una fecha plausible y un "no hay
alarmas" no los huele nadie. Corolario para el criterio de arreglo: los agregados de dinero y los
contadores de decisión deben **fallar cerrado** (500) si no caben en el tope, no devolver la
cifra calculada sobre el conjunto incompleto.
