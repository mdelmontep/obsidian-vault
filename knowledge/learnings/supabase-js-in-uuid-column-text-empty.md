---
title: supabase-js .in() sobre columna UUID con array text puede devolver vacío silenciosamente
date: 2026-06-09
source: claude-code-session
tags: [supabase, postgrest, uuid, join, rpc]
---

## Qué pasa

`.from('organizations').select('id, nombre').in('id', text_uuid_array)` devuelve `data: []` sin error, aunque:
- El cliente usa `service_role` (bypass RLS garantizado)
- La misma query con psql directo devuelve los datos correctos
- Los UUIDs en el array sí existen en la tabla

## Root cause

No confirmada. Hipótesis más probable: coerción `text → UUID` en la capa PostgREST falla silenciosamente en alguna combinación de versión/config.

## Fix / patrón

Mover el JOIN a SQL directamente en la función RPC (SECURITY DEFINER). El JOIN en PostgreSQL no tiene el problema de coerción:

```sql
-- Añadir el campo directamente en la función
LEFT JOIN public.organizations o ON o.id::text = sub.folder
```

El resultado llega junto con los datos de storage; la app no necesita hacer join.

## Caso real

mig 236 TuFacturaIA: `storage_usage_by_org()` ampliada con `org_nombre` vía LEFT JOIN. Panel admin `/admin/system?tab=storage` mostraba "— sin nombre" para todas las orgs hasta el fix.
