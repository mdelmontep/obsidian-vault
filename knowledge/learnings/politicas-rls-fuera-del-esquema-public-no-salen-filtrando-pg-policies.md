---
title: auditar quién usa una función filtrando pg_policies por schemaname='public' te deja ciego a storage
date: 2026-08-12
source: claude-code-session
tags: [supabase, postgres, rls, storage, seguridad]
---

Al decidir si se puede revocar `EXECUTE` de una función helper, la pregunta que
manda es «¿la usa alguna política RLS?». La consulta natural es sobre
`pg_policies`, y ahí es donde se cuela el error: filtrar por
`schemaname = 'public'`.

**Las políticas de Supabase Storage viven en `storage.objects`, no en `public`.**
En FacturaIA (11-ago) `user_active_org_ids()` salía con 0 políticas y aspecto de
huérfana; sostenía **6 políticas de `storage.objects`**. Revocarla habría roto la
subida de logos y documentos desde el navegador, y el fallo habría aparecido en
cara del cliente, no en un test.

Sin filtro de esquema, y agrupando para ver dónde:

```sql
select count(*) filter (where schemaname <> 'public') as fuera_de_public,
       string_agg(distinct schemaname||'.'||tablename, ', ')
         filter (where schemaname <> 'public') as donde
  from pg_policies
 where coalesce(qual,'')||' '||coalesce(with_check,'') like '%mi_funcion(%';
```

Corolario: un gate que solo comprueba «¿sobra alguna función expuesta?» no ve
este fallo. Hay que medir **las dos direcciones** — que las excepciones legítimas
SIGUEN accesibles. Ver [[supabase-rpc-security-definer-execute-public]].
