---
title: un guard que fecha la evidencia por el commit la invalida en cada rebase — fíchala por contenido
date: 2026-08-04
source: claude-code-session
tags: [gate, ci, evals, git, metodo, agh]
---
Patrón: un guard exige que un artefacto caro (corrida de evals, build, benchmark) sea
**posterior** al commit que tocó lo medido, con `git log -1 --format=%cI`. Eso es el
**committer date**, y un `rebase` lo reescribe. Con varias sesiones mergeando, la secuencia
normal —medir, rebasar antes de mergear— **invalida la medición con el contenido idéntico**.

Coste real (AGH #855): dos corridas completas en una tarde, ~12 $ tirados. Y el escape que
existía no servía: declaraba en la PR «cobertura CERO», que era **falso**.

La pregunta correcta no es *«¿se corrió DESPUÉS del commit?»* sino **«¿se corrió sobre ESTE
contenido?»** → el artefacto guarda un **hash** de las fuentes y el guard lo compara con el
árbol. Sobrevive a rebase, `--amend` y cambio de rama.

Y no afloja el guard, lo aprieta: por reloj, un artefacto reciente pasa aunque se hubiera
corrido con otro contenido (tocar, correr, volver atrás). Por hash, no.

Detalles que cargan peso: sin hash → caer al reloj (degradación segura); la RUTA entra en el
hash (mover el fichero es cambio real); ordenar por ruta (el orden de `readdir` no está
garantizado); y el IO en **un solo módulo** — el que escribe el artefacto y el que lo juzga
tienen que calcular la misma huella o divergen. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
