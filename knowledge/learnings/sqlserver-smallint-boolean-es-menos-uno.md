---
title: columnas smallint usadas como boolean en SQL Server legado son -1=true, no 1
date: 2026-07-21
source: claude-code-session
tags: [sql-server, etl, legacy]
---
En ERPs legado sobre SQL Server, columnas `smallint`/`tinyint` reutilizadas como boolean (ej. `es_instalador`, `eliminado`) suelen venir de VB6/Access clásico, donde `True` se serializa como **-1**, no `1`. Un filtro `WHERE flag=1` da 0 filas silenciosamente aunque el dato "activo" exista y sea mayoritario.

Fix: comprobar la distribución real (`GROUP BY flag`) antes de asumir 0/1 — si aparece `-1` junto a `0`, ese es el true/false real. Aplica también a "boolean-alike" derivados de un cálculo (ej. `cobro`/`parapedir` en wapi) donde el signo, no el valor, codifica el flag.
