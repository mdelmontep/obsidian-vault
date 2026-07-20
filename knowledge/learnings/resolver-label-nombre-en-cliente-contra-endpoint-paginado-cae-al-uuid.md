---
title: resolver nombre/label en cliente contra un endpoint paginado cae al UUID crudo
date: 2026-07-20
source: claude-code-session
tags: [react, paginacion, ui, supabase, arquitectura]
---

Hermano de [[contador-por-tab-derivado-de-datos-paginados-colapsa-a-0]]: mismo anti-patrón (tratar un endpoint paginado como si fuera el catálogo completo en cliente), otro síntoma.

**Bug**: un detalle (líneas de composición, líneas de presupuesto) trae `material_id` (UUID) y el front lo traduce a nombre con `new Map(catalogo.map(m=>[m.id, m.denominacion]))` + fallback `?? id`. El `catalogo` viene de `/…/materiales`, que se paginó (50/pág, excluye descatalogados). Si el id cae fuera de la 1ª página o está descatalogado → no está en el mapa → se pinta el **UUID crudo**. En una org grande (4939 materiales) salta siempre.

**Causa raíz**: el endpoint de listado se reutilizó como "catálogo de nombres" en cliente después de meterle paginación (regresión silenciosa: el fallback `?? id` estaba como red de seguridad y pasó a ser el caso normal).

**Fix**: resolver el nombre en el SERVIDOR, en el endpoint de detalle, consultando por id (sin paginar, incluyendo descatalogados) y devolviendo `denominacion` en cada línea. El front usa `l.denominacion`, no un mapa. Para los desplegables de alta que SÍ necesitan el catálogo, pedirlo con `page_size` alto (tope), no la 1ª página.

**Regla**: nombres/labels de una relación se resuelven en el detalle (server-side, por id), nunca en cliente contra un endpoint paginado. Un `?? id` que expone un UUID es la señal.

Caso real FacturaIA: Obras, PR #1103 (UO composición + detalle de presupuesto). El endpoint de presupuesto ya lo hacía bien (`getObraPresupuestoDetail`) y el front lo ignoraba.
