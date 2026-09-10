---
title: el auth.uid() de supabase autohospedado solo lee el GUC legacy
date: 2026-09-10
source: mandadm
tags: [supabase, postgrest, rls, autohospedado]
---
El `auth.uid()` que trae `supabase/postgres` es, literalmente,
`select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid` — **solo la forma legacy**.

PostgREST con `PGRST_DB_USE_LEGACY_GUCS: "false"` pone `request.jwt.claims` (un JSON), no
`request.jwt.claim.sub`. Con esa combinación `auth.uid()` devuelve **NULL en cada política**: cero
filas para todo el mundo. La RLS *parece* funcionar —no se escapa un solo dato— y en realidad no
está filtrando nada, está negando todo. Un panel vacío se lee como «aún no hay datos».

Fix: `PGRST_DB_USE_LEGACY_GUCS: "true"` en el autohospedado, y comprobar que coincide con lo que
ponga el código que abre conexiones `pg` crudas por su cuenta (en mandadm,
`client-user.ts` hace `set_config('request.jwt.claim.sub', …)`): **una sola convención de GUC en
todo el sistema**.

Cómo verlo en 10 s: `select prosrc from pg_proc p join pg_namespace n on n.oid=p.pronamespace
where n.nspname='auth' and p.proname='uid'`.
Ver [[montar-la-carpeta-de-init-tapa-el-bootstrap-de-la-imagen]]
