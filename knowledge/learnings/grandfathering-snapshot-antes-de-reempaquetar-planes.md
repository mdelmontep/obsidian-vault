---
title: grandfathering — snapshot a org_features antes de reempaquetar plan_features
date: 2026-06-26
source: claude-code-session
tags: [pricing, planes, supabase, multi-tenant, billing]
---

Al mover features entre tiers (reempaquetar `plan_features`), los clientes existentes
pierden acceso a lo que ya usaban si solo cambias los defaults del plan.

Patrón (todo en la MISMA migración, en este orden):
1. INSERT en `org_features` un override `enabled=true, source='grandfathered'` por cada
   feature que cada org tiene HOY vía su plan actual (`JOIN plan_features WHERE enabled`).
   Filtro: `billing_status IN ('active','trial') AND NOT complimentary`. `ON CONFLICT DO NOTHING`
   (respeta overrides previos manuales/addon).
2. DESPUÉS cambiar `plan_features` (quitar feature de un tier = `enabled=false`, NUNCA DELETE).

El override por org gana sobre el default del plan → el cliente conserva acceso aunque su
tier ya no incluya esa feature. Si el CHECK de `source` no admite el valor nuevo, extiéndelo
en la misma migración (DROP+ADD constraint). Las altas nuevas sí ven el empaquetado nuevo.

Relacionado: [[feature-flags-multi-tenant-patron-plan-defaults-org-overrides]] · [[cambiar-plan-debe-invalidar-todos-los-datos-derivados]]
