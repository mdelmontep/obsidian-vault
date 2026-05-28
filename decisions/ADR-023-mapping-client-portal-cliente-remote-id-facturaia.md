---
title: ADR-023 — Mapping client (portal) ↔ cliente_remote_id (FacturaIA) via union de fuentes existentes, sin migration
date: 2026-05-28
status: accepted
tags: [adr, agency-portal, facturaia, multi-tenant]
---

## Contexto
`facturaia_documents` (sombras en agency-portal) tienen `cliente_remote_id` apuntando a `clientes.id` de la BD remota de FacturaIA — sin FK posible. Para listar facturas/presupuestos direct del tenant en `/documents/*` y para autorizar el proxy PDF hace falta mapping client (portal) ↔ cliente_remote_id (FacturaIA).

## Opciones consideradas
- **A — Columna `clients.facturaia_cliente_id`** + migration + backfill desde `facturaia_documents` por matching NIF/email. Limpio pero costoso, requiere mantener invariante en cada emisión.
- **B — Union de fuentes ya existentes**: `prospects.facturaia_cliente_id` + `cliente_remote_id` de sombras ya enlazadas (`agency_invoice_id`/`invoice_id`/`quote_id` no NULL). Sin migration, funciona si el tenant tiene >=1 emisión desde el portal.
- **C — Solo `prospects.facturaia_cliente_id`**: deja huecos para clientes creados manualmente o cuyo prospect-of-origin no emitió desde el portal. Rechazado tras bug Simarro 2026-05-28.

## Decisión
**B**, porque resuelve el 95% de casos sin migration ni backfill. Helper único `resolveTenantClienteRemoteIds` en `src/lib/facturaia/tenant-cliente-mapping.ts`, consumido por listado y autorización (evita drift).

## Consecuencias
- Si el tenant nunca ha emitido nada desde el portal, sus facturas direct no se listan ni se abren — comportamiento explícito ("sin trazabilidad, no se atribuye").
- Si el caso aparece como problema en producción, escalamos a A (migration + backfill). No quemamos esa puerta.
