---
title: "levantar Supabase local en FacturaIA: sin config.toml, puertos 544xx, analytics off, dup 519"
date: 2026-07-21
source: claude-code-session
tags: [supabase, local, testing, docker]
---
El repo NO commitea `supabase/config.toml`, así que los tests de integración (`vitest.integration.config.ts`, `it.skipIf` sin envs) no corren de fábrica. Para verificar SQL/RPCs contra BD real (lo correcto en cambios fiscales) hay que levantarlo a mano:

1. `supabase init` (crea `config.toml`; NO commitear).
2. Suele haber otro stack corriendo (proyecto "app") ocupando 543xx → cambia todos los puertos a 544xx: `sed -i.bak -E 's/5432([0-9])/5442\1/g' supabase/config.toml`.
3. `[analytics] enabled = false` — el contenedor `vector` falla en Colima ("docker.sock operation not supported") y aborta el start.
4. Duplicado de nº de migración (p.ej. `519`) rompe el `db reset` con "duplicate key ... version 519": renombra local el orphan a un nº libre (revertir después) — ver [[db-push-remote-versions-not-found-es-checkout-stale-o-num-duplicado-no-repair]].
5. `supabase start` → coge `SUPABASE_LOCAL_URL`/service key de `supabase status -o env` → `SUPABASE_LOCAL_URL=.. SUPABASE_LOCAL_SERVICE_KEY=.. npx vitest run --config vitest.integration.config.ts <archivos>`.
6. `supabase stop` + borra `config.toml`/`.bak`/artefactos (no commitear nada de esto).

Los puertos Postgres directos (5432/6543) a veces están bloqueados desde la Mac, pero `db push --db-url` y el stack local por 54321 conectan igual. [[facturaia]]
