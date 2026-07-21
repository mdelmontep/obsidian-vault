---
title: RPC SECURITY INVOKER sin parámetro de org no es llamable desde admin client (bypasa RLS)
date: 2026-07-22
source: claude-code-session
tags: [supabase, rls, security, rpc, multi-tenant]
---
Un RPC `SECURITY INVOKER` que resuelve el scoping por-org SOLO vía RLS (sin `p_org_id` como parámetro explícito) asume que el caller siempre lleva la sesión del usuario. Si luego lo llamas desde un `service_role` client (admin client, típico en RSC/server-fetch para bypasear RLS y hacer el `.eq('org_id', ...)` a mano), el RPC sigue ejecutándose — `SECURITY INVOKER` solo decide CON QUÉ rol corre el cuerpo de la función, y `service_role` bypasa RLS igual que con cualquier tabla. Resultado: el RPC cuenta/lee de TODAS las orgs, no solo la tuya — fuga cross-tenant silenciosa (sin error, solo dato incorrecto).

Fix: el RPC necesita `p_org_id` como parámetro explícito + filtro interno con él, no depender de `auth.uid()`/RLS implícito. Antes de extraer cualquier query a un helper server llamado con admin client, comprobar que TODAS las tablas Y RPCs involucrados acepten/filtren por org explícitamente — si alguno depende de RLS sin parámetro de org, esa ruta no es migrable a admin-client sin tocar BD primero.
