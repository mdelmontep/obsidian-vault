---
title: supabase db push aplica todas las migraciones pendientes, aparta las ajenas antes
date: 2026-07-01
source: claude-code-session
tags: [supabase, migrations, git-worktree]
---

`supabase db push --linked` aplica **todas** las migraciones locales pendientes en
`supabase/migrations/` en orden numérico, sin selección — no hay flag para "aplica solo
esta". Si trabajas en el mismo repo que otra sesión/rama en paralelo y ella tiene una
migración sin commitear con número posterior al hueco que vas a usar tú, un push normal
también la sube a prod sin que tú la hayas validado.

Fix (caso real, TuFacturaIA 2026-07-01, migraciones 421-424 con 3 sesiones a la vez):
1. `mv supabase/migrations/<NNN_ajena>.sql /tmp/` (apartarla, no tocar su contenido)
2. `supabase db push --linked` — el prompt de confirmación solo lista la(s) tuya(s)
3. `mv /tmp/<NNN_ajena>.sql supabase/migrations/` (devolverla a su sitio intacta)

Verificar antes con `supabase migration list --linked` qué hay pendiente y de quién es cada
archivo (`git status` — si es `??` y no la creaste tú esta sesión, es ajena).
