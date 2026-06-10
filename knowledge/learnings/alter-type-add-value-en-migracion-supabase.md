---
title: extender un enum postgres en migración supabase con ALTER TYPE ADD VALUE
date: 2026-06-10
source: sesión modelo 349 (mig 250 facturaia)
tags: [supabase, postgres, enum, migracion]
---

Para añadir valores a un enum existente en una migración (NO recrear el tipo):

- `ALTER TYPE public.<enum> ADD VALUE IF NOT EXISTS '<valor>';` — idempotente (PG 12+), uno por valor.
- GOTCHA: un valor recién añadido NO es usable hasta el COMMIT. Si la MISMA migración lo USA (insert/CHECK/cast), peta. Solución: pon los `ADD VALUE` AL PRINCIPIO del archivo SUELTOS (sin `BEGIN/COMMIT`, autocommit); el DML que NO referencia el valor nuevo puede ir en su propio `BEGIN`.
- `ADD VALUE` no renombra ni elimina valores. Si necesitas nombres nuevos, añádelos y mapea enum→letra/valor en el código (TS como fuente de verdad), no fuerces el nombre canónico en BD.
- Verifica en prod: `select enumlabel from pg_enum e join pg_type t on t.oid=e.enumtypid where t.typname='<enum>'`.
- Aplicar: `supabase db push --linked` desde un checkout que SÍ contenga la migración; el worktree necesita copiar el link, ver [[worktree-facturaia-build-supabase]]. Distinto del enum-vía-CHECK: ver [[enum-nuevo-en-codigo-sin-ampliar-check-bd-rompe-insert-silencioso]].
