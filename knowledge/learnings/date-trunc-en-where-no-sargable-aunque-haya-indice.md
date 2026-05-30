---
title: date_trunc en WHERE no es sargable aunque haya índice
date: 2026-05-29
source: facturaia mig 181 — get_org_usage seq scan en bandeja_ingesta
tags: [postgres, performance, sargabilidad, indices]
---

`WHERE date_trunc('month', col) = date_trunc('month', now())` **no usa** el índice `(otra_col, col)` aunque exista — Postgres requiere columna desnuda en el lado izquierdo del operador para que el predicado sea sargable. Cae a seq scan que crece linealmente con la tabla.

Fix sin índice nuevo: reescribir con range explícito y los mismos límites lógicos.

```sql
-- antes (seq scan)
WHERE org_id = X AND date_trunc('month', created_at) = date_trunc('month', now())

-- después (index range scan sobre (org_id, created_at))
WHERE org_id = X
  AND created_at >= date_trunc('month', now())
  AND created_at <  date_trunc('month', now()) + interval '1 month'
```

Identidad lógica: `date_trunc('month', x)` es monótona — `date_trunc('month', x) = M ⟺ M ≤ x < M + 1 month`. Mismo conjunto, ahora con index scan.

Aplica también a `date(col) = '2026-05-01'`, `extract(year from col) = 2026`, `lower(col) = 'x'` (este último necesita índice funcional o cambiar a citext).

Alternativa si no puedes reescribir el predicado: índice funcional `CREATE INDEX ... ON tabla ((date_trunc('month', col)))`. Más overhead que reescribir.

[[supabase-migration-new-rompe-secuencia-nnn-name]] [[migracion-aplicada-fuera-de-historial-supabase]]
