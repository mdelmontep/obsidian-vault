---
title: tests de integración Postgres que se autosaltan sin DB → levantar pgvector local, no postgres pelado
date: 2026-07-03
source: claude-code-session
tags: [testing, postgres, docker, ci]
---

Suites con tests `*.pg.test.ts` que hacen `try { SELECT 1; applySchema } catch { skip }`
pasan en VERDE sin DB porque se autosaltan — engañoso: crees que validaste el cambio de
schema/SQL y esos tests ni corrieron. Para validarlos de verdad, levantar la DB local con
las creds exactas que espera el test (leer el default de `DATABASE_URL` en el fichero).

Gotcha: si el `schema.sql` usa `CREATE EXTENSION vector` (pgvector para RAG), `postgres:16`
pelado falla con `extension "vector" is not available` (que el catch traga como "no
disponible"). Usar la imagen `pgvector/pgvector:pg16`:

`docker run -d --name test-pg -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=<db> -p 5433:5432 pgvector/pgvector:pg16`

Luego `DATABASE_URL=postgres://user:pass@localhost:5433/<db> npm test`. Relacionado:
[[vitest-fileparallelism-false-tests-integracion-bd-compartida]].
