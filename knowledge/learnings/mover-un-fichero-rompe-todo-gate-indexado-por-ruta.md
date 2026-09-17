---
title: mover un fichero rompe todo gate indexado por ruta, y hay que probar que la deuda no crece
date: 2026-08-09
updated: 2026-09-18
source: claude-code-session
tags: [gates, refactor, baseline, facturaia]
---

Al partir un fichero grande, su deuda medida **viaja a rutas nuevas que nacen con cap 0** y los trinquetes bloquean el commit. Pasó en los tres splits de la tanda con: `.inline-style-baseline.json`, `.design-debt-baseline.json` y el censo `tap-target-inventario.json`.

Antes de reasentar ningún baseline, **demuestra que la deuda SE MUEVE y no crece**: suma la métrica en el fichero original (desde `git show HEAD:<fichero>`) y compárala con la suma de original + piezas nuevas. Si el total es idéntico, reasentar es contabilidad; si sube, es una subida disfrazada de refactor.

Dos trampas propias del reasentado:
- Un censo con etiquetas repetidas en varios ficheros (`"Eliminar línea"`) no se reapunta por nombre: hay que cruzar contra el censo vivo y **exigir un único candidato** dentro del `_parts/` nuevo, o acabas moviendo entradas legítimas de otros ficheros.
- Correr solo los tests del dominio tocado no basta: el censo de tap-targets vive en `scripts/__tests__/`. Un split dejó `main` en rojo un rato por eso.

**Y no solo los baselines numéricos: también las LISTAS DE EXCEPCIONES por ruta.** 18-sep-2026, facturaia #2779: extraer un emisor de `system_alerts` a `_parts/` dejó su entrada de `SIN_RESOLVEDOR` apuntando a un fichero que ya no emite, así que el guard dejó de vigilar al emisor real. Lo cazó el **test gemelo** del propio guard —«la lista de excepciones no arrastra entradas muertas»—, que es la pieza que hay que escribir siempre al lado de una lista así: sin él, una excepción sobrevive a su motivo y tapa el siguiente caso real en silencio. Corolario medido el mismo día: correr los tests de las carpetas del PR daba verde; lo vio el gate entero.

Ver [[trinquete-indexado-por-ruta-se-rompe-al-mover-ficheros]] si existe, y el aviso de `dependency-map.md` sobre índices por path.
