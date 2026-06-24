---
title: aplicar migración a prod con db push --db-url (worktree sin link / --linked colgado)
date: 2026-06-25
source: claude-code-session
tags: [supabase, migraciones, facturaia, deploy]
---

`supabase db push --linked` falla/se cuelga si el worktree no está linkado
(`Cannot find project ref`) o si el pre-push lanza `supabase migration list --linked`
y se queda sin red/sin TTY. Alternativa limpia (NO es SQL directo — actualiza
`schema_migrations`):

1. `supabase db push --db-url "$(grep '^SUPABASE_DB_URL=' .env.local | cut -d= -f2-)" --dry-run`
   → lista lo pendiente sin aplicar. Confirma que SOLO sale tu migración.
2. quitar `--dry-run` para aplicar.

Por qué importa: el dev server usa `.env.local` → **Supabase de PROD** (no hay BD de
test separada con el schema). Una feature con migración nueva da **500 en localhost**
hasta el `db push`; y el flujo que muta (p.ej. importar devoluciones) toca prod →
hazlo solo en org `is_test`. Orden correcto: merge → `db push` desde main → QA.
Ver [[migracion-aplicada-fuera-de-historial-supabase]] · [[verificacion-no-mutar-estado-prod-cuenta-real]].
