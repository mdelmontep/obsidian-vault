---
title: varios runners de ci en el mismo dockerd chocan por nombre de proyecto y limpieza global
date: 2026-10-16
source: facturaia #3614
tags: [ci, docker, supabase, github-actions, gotcha]
---
Cuatro runners self-hosted (`gates-1..4`) en la misma VM comparten **un único dockerd**. Todos
levantaban el stack de Supabase como proyecto `fia-ci` en los mismos puertos, y la limpieza de
bases efímeras barría por una etiqueta GLOBAL: un job tiraba la base del otro a mitad de suite.
Síntoma: `integration` roja 3 veces seguidas en un PR sin cambios de BD, verde en local.

- Nombre de proyecto y puertos POR RUNNER (`fia-ci-<n>`, base + 1000 + 100·n).
- La limpieza acota por una etiqueta con la red del job (`fia.base-efimera.red=<red>`), nunca por la global.
- `stop` previo con reintentos: un stack a medias del job anterior deja puertos cogidos.
- Se prueba con dos runs CONCURRENTES verdes, no con uno.

Relacionado: [[las-bases-efimeras-que-nadie-borra-hacen-eterno-el-arranque-sucio]] · [[facturaia]]
