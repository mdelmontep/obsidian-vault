---
title: in (select func()) fuerza seq scan en postgres; = any(array(...)) usa índice (initplan)
date: 2026-07-21
source: claude-code-session
tags: [postgres, supabase, rls, performance]
---
`col IN (SELECT set_returning_func(x))` impide usar el índice sobre `col`: el planner hace Seq Scan de la tabla entera + Hash Join contra el conjunto. Caso real FacturaIA: `get_org_usage` con `org_id IN (SELECT org_billing_group(p_org_id))` = 22% del tiempo de BD, Seq Scan de `facturas` en cada llamada.

Fix: materializar en array y usar `col = ANY(array(SELECT func(x)))` → InitPlan (se evalúa una vez), Index Scan. Medido 567ms→105ms.

Mismo mecanismo (InitPlan) que el truco de RLS de Supabase: envolver funciones de CERO argumentos / constantes-por-statement en `(select f())` (`auth.uid()`, `get_user_org_id()`) para no reevaluarlas por fila. Dos gotchas no obvios: (1) el linter `auth_rls_initplan` NO detecta funciones propias tipo `get_user_org_id()` — hay que buscarlas a mano (grep pg_policies); (2) NUNCA envolver funciones que reciben la columna de la fila (`is_billing_readonly(org_id)`) → serían subconsultas correlacionadas.

Verificar equivalencia por round-trip: quitar los wraps del resultado debe reproducir el original byte a byte (0 mismatch en USING y WITH CHECK) → prueba que solo cambia el plan, no la semántica (ni fuga cross-org en RLS).
