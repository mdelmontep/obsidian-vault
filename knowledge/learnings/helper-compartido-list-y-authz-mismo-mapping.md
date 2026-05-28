---
title: list y authz que comparten predicado de pertenencia = un solo helper
date: 2026-05-28
source: claude-code-session
tags: [multi-tenant, security, design]
---

Cuando "qué se lista" y "qué se puede abrir" responden a la misma pregunta de pertenencia, extraer la respuesta a un helper único. Si vive duplicada en dos sitios, el drift es cuestión de tiempo: un cambio en uno no se refleja en el otro, y aparece un agujero (puedes abrir lo que no listas, o listas lo que no puedes abrir).

**Caso real 2026-05-28 (agency-portal)**: el listado `/documents/invoices` y el proxy `/api/facturaia/pdf/[shadowId]` necesitan la misma respuesta — "¿qué `cliente_remote_id` pertenecen al tenant activo?". Solución: helper único `resolveTenantClienteRemoteIds(agencyId, clientId)` en `src/lib/facturaia/tenant-cliente-mapping.ts` consumido por `listTenantInvoices/Quotes` (filtra el listado) y por `tenantOwnsShadow` (autoriza el PDF).

**Regla**: ante dos call sites que evalúan "esto pertenece a X", buscar el predicado común y extraerlo. Single source of truth elimina la clase entera de bugs cross-tenant donde un endpoint olvida aplicar el filtro que el otro sí aplica.

Ver [[single-source-attribution-multi-fuente]].
