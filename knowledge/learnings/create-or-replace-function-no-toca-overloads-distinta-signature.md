---
title: create or replace function no toca overloads con signature distinta
date: 2026-05-21
source: claude-code-session
tags: [postgres, supabase, migrations]
---

Postgres identifica funciones por `(schema, name, args)`. `CREATE OR REPLACE FUNCTION` solo afecta la firma idéntica — si recreas con args distintos, la vieja queda huérfana coexistiendo en BD.

Caso real FacturaIA: `convertir_presupuesto_a_factura` creada en mig 036 con `(uuid, uuid)`, recreada en migs 082/084/088/119 con `(uuid, uuid, text, uuid, uuid)`. La 2-args sobrevivió 6 migs hasta detectarse durante smoke mig 119. Riesgo: callers olvidados usando la firma vieja con lógica desactualizada.

Patrón: tras refactor de firma, añadir `DROP FUNCTION IF EXISTS public.X(args_viejos)` explícito en la misma migración. Args exactos importan — Postgres usa identity arguments para resolver.

Verificar antes/después:
```sql
SELECT pg_get_function_identity_arguments(oid)
FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
WHERE n.nspname='public' AND p.proname='X';
```

Si tu migración recrea por refactor, añadir DO block con assert post-drop que cuente firmas esperadas (count=1) y huérfanas (count=0). Falla la transacción si quedó algo.
