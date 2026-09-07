---
title: una verificación corrida antes del cambio destructivo prueba el esquema que vas a borrar
date: 2026-09-06
source: facturaia
tags: [metodo, verificacion, migraciones, esquema]
---
Retirando una columna (`catalogo_servicios.unidades_por_caja`, 31 lectores), corrí
las tres verificaciones de navegador **antes** del `DROP`, con el código nuevo ya
desplegado. Salieron verdes y las di por buenas. No probaban nada: el código nuevo
leía la presentación, sí, pero la columna **seguía existiendo**, así que cualquier
lector olvidado también funcionaba. Verde compatible con las dos hipótesis.

El `DROP` no es el último paso del trabajo: es **el primer momento en que la
verificación discrimina**. Antes, un `COALESCE` superviviente o una vista que aún la
selecciona pasan invisibles; después fallan con `42703`.

Regla: **toda verificación de una retirada se repite después de retirar**, y la
predicción se escribe antes de mirar («6 cajas · 2 unidad»), que es lo que impide
leer el resultado como confirmación. Vale igual para borrar un env, una feature flag
o una ruta: mientras el camino viejo siga en pie, el verde no distingue.
Ver [[una-medida-compatible-con-la-hipotesis-no-es-una-medida-de-la-hipotesis]] ·
[[un-prompt-de-continuacion-propaga-los-punteros-que-no-abriste]].
