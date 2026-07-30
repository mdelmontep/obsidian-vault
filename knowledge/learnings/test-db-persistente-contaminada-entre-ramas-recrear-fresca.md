---
title: bd de test persistente contaminada entre ramas → recrear fresca antes del gate
date: 2026-07-05
source: claude-code-session
tags: [postgres, testing, migrations, gotcha, claude-code]
---
Una BD de test local persistente (contenedor Docker) CONSERVA el schema entre cambios de rama. Si saltas a una rama que NO tiene la migración X, pero la BD sigue con la tabla de X (aplicada desde otra rama), los tests `.pg` / de drift / de "completeness de tablas" fallan **atribuyéndolo a TU cambio** — pero es contaminación de la BD, no un bug del diff.

Síntoma real (AGH, 2×): rama sin la mig 0004 contra `agh_dev` que aún tenía `contacts` → `reset-completeness.pg.test.ts` falla «tabla `contacts` sin clasificar»; 20 fallos `.pg` que no tocaban nada del diff.

Fix: recrear la BD **fresca ANTES del gate en cada rama** (los tests auto-migran al estado de esa rama):
`docker exec pg psql -U u -d postgres -c "DROP DATABASE IF EXISTS db WITH (FORCE);"` → `CREATE DATABASE db;` → `CREATE EXTENSION IF NOT EXISTS vector;`. Una sentencia por `-c` (DROP/CREATE no van juntas en un `-c`).

**La variante inversa, y es la que más despista** (2026-07-30, AGH): la BD local se queda **POR
DETRÁS** de `main`. Tras semanas sin migrarla estaba en la 0023; `main` iba por la 0027 → los `.pg`
del dashboard reventaban con **500** porque una columna nueva no existía, con un diff que solo tocaba
un fichero del agente. Clave: `applySchema` (el `CREATE TABLE IF NOT EXISTS` del schema) **NO añade
columnas a tablas que ya existen** — solo las migraciones lo hacen. Fix: `npm run db:migrate`.

Regla que cubre las dos variantes: si los `.pg` que fallan **no tocan la superficie de tu diff**,
corre ese mismo test desde el checkout en `main` con el mismo `DATABASE_URL` antes de leer el diff.
Si falla igual, no es tuyo — descartarlo cuesta 40 s y me costó un gate entero no hacerlo.

Relacionado: [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] · [[agh-iberica]].
