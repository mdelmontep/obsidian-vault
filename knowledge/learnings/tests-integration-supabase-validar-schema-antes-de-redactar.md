---
title: tests integration supabase validar schema antes de redactar
date: 2026-05-07
source: claude-code-session
tags: [tests, supabase, ci]
---

Escribir tests de integración con Supabase real sin verificar el schema → cascada de fixes en CI. Sesión real: 6 iteraciones por inventar campos:

- `slug`, `is_test` (no existían en organizations)
- `siguiente` (real: `contador_actual`)
- `iva` (real: `iva_pct`)
- `created_via` NOT NULL CHECK (faltaba en insert)
- parámetro RPC `p_codigo` (real: `p_serie_codigo`)
- RPC devolvía TEXT formateado, no INTEGER (parseado mal)

Regla: antes del primer commit del test:

```bash
grep -A 30 "CREATE TABLE.* X " supabase/migrations/001_schema.sql
# o
SELECT column_name, data_type, is_nullable
FROM information_schema.columns WHERE table_name='X';
```

Y mirar la firma exacta del RPC (`grep -A 10 "CREATE.*FUNCTION.*nombre"`). Cada iteración CI cuesta ~3-4 min de docker pull supabase.
