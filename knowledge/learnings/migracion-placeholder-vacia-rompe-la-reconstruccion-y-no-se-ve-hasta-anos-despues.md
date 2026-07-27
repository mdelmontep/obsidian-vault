---
title: una migración placeholder vacía rompe la reconstrucción y no se ve hasta años después
date: 2026-07-27
source: claude-code-session
tags: [supabase, migraciones, deuda, facturaia]
---

`418_ingesta_routing_rules.sql` contenía literalmente `-- Actual content was applied via remote; no-op
here.`: la tabla se creó a mano en producción y el fichero solo existía para cuadrar
`schema_migrations`. Prod funcionaba, así que nadie lo notó. **123 migraciones después**, la `541` hace
`alter policy … on public.ingesta_routing_rules` y revienta con `relation does not exist` en cualquier
entorno que no sea prod, tumbando todo lo que venga detrás. Salió al migrar un sandbox con 319
migraciones de retraso, o sea con prisa.

- El daño de saltarse "todo cambio de schema va al repo" **no aparece al saltárselo**, aparece cuando
  alguien intenta levantar un entorno nuevo. Y entonces ya son varios agujeros a la vez.
- Reconstruir el DDL "de memoria" o desde los tipos generados **no vale**: la versión inferida desde
  `database.types.ts` no llevaba ninguna de las 9 constraints ni los 2 índices únicos parciales.
  Volcarlo de prod: `information_schema.columns`, `pg_indexes`, `pg_get_constraintdef`, `pg_policies`,
  `pg_get_functiondef`.
- Detector barato: `grep -rl "Applied directly on remote" supabase/migrations/`, y revisar los huecos de
  numeración uno a uno — un hueco puede ser un número quemado o SQL que nadie escribió.
- **No está cerrado hasta que la reconstrucción se prueba** en un proyecto vacío sin tocar nada a mano.

Ver [[db-push-remote-versions-not-found-es-checkout-stale-o-num-duplicado-no-repair]] · [[facturaia]]
