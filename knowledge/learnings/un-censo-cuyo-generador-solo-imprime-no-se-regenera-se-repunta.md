---
title: un censo cuyo generador solo imprime no se regenera, se repunta a mano
date: 2026-09-02
source: facturaia — PR #2379 (tap-target-inventario tras partir un componente)
tags: [trinquetes, censos, refactor, tests, facturaia]
---

Partir un componente en dos mueve botones de fichero y pone su censo en rojo: N entradas
«nuevas» y N «desaparecidas», simétricas, mismas etiquetas. El reflejo es correr el generador
y pegar su salida. **Antes, mira si el generador escribe el fichero.**

En facturaia hay dos familias con la misma pinta y comportamiento opuesto:
- **Trinquetes con baseline derivable** (`inline-style`, `design-debt`, `file-size`,
  `global-css`, `max-rows`): tienen `writeFileSync` y un `--write`. Regenerar es correcto.
- **Censos con juicio humano** (`tap-target-inventario.mjs`): solo importan `readFileSync` y
  hacen `console.log`. Su JSON lleva campos que el script **no puede derivar** —en éste,
  `disposicion` (si el botón va en fila densa) y `nota` (por qué se aceptó esa talla)—.
  Pegar la salida del `--json` los borra en silencio y el test sigue verde.

Regla: `grep -c writeFileSync <generador>`. Si es 0, el fichero es una decisión, no una
salida: mueve `fichero`/`linea` de las entradas afectadas y conserva el resto, añadiendo a
`nota` por qué se movió. Ver [[trinquete-baseline-bloquea-solo-lo-nuevo-patron-reusable]] · [[facturaia]]
