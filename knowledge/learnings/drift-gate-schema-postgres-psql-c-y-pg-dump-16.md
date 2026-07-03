---
title: gate de drift de schema postgres — gotchas de psql -c y pg_dump ≥16
date: 2026-07-03
source: claude-code-session
tags: [postgres, migraciones, ci]
---
Al montar un gate que compara dos schemas por dump (p. ej. probar que `schema.sql` == baseline+migraciones):

- **`DROP/CREATE DATABASE` NO caben en un solo `psql -c 'a; b'`**: varias sentencias en un `-c` van en transacción implícita → `ERROR: cannot run inside a transaction block`. Un `-c` por sentencia (cada una es query autónoma, autocommit) o pipe por stdin (cada `;` se envía por separado).
- **`pg_dump` ≥16 emite `\restrict <token>` / `\unrestrict <token>` con token ALEATORIO por ejecución** (endurecimiento anti-inyección de psql). Si no se filtran, dos dumps idénticos difieren siempre → drift falso. Añadir `^\\restrict|^\\unrestrict` al filtro.
- **`pg_dump` del host se niega a volcar de un server de versión MAYOR** (`server version mismatch`) → corre `pg_dump`/`psql` DENTRO del contenedor (`docker compose exec -T postgres`) para paridad de versión.
- Comparación: `pg_dump --schema-only --no-owner --no-privileges --no-comments --schema=public --exclude-table=<control>` + `grep -Ev '^(--|SET |SELECT pg_catalog\.set_config|\\restrict |\\unrestrict |$)'` en ambos, `diff`.
- Para que dos caminos converjan en el dump: **nombrar constraints explícitamente** en ambos lados (un CHECK/FK anónimo recibe nombre autogenerado que diverge del ALTER) y **columnas nuevas al final** (ADD COLUMN las deja al final; el orden no se normaliza).
