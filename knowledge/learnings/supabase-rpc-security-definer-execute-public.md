---
title: rpc security definer en supabase son ejecutables por anon vía postgrest si no revocas
date: 2026-06-04
source: claude-code-session
tags: [supabase, postgrest, seguridad, rls]
---
Postgres concede EXECUTE a PUBLIC por defecto al crear una función. En Supabase,
PUBLIC incluye anon y authenticated → PostgREST las expone en POST /rest/v1/rpc/<fn>
invocables con el ANON KEY PÚBLICO (está en el bundle JS). Si la función es
SECURITY DEFINER y recibe org_id/user_id por parámetro sin validar al caller
(ej. change_billing_status(org_id,'active')), cualquiera salta el pago / hace IDOR.
Detección: `SELECT proname, proacl FROM pg_proc WHERE prosecdef` → ACL con `=X/` (PUBLIC) o `anon=X`.
Fix: REVOKE EXECUTE ON FUNCTION ... FROM PUBLIC, anon (y authenticated si es verbo
admin-only llamado SOLO con service_role; revocar es seguro porque service_role ignora el ACL).
NO revocar authenticated de helpers usados en políticas RLS (get_user_org_id) ni de
helpers de trigger (recompute_*) — rompe inserts/lecturas de usuario legítimo.
Caso TuFacturaIA mig 213: 50+ RPCs expuestas, change_billing_status = bypass de pago.
