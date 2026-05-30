---
title: cliente react bypasa endpoint canónico con supabase.from() — guards = teatro
date: 2026-05-30
source: claude-code-session
tags: [auth, defense-in-depth, supabase, react, fiscal, gotcha]
---

Cuando un endpoint canónico tiene guards (BD CHECK + 422 + audit log), el cliente NO debe replicar la lógica con `supabase.from('X').insert/update` directo desde el componente — el guard del endpoint se vuelve teatro y el bug latente se cuela en BD silenciosamente.

**Caso real PR #108 TuFacturaIA**: `handleAprobar` en `ingesta-view.tsx` insertaba factura USD `tipo_cambio_fuente='manual_requerido'` con `tipo_cambio=1` (=EUR), falsificando `base_eur` fiscal. El endpoint `POST /api/recibidas/[id]/aprobar` rechazaba con 422, pero nadie lo llamaba.

**Patrón fix**:
1. Cliente edita campos NO críticos directo (proveedor, descripción, etc).
2. Para el cambio de estado o cualquier transición con efecto fiscal/legal → `fetch(POST endpoint)` canónico.
3. Manejo explícito 422/409/404 con copy específico al usuario.

**Detección**: `grep -rn "from('facturas').insert\|update" src/components/` debería devolver vacío si todos los flujos transicionan vía endpoint. Cualquier resultado = candidato a refactor.

Ver [[campo-huerfano-shape-sin-migracion-paralela]].
