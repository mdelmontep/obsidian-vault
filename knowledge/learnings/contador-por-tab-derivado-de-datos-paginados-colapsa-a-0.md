---
title: contador por tab/segmented derivado de datos ya paginados colapsa a 0 al filtrar
date: 2026-07-06
source: claude-code-session
tags: [react, paginacion, ui, supabase]
---

Patrón de bug recurrente: badges de un Segmented/tabs (ej. "WhatsApp 9", "Vencida 12") calculados con `.filter()`/`.reduce()` sobre el array `data` que YA devuelve el hook paginado — y ese `data` ya viene acotado server-side por el filtro activo (`.eq('estado', filtroActivo)`) y por `.range()`.

**Síntoma**: al activar un tab concreto, el resto de badges colapsan a 0 (solo hay filas del tab activo en el array). El propio "Todas" puede estar mal: si usa `totalCount` de esa misma query filtrada, no es el total real; si usa `data.length`, es solo el tamaño de página.

**Fix**: separar "conteo por categoría" (debe ser independiente del filtro activo, global u respetando SOLO los demás filtros) de "datos de la página actual" (sí filtrados/paginados). Implementación: N queries `.select('id', {count:'exact', head:true})` en paralelo, una por categoría, sin `.eq()` sobre el campo que define el tab. Exponerlas como campo aparte del hook (`channelCounts`/`estadoCounts`), nunca derivarlas de `data` en el componente.

**Gotcha en tests**: si el mock de Supabase comparte un único objeto `chain.eq` entre la query paginada y las nuevas queries de conteo, los tests que assertan "NO se llamó a `.eq('x', y)`" se rompen por falsos positivos — las queries de conteo llaman `.eq()` con valores que la query principal no usaba. Aislar con un sub-chain propio para el conteo (ej. rutear por `select(cols, {head:true})` a un chain distinto).

Hermano: [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]] (misma trampa — endpoint paginado tratado como catálogo completo en cliente — pero el síntoma es un UUID crudo en vez de un conteo a 0).

No es específico de un proyecto: aplica a cualquier vista con Segmented/tabs + paginación server-side + Supabase/Postgres. Caso real: 4 vistas de TuFacturaIA con el mismo bug (`/ingesta`, `/emitidas`, `/recibidas`, `/presupuestos`, PRs #771/#772).

**Variante badge con endpoint dedicado (FacturaIA #829)**: si el contador YA tiene un endpoint autoritativo propio (ej. `/unread-count`, escanea 500 filtrando severidad a nivel DB), cuidado con un SEGUNDO fetch (el del listado, típico en hooks SWR) que también escriba ese valor con su count sobre la página cargada — lo DEGRADA (críticas antiguas fuera del slice → badge a 0). Regla: el fetch del listado actualiza solo `items`; el contador lo mantiene únicamente su endpoint dedicado.

**Variante más dura (conciliación, PR #773)**: si el "estado" no es una columna sino que se DERIVA en JS de agregados sobre varias tablas relacionadas (asignaciones, metadata, sugerencias IA...), el conteo `select(id, {count, head:true})` no basta — hay que portar esa clasificación a una función SQL (`CASE`/`EXISTS`/`SUM` con `FILTER`), `SECURITY INVOKER` si RLS ya scopea por org (no confiar en un `p_org_id` de parámetro). Bonus: si la clasificación JS dependía de una query con `.limit(N)` sin acotar por fila, portarla a SQL con `EXISTS` sin límite corrige ese sesgo de paso.
