---
title: migration con NOT NULL — secuencia ADD nullable, UPDATE backfill, SET NOT NULL
date: 2026-05-05
source: claude-code-session
tags: [postgres, migrations, schema]
---

Añadir una columna NOT NULL a tabla con datos preexistentes en un solo paso falla — Postgres no sabe qué valor poner para las filas viejas.

Patrón en una sola migration (atómica, sin riesgo de filas con NULL coladas):

```sql
-- 1. Nullable
ALTER TABLE x ADD COLUMN created_via text CHECK (created_via IN (...));

-- 2. Backfill desde otras columnas con CASE
UPDATE x SET created_via = CASE
  WHEN fuente = 'api' THEN 'api'
  WHEN generado_por_voz THEN 'voice'
  ELSE 'web'
END WHERE created_via IS NULL;

-- 3. NOT NULL al final = disciplina futura
ALTER TABLE x ALTER COLUMN created_via SET NOT NULL;
```

Si dejas el SET NOT NULL para "después", las escrituras nuevas se cuelan con NULL antes de que apliques el segundo migration. Romper la disciplina invisiblemente. Hacerlo todo junto.
