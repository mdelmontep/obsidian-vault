---
title: el cliente de impersonación stubbea .rpc() → cualquier dato servido por RPC sale vacío en Vista cliente
date: 2026-07-17
source: claude-code-session
tags: [impersonation, supabase, rpc, dashboard, facturaia]
---
En FacturaIA la "Vista cliente" (superadmin) usa `createImpersonateClient(orgId)`: reenvía `.from()` a `/api/admin/impersonate/query` (service-role acotado a org) pero **stubbea TODAS las `.rpc()`** con `{data:null, error:'read-only'}`. Efecto trampa: cualquier widget cuyos datos vengan de una RPC (no de `.from()`) sale **vacío/skeleton** al ver como cliente, mientras el resto de la página carga bien. Caso real: las tarjetas "Salud del negocio" se vaciaron cuando los KPIs se movieron a la RPC `dashboard_kpis` (mig 460) — no fallaba para usuarios normales, solo en impersonation.

Regla: al mover lógica de `.from()` a una RPC, comprobar que NO rompe la Vista cliente. Si la Vista cliente debe verlo, la RPC necesita un `p_org_id` opcional y hay que exponerla por un endpoint superadmin (allowlist read-only) que la ejecute con service-role fijando la org — la RPC `SECURITY INVOKER` sin RLS (service-role) exige el filtro explícito por org. Patrón: PR #988 (`/api/admin/impersonate/rpc` + `p_org_id` en `dashboard_kpis`). Ver [[endpoints-impersonate-por-query-no-cookie]] · [[nextjs16-impersonation-cookie-stuck-no-implica-middleware-off]].
