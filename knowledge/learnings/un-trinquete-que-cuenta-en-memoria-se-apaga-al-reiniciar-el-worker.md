---
title: un trinquete que cuenta en memoria se apaga justo en las tandas que tienen rojos
date: 2026-09-22
source: facturaia
tags: [testing, playwright, candados, trinquetes]
---
El candado del eje de permisos de FacturaIA aplicaba su suelo (64 endpoints medidos) **solo si
la tanda había ejecutado el universo entero**, y esa cuenta vivía en una variable del proceso del
worker. Con `retries: 1`, un fallo **reinicia el worker**: el contador vuelve a cero, los casos ya
ejecutados dejan de contarse, `ejecutados` nunca iguala al universo y el caso final se **salta**.

O sea: el trinquete se apagaba solo en las tandas con rojos, que son las únicas en las que sirve.
Y un `skipped` no se distingue de un verde en el informe, así que nadie lo veía.

Patrón, no anécdota: **cualquier agregado que cruce casos de una suite tiene que vivir fuera del
proceso** (un fichero en `test-results/`, una línea por caso, manda la última por id — así el
reintento corrige en vez de duplicar). Aplica a Playwright, a vitest con `pool: 'forks'` y a
cualquier runner que reinicie el worker al fallar o al repartir shards.

El tell para buscarlo: un `test.skip(condición_sobre_un_contador)` en el caso que cierra la suite.
