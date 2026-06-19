---
title: endpoint que escribe overrides de features debe gatear "enable" por plan o compra (bypass de pago)
date: 2026-06-19
source: claude-code-session
tags: [saas, seguridad, billing, feature-flags, supabase]
---
`org_has_feature` da precedencia al override de `org_features` sobre el plan. Un
endpoint cliente que hace `upsert(org_features, enabled=true)` (toggle de módulos)
SIN verificar que la feature está en el plan efectivo o comprada = bypass total de
monetización: cualquier owner/admin activa módulos de pago gratis con un solo PATCH.

La convención del frontend ("si no está en plan, redirige a checkout") NO es control
de seguridad — el server debe rechazar (402) el enable de features fuera del plan/sin
compra. La rama `source='addon'` tampoco basta si solo valida `addon_purchasable`
(que la feature SEA comprable) y no que se HAYA pagado.

Regla: enable permitido sólo si `enPlan || override existente con source='addon'`
(que solo escribe el webhook de pago); disable siempre OK. Preservar `source='addon'`
al togglear para no degradar la prueba de compra. Caso TuFacturaIA PATCH
/api/settings/features (auditoría 2026-06-19). Ver [[feature-flags-multi-tenant-patron-plan-defaults-org-overrides]].
