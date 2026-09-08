---
title: la mutación que desbloquea el guard tiene que ser sobre un fichero DEL STAGE
date: 2026-09-08
source: facturaia
tags: [hooks, mutacion, gates]
---
`mutate-guard` bloquea un commit que toca código **y** añade tests sin víctima
demostrada. Cruza el registro de mutaciones contra los ficheros **de código que
están en el stage de ESE commit** — no contra "algo que mutaste hace un rato".

Trampa medida el 8-sep: el test nuevo vigilaba `core.hooksPath`, así que muté
`package.json` (donde se declara) y salió `✓ VÍCTIMA`… y el guard siguió
bloqueando, con razón: `package.json` no estaba en el stage. La mutación tiene que
caer sobre `.githooks/pre-push` / `pre-commit`, que era lo que el commit cambiaba.

Consecuencia útil, no burocracia: si no encuentras dónde mutar **dentro de lo que
cambias**, tu test no está midiendo tu cambio. Ahí el arreglo fue escribir un
segundo test que ejecuta los hooks de verdad contra un repo temporal ajeno, y
entonces sí hubo dónde mutar. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
