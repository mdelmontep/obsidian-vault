---
title: migraciones incrementales conviviendo con schema.sql idempotente (guards + drift-gate)
date: 2026-07-04
source: claude-code-session
tags: [postgres, migraciones, arquitectura]
---
Para que migraciones versionadas (`NNNN_*.sql` + tabla `schema_migrations`) convivan con un
`schema.sql` idempotente que SIGUE siendo el bootstrap de BD nueva (no congelar el schema):

- Haz las migraciones **guarded** (`ADD COLUMN IF NOT EXISTS`, guard por `pg_constraint` para
  `ADD CONSTRAINT`). En BD nueva (creada por `schema.sql`, que ya lleva el cambio inline) son
  **no-op** y solo se registran; en BD existente aplican el `ALTER`. **Un solo camino de runner**
  (`applySchema → runMigrations`), sin la rama frágil "stampear-sin-correr vs correr".
- Cada cambio vive en DOS sitios (inline en `schema.sql` + la migración) → un **drift-gate** prueba
  que convergen: dos BD limpias (una con `schema.sql`, otra con `baseline.sql` + migraciones),
  `pg_dump` normalizado + `diff`. **Test negativo del gate obligatorio** (un drift deliberado debe
  hacerlo fallar, si no queda verde siempre y nadie se entera).
- Para que el gate no dé falso positivo: **constraints NOMBRADOS en ambos lados** (un CHECK/FK
  anónimo recibe nombre autogenerado que diverge del ALTER) y **columnas nuevas AL FINAL**
  (`ADD COLUMN` las deja al final; el orden no se normaliza).
- Runner: tx por migración con el INSERT de control DENTRO (atómico), advisory lock (deploys
  concurrentes), checksum (migraciones inmutables), forward-only, detección de versión duplicada.
- Gotchas del gate en [[drift-gate-schema-postgres-psql-c-y-pg-dump-16]].
