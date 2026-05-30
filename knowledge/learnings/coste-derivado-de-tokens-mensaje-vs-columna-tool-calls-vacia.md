---
title: Coste copiloto — derivar de tokens del mensaje, no de columna `cost_usd` de tool_calls
date: 2026-05-30
source: facturaia /admin/ia-ops
tags: [observabilidad, copiloto, ia-ops, cost-tracking, supabase, facturaia]
---

# Coste copiloto vacío — la columna `cost_usd` de `copiloto_tool_calls` nunca se escribía

**Síntoma**: panel `/admin/ia-ops` mostraba `Coste total IA $0.00` aunque había 6 mensajes copiloto registrados con tokens reales (`copiloto_mensajes.tokens_in/out` > 0).

**Causa**: el agregado en `src/lib/admin/ia-ops/queries.ts:271` sumaba `cost += Number(t.cost_usd) || 0` desde `copiloto_tool_calls`, pero el INSERT en `src/app/api/copiloto/message/route.ts:188-203` solo escribía `tool_name, params_hash, destructive, confirmed_*, success, error, duration_ms` — `cost_usd`, `tokens_in`, `tokens_out` quedaban NULL en cada fila. Verificado en BD: 4 filas últimos 7d, `n_cost_set=0`. La columna existía desde la migración base 105.

**Fix**: derivar el coste al vuelo en la query del panel usando `estimateCostUsd(modelo, tokens_in, tokens_out)` (función pura ya existente en `src/lib/conciliacion/ai-enrich.ts:281`) sobre `copiloto_mensajes` filtrando `rol='assistant'`. Una sola fuente de verdad. Sin migración BD. La columna `cost_usd` de tool_calls queda NULL — informativa por si hay panel detallado futuro, pero ya no es load-bearing.

**Patrón generalizable**: si un panel suma una columna nullable que requiere un writer separado para rellenarse, el riesgo de "agregado siempre 0" es alto. **Preferir derivar desde columnas que ya se escriben** (tokens + modelo) sobre crear columnas que dependen de que cada caller las recuerde. La auditoría es: `select count(*), count(col) from tabla` — si `count(col) << count(*)` y el panel suma `col`, hay bug.

**No aplicar a**: agregados muy caros (millones de filas) o donde la heurística pierde fidelidad (precios reales del provider vs estimación tokens). Aquí el `estimateCostUsd` está calibrado y los volúmenes son bajos.

Relacionado: [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]] (mismo anti-patrón pero al revés — datos críticos sin estructura vs estructura sin writer).
