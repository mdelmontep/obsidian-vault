---
title: un rpc/policy que scopea por auth.uid() devuelve vacío con service-role
date: 2026-06-19
source: claude-code-session
tags: [supabase, rls, service-role, api]
---

Un RPC `SECURITY DEFINER` (o cualquier query) que filtra por `auth.uid()` —
directa o vía RLS — depende del JWT del usuario autenticado. Llamado con el
**service-role / admin client** (`createAdminClient`), `auth.uid()` es NULL y RLS
se bypasea → devuelve vacío o, peor, TODAS las filas de TODAS las orgs.

Trampa concreta (FacturaIA 2026-06-19): el RPC `dashboard_top_clientes` va por RLS
(`auth.uid()` → org). Reusarlo en un endpoint `/api/v1/*` (que corre service-role)
NO funciona: no hay sesión de usuario. Fix: NO reusar el RPC del dashboard;
reimplementar la agregación en el endpoint/cron con filtro **`org_id` explícito**
(`.eq('org_id', orgId)`) tomado del principal/contexto, nunca del input.

Regla: en servidor/v1/cron con admin client, el scoping por org es responsabilidad
del CÓDIGO (filtro explícito), no de RLS. RLS solo protege el path `authenticated`.
Ver [[supabase-rpc-security-definer-execute-public]].
