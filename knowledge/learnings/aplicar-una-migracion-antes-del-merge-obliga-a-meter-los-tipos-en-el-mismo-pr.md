---
title: aplicar una migración antes del merge obliga a meter los tipos en el mismo pr
date: 2026-10-17
source: facturaia (migs 1085 y 1086, PRs #3655 y #3651)
tags: [supabase, gen-types, merge, facturaia]
---
- **Qué pasa:** la regla es aplicar a prod antes de mergear. Desde ese momento `gen:types:check` compara el esquema de prod con `database.types.ts` de main, y se pone en rojo en TODAS las ramas abiertas, no solo en la tuya.
- **Fix:** regenerar los tipos justo después del `db push` (`npm run gen:types -- --proyecto-comun` desde el worktree) y commitearlos en el mismo PR de la migración. Ese PR se mergea el primero del tren; el resto, después, con `merge origin/main`.
- **Si la migración ya entró sin tipos:** un PR solo de tipos (como el #3655), y se mergea antes que nada.
- **Tell:** un `gen:types:check` rojo en una rama sin migraciones es que otro aplicó la suya.
- Relacionado: [[set-role-dentro-de-una-migracion-rompe-el-db-push-de-prod]]
