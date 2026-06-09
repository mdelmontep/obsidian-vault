---
title: profiles pk es user_id, no id — fk en migraciones
date: 2026-06-09
source: claude-code-session
tags: [supabase, migraciones, facturaia, schema]
---

La tabla `public.profiles` de TuFacturaIA usa `user_id` como PK, no `id`.

Al escribir una FK hacia profiles desde otra tabla, usar:
```sql
REFERENCES public.profiles(user_id) ON DELETE SET NULL
```

El error en el dashboard si se omite la columna: `ERROR: 42703: column "id" referenced in foreign key constraint does not exist`.

Aplica también a políticas RLS y joins: `p.user_id`, nunca `p.id`.
