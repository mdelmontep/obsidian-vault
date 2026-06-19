---
title: el advisor de Supabase marca trigger functions DEFINER como ejecutables por anon/authenticated, pero son ruido
date: 2026-06-19
source: claude-code-session
tags: [supabase, seguridad, advisors, rls, triaje]
---
`get_advisors(security)` lista `anon_security_definer_function_executable` /
`authenticated_...` por cada función `SECURITY DEFINER` con EXECUTE a PUBLIC. La
mayoría son **trigger functions** (`RETURNS trigger`): PostgREST NO las expone como
RPC (no se invocan fuera de contexto de trigger) → ruido, aunque el GRANT exista.

El riesgo real son las DEFINER **no-trigger** invocables con args (clase bypass tipo
`change_billing_status`). Triaje:
1. Filtrar `RETURNS trigger` = ruido.
2. Helpers de RLS (`get_user_org_id`, `org_has_feature`, `current_is_superadmin`)
   DEBEN mantener EXECUTE a `authenticated` — no revocar (romperías las policies).
3. `rls_enabled_no_policy` (INFO) en tablas service-role-only es correcto
   (deny-by-default), no bug.

Verificar invocabilidad real con `has_function_privilege` contra prod, no asumir por
el advisor. Caso TuFacturaIA (auditoría 2026-06-19). Ver
[[supabase-rpc-security-definer-execute-public]] · [[supabase-enable-rls-olvidado-tabla-publica]].
