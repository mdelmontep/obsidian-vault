---
title: supabase — borrado masivo por api hace timeout; borrar por lotes con ctid
date: 2026-07-21
source: claude-code-session
tags: [supabase, postgres, migracion]
---
Un `DELETE ... WHERE org_id=X` que arrastra decenas de miles de filas (o cascada a hijos)
por PostgREST / MCP `execute_sql` revienta por timeout del gateway (~pocos segundos), y a
veces hace rollback silencioso (el cliente reporta timeout pero puede haber commiteado o no
— verificar con un `count` después).

Fix: borrar por lotes con `ctid`:
`DELETE FROM tabla WHERE ctid IN (SELECT ctid FROM tabla WHERE org_id=X LIMIT 130000)`,
repitiendo hasta 0. Borrar primero las hijas voluminosas (líneas), luego el padre
(la cascada de padres ya es rápida sin hijas). ~130k filas/lote entran bien.
Guarda de seguridad al limpiar: nunca borrar en una org con `is_test=false`.
