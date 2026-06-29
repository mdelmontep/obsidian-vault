---
title: supabase check constraint — insertar valor no permitido → 23514 no 23505
date: 2026-06-30
source: claude-code-session
tags: [supabase, postgres, cobros, errores]
---

Insertar `triggered_by: 'copiloto'` en `cobros_recordatorios` lanzó `23514` (check_violation),
no `23505` (unique_violation). El código manejaba solo `23505` → cayó en el branch genérico
de error y no enviaba ningún email. Ningún log lo decía claramente.

**Valores permitidos** (mig 065): `triggered_by IN ('cron', 'manual')`.

**Fix**: usar `'manual'` para invocaciones desde copiloto/UI.

**Patrón**: antes de insertar un string en columna con CHECK enum, grep la migración:
`grep -n "triggered_by\|CHECK" supabase/migrations/*.sql`

Aplica a: `cobros_recordatorios.triggered_by`, `facturas.fuente` (CHECK propio).
