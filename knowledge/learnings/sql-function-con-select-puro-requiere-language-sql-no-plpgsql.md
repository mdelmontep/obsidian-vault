---
title: sql function con select puro requiere language sql no plpgsql
date: 2026-04-21
source: claude-code-session
tags: [postgresql, supabase, sql]
---

Si el body de una función PostgreSQL es un SELECT directo (sin `BEGIN`/`END`/`RETURN`), debe declararse como `LANGUAGE sql`, no `LANGUAGE plpgsql`.

Con `plpgsql`, PostgreSQL espera un bloque procedural y falla con:

```
ERROR: syntax error at or near "SELECT"
```

Ejemplo correcto:

```sql
CREATE OR REPLACE FUNCTION admin_dashboard_stats()
RETURNS JSONB AS $$
  SELECT jsonb_build_object(
    'total_orgs', (SELECT COUNT(*) FROM organizations),
    'mrr', (SELECT COALESCE(SUM(p.precio_mes), 0) FROM organizations o JOIN plans p ON o.plan = p.id WHERE o.billing_status = 'active')
  );
$$ LANGUAGE sql SECURITY DEFINER;
```

Si necesitas variables, control de flujo o `RAISE`, entonces sí usa `plpgsql` con `BEGIN ... RETURN ... END;`.
