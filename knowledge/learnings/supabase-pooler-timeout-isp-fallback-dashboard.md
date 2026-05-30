---
title: supabase pooler :5432/:6543 timeout desde ISP — fallback dashboard sql editor
date: 2026-05-30
source: claude-code-session
tags: [supabase, postgres, network, migrations, gotcha]
---

`supabase db push --linked` cuelga en `Initialising login role...` o falla con `dial tcp <ip>:5432 i/o timeout` desde ciertas redes ISP españolas (movistar, fibras compartidas hoteles, wifi cafeterías). Ambos puertos `:5432` (session) y `:6543` (transaction pooler) bloqueados a AWS Dublin.

**Fix sin esperar red**:
1. Dashboard SQL Editor → pegar contenido de la mig → Run.
2. Registrar la mig como aplicada para que el CLI no la reintente:
   ```sql
   insert into supabase_migrations.schema_migrations (version, name)
   values ('NNN', 'nombre_sin_extension') on conflict (version) do nothing;
   ```
3. Verificar con `select version from supabase_migrations.schema_migrations order by version desc limit 5;`

NUNCA editar `schema_migrations` sin `on conflict do nothing` — un INSERT crudo con version duplicada rompe `supabase migration repair`.

**Alternativa**: tetherear móvil (datos no bloquean 5432) y reintentar `supabase db push --linked` normal.

Ver [[campo-huerfano-shape-sin-migracion-paralela]] (caso típico que pide push urgente).
