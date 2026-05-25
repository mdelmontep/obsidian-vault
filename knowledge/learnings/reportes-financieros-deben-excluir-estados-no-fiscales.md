---
title: reportes financieros deben excluir estados no-fiscales
date: 2026-05-07
source: claude-code-session
tags: [billing, fiscal, supabase, agentesia]
---

Bug fiscal real: modelo 303 de IVA + dashboard de cashflow + KPIs sumaban TODAS las facturas sin filtrar estado. Borradores (no son fiscales) inflaban IVA repercutido. Anuladas se compensaban con su abono pero solo si ambos en el mismo periodo.

Regla: cualquier query agregada (sum, count) sobre facturas debe filtrar:

```sql
-- emitidas
WHERE estado NOT IN ('borrador', 'anulada')
-- recibidas (TuFacturaIA)
WHERE estado NOT IN ('sin_aprobar', 'disputada')
```

Aplica a: KPI dashboard, modelo 303, exportaciones CSV, gráficos cashflow, métricas módulos. Si declaras a Hacienda con borradores contando, el modelo 303 sale mal.

Detección: revisar cualquier `.reduce((s, f) => s + f.total)` o `.from('facturas').select('count')` en el codebase.
