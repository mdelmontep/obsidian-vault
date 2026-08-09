---
title: mover un fichero rompe todo gate indexado por ruta, y hay que probar que la deuda no crece
date: 2026-08-09
source: claude-code-session
tags: [gates, refactor, baseline, facturaia]
---

Al partir un fichero grande, su deuda medida **viaja a rutas nuevas que nacen con cap 0** y los trinquetes bloquean el commit. Pasó en los tres splits de la tanda con: `.inline-style-baseline.json`, `.design-debt-baseline.json` y el censo `tap-target-inventario.json`.

Antes de reasentar ningún baseline, **demuestra que la deuda SE MUEVE y no crece**: suma la métrica en el fichero original (desde `git show HEAD:<fichero>`) y compárala con la suma de original + piezas nuevas. Si el total es idéntico, reasentar es contabilidad; si sube, es una subida disfrazada de refactor.

Dos trampas propias del reasentado:
- Un censo con etiquetas repetidas en varios ficheros (`"Eliminar línea"`) no se reapunta por nombre: hay que cruzar contra el censo vivo y **exigir un único candidato** dentro del `_parts/` nuevo, o acabas moviendo entradas legítimas de otros ficheros.
- Correr solo los tests del dominio tocado no basta: el censo de tap-targets vive en `scripts/__tests__/`. Un split dejó `main` en rojo un rato por eso.

Ver [[trinquete-indexado-por-ruta-se-rompe-al-mover-ficheros]] si existe, y el aviso de `dependency-map.md` sobre índices por path.
