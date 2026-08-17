---
title: en supabase gestionado, postgres no puede el grant de storage pero sí crear sus políticas
date: 2026-08-17
source: claude-code-session
tags: [supabase, storage, rls, migraciones, postgres]
---

`storage.objects` lo posee `supabase_storage_admin`, y `postgres` **no** es miembro:
`grant supabase_storage_admin to postgres` da `42501: role memberships are reserved, only
superusers can grant them` — por Management API **y por el SQL Editor de la consola**, que
corre con el mismo rol. Eso es cierto y no se arregla.

**Lo que NO se deduce de ahí: `create policy … on storage.objects` SÍ funciona como
`postgres`, y `insert into storage.buckets` también.** Son sentencias distintas con
requisitos distintos. En TuCRMIA esa deducción bloqueó una épica **once días** y generó un
ticket a soporte que no hacía falta.

Lo que sí exige pertenencia es el `set local role <dueño>` que se suele copiar delante del
bloque: quítalo y las políticas se crean igual.

Sonda no destructiva para medirlo en un minuto (crea y revierte en la misma transacción):

```sql
do $$ begin
  create policy sonda on storage.objects for select to authenticated using (false);
  raise exception 'SI_PUEDE (revertido a propósito)';
end $$;
```

Ver [[un-guard-que-mide-un-sustituto-bloquea-sin-que-nadie-pruebe-el-hecho]].
