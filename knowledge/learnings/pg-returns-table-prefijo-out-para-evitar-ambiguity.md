---
title: PG function RETURNS TABLE con SELECT INTO → prefijo out_ para evitar ambiguity
date: 2026-05-21
source: claude-code-session
tags: [postgres, supabase, migrations, sql]
---

`CREATE FUNCTION x() RETURNS TABLE (factura_id UUID, ...)` colisiona con `SELECT factura_id INTO v_local FROM facturas` dentro de la misma función → error `column reference "factura_id" is ambiguous` al INVOCAR (no al CREATE).

Solución: prefijar columnas OUT con `out_*`:
```sql
RETURNS TABLE (out_factura_id UUID, out_factura_num TEXT, ...)
```

Caller TS/JS lee `result.out_factura_id` (Supabase RPC devuelve nombres declarados).

Gotcha grave: si fixeas en prod sin alinear el archivo de migración, `supabase db reset` o staging fresh recrean la función SIN prefijo → endpoint que lee `out_*` recibe `undefined`. Drift silencioso.

**Regla**: tras cualquier `CREATE OR REPLACE FUNCTION` aplicado directo en prod por hotfix, alinear archivo migración inmediatamente. Test de regresión: asertar que el JSON response del endpoint contiene las keys esperadas + assertion explícita "no `out_*` keys leaked".

Caso real: mig 131 `desvincular_asignacion` (2026-05-21) — primera version sin prefijo crasheó ambiguity, fix 131c con prefijo en prod, archivo desincronizado hasta PR #69.
