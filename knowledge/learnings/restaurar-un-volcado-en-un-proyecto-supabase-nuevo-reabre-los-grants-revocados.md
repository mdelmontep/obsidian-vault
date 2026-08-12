---
title: restaurar un volcado en un proyecto supabase nuevo reabre los grants que revocaste
date: 2026-08-12
source: claude-code-session
tags: [supabase, postgres, seguridad, rls, backup, restore]
---
Un proyecto Supabase nuevo trae `ALTER DEFAULT PRIVILEGES ... GRANT ALL ON FUNCTIONS TO anon,
authenticated, service_role` en `public`. `pg_dump` describe los permisos respecto al default de
**Postgres**, no al de Supabase: para una función que en origen es `{postgres, service_role}` emite
`REVOKE ALL ... FROM PUBLIC` + `GRANT ... TO service_role`, y **nunca** `REVOKE ... FROM anon`,
porque en el origen ese grant no existe. En el destino sí — se lo dio el default al crearla.

Resultado medido (TuFacturaIA, 12-ago): la copia restaurada salía con **165 funciones SECURITY
DEFINER invocables por `anon`** y 191 por `authenticated`; el origen, 0 y 0. Restaurar reabría entero
un agujero cross-org cerrado tres semanas antes. Pasa igual con TABLAS (12 con CRUD de más).

Cura: **prevenir, no reparar** — revocar los default privileges del destino ANTES de crear nada. Es
seguro si ningún objeto del origen tiene ACL implícita (compruébalo: `proacl is null` / `relacl is
null` a cero), y el propio volcado restaura los defaults al final. En `scripts/restaurar-copia.sh`.

Ver [[facturaia]] · [[supabase-rpc-security-definer-execute-public]].
