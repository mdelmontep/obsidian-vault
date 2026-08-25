---
title: conflicto de rebase entre 2 PRs que añaden columnas distintas a la misma tabla se resuelve aditivo
date: 2026-07-11
source: claude-code-session
tags: [git, postgres, migraciones, conflictos]
---

Dos PRs en paralelo añaden cada una una migración `ALTER TABLE ... ADD COLUMN` distinta sobre la
MISMA tabla (p. ej. `conversation_state`). Al rebasar la segunda sobre la primera ya mergeada,
conflicto real en: el store/tipo que lee la fila (interfaz + SELECT + INSERT/ON CONFLICT), el
bloque `schema.sql` (drift-gate), y cualquier test que las toque cerca.

Resolución correcta: **mantener AMBOS lados completos** (las dos columnas en la interfaz/SELECT/
INSERT, los dos bloques ALTER en schema.sql, los dos tests) — nunca "elegir un lado". Tras
resolver, re-correr drift-gate (`schema.sql` vs `baseline.sql`+migraciones con las DOS
migraciones aplicadas) para confirmar que sigue convergiendo antes de mergear la segunda PR.

**Matiz que cuesta caro (31-jul): «aditivo» describe el CONTENIDO, no los LÍMITES del conflicto.**
Comprobar que los dos lados no se solapan NO autoriza a automatizar la resolución quitando los
marcadores con un script: git corta donde diverge el texto, no en fronteras sintácticas, y un hunk
que parte por la mitad de una función deja la llave de cierre en el lado descartado. El resultado no
compila, así que **ningún test lo ve** (la suite ni carga el módulo); lo caza `lint`. Regla: tras
resolver cualquier conflicto en código, `npx tsc --noEmit` **antes** de `git rebase --continue`.
Regenerar sí vale para derivados (ver [[conflicto-rebase-json-generado-regenerar-no-mergear-a-mano]]);
la confianza que da ahí no se traslada al código.
