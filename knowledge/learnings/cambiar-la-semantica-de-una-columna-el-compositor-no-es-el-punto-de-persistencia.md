---
title: cambiar la semántica de una columna: el compositor no es el punto de persistencia
date: 2026-07-27
source: claude-code-session
tags: [arquitectura, verificacion, gate, tests]
---

Cambié el valor canónico en la función de composición (`baseReportada`) y di el bug por cerrado. Ese valor alimentaba el INSERT de UNA tabla y el DTO de respuesta; el INSERT de la OTRA seguía leyendo la variable vieja (`totales.base`). Resultado: migración de datos ✅, camino de edición ✅, **camino de creación intacto** — cada documento nuevo volvía a nacer con el bug que la PR decía cerrar.

- Al cambiar la semántica de una columna, grep de los **puntos de ESCRITURA** (`base:` en cada INSERT / payload de RPC), no del valor que devuelve el compositor. Después: que todas las ramas lean la misma variable y que la vieja **no aparezca en ningún INSERT**.
- **7.516 tests en verde no significaron nada**: ninguno miraba el payload persistido de ese camino. Cobertura de la suite ≠ cobertura del camino que estás tocando. El test que faltaba (mirar `p_presupuesto.base`) falla con `expected 1000 to be 800` en cuanto se revierte.
- La verificación que vale es **crear una entidad NUEVA en prod tras el deploy y leer la fila**. Leer los datos que arregló el backfill no prueba absolutamente nada del código.
- Cuando el smoke post-deploy salió mal, mi primera hipótesis fue el deploy (contenedor viejo) en vez de mi propio cambio. Comprobado antes de acusar: deployment `done`, contenedor recreado, commit correcto. Otra vez la hipótesis cara antes que la barata.

Complementa [[campo-sincronizado-entre-tablas-debe-poblarse-en-todos-los-puntos-de-escritura]]. Nació en TuFacturaIA, ver [[facturaia]] · [[base-persistida-debe-ser-la-imponible-o-total-menos-base-miente]].
