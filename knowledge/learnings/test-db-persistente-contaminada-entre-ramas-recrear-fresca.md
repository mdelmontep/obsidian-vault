---
title: bd de test persistente contaminada entre ramas → recrear fresca antes del gate
date: 2026-07-05
source: claude-code-session
tags: [postgres, testing, migrations, gotcha, claude-code]
---
Una BD de test local persistente (contenedor Docker) CONSERVA el schema entre cambios de rama. Si saltas a una rama que NO tiene la migración X, pero la BD sigue con la tabla de X (aplicada desde otra rama), los tests `.pg` / de drift / de "completeness de tablas" fallan **atribuyéndolo a TU cambio** — pero es contaminación de la BD, no un bug del diff.

Síntoma real (AGH, 2×): rama sin la mig 0004 contra `agh_dev` que aún tenía `contacts` → `reset-completeness.pg.test.ts` falla «tabla `contacts` sin clasificar»; 20 fallos `.pg` que no tocaban nada del diff.

Fix: recrear la BD **fresca ANTES del gate en cada rama** (los tests auto-migran al estado de esa rama):
`docker exec pg psql -U u -d postgres -c "DROP DATABASE IF EXISTS db WITH (FORCE);"` → `CREATE DATABASE db;` → `CREATE EXTENSION IF NOT EXISTS vector;`. Una sentencia por `-c` (DROP/CREATE no van juntas en un `-c`). Relacionado: [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]].
