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
