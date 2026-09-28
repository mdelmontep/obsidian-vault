---
title: leer un valor desde el updater de setstate tras un await no funciona en react
date: 2026-09-28
source: agh-iberica
tags: [react, hooks, testing]
---
Patrón roto: `let v; set(s => { v = s.x; return s; }); await otra(v);`. React ejecuta el updater funcional
en el siguiente render, no dentro de la llamada a `set`, así que `v` sigue `undefined` y el segundo paso no ocurre.
Caso real (AGH #2092): «Confirmar el CV» encadenaba revisar → confirmar leyendo la versión revisada así.
En producción no confirmaba nunca.

Por qué no lo vio nadie: los tests pasaban un `set` fake SÍNCRONO (`set = f => { state = f(state) }`), que
ejecuta el updater al momento. El fake horneaba la premisa falsa.

Fix: que la función async DEVUELVA el valor que la siguiente necesita (`const v = await revisar(); await confirmar(v)`),
en vez de sacarlo del estado.
Test con dientes: un `set` DIFERIDO que encola los updaters y los aplica después. Ese test falla con el patrón roto.
Ver [[setstate-anidado-en-updater-rompe-bajo-strictmode]] · [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]].
