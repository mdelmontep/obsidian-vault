---
title: facturaia tests admin feature flags
date: 2026-04-21
source: claude-code-session
tags: [facturaia, testing, pendiente]
---

Escribir tests automatizados para las funciones criticas del admin panel:

- `orgHasFeature(orgId, featureId)` — probar: core siempre true, override > plan default, feature inexistente = false
- `getOrgBilling(orgId)` — probar lazy expiration: trial vencido → grace_period, grace vencido → expired
- `isSuperadmin()` — probar: email en SUPERADMIN_EMAILS = true, flag en profiles = true, ninguno = false
- Billing state machine: transiciones validas vs invalidas (ej: trial → active OK, trial → cancelled NO)
- Feature toggle: crear override, verificar resolucion, borrar override, verificar que vuelve al plan default

No hay framework de testing configurado aun en FacturaIA. Decidir: vitest vs jest.
