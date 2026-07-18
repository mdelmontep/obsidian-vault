---
title: REVOKE FROM PUBLIC no elimina grants individuales de anon/authenticated
date: 2026-06-11
source: claude-code-session facturaia
tags: [postgres, supabase, seguridad, rls]
---

`REVOKE EXECUTE ON FUNCTION ... FROM PUBLIC` solo quita el grant implícito de PUBLIC. Si `anon`/`authenticated` recibieron EXECUTE individual (p. ej. al crear la función, o por GRANT previo), **lo conservan** y PostgREST sigue exponiendo la RPC al anon key.

Caso real: mig 245 TuFacturaIA (`merge_proveedor`, SECURITY DEFINER) hizo `REVOKE FROM PUBLIC` + `GRANT TO service_role` pero anon/authenticated mantenían EXECUTE → `/rpc/merge_proveedor` público. Fix mig 252.

Patrón correcto para RPC service-role-only:
```sql
REVOKE EXECUTE ON FUNCTION f(...) FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION f(...) TO service_role;
```
Verificar: `has_function_privilege('anon', 'f(...)', 'execute')` debe ser false.

3ª/4ª reincidencia (mig 320 2026-06-17: `merge_cliente`/`crear_org_adicional`/`get_stock_health`/`complete_onboarding_perfil`; migs 486/489 módulo Obras 2026-07-18: `obras_cerrar`/`obras_aceptar_presupuesto`/`obras_siguiente_numero_presupuesto` ejecutables por `authenticated`, verificado `has_function_privilege=true`). Reincide en CADA módulo nuevo porque el grep-audit no se corre al crear la migración → el `REVOKE FROM PUBLIC, anon, authenticated` debe ser el DEFAULT (meterlo en la skill `fia-migracion` + grep de `security definer` sin su trío de REVOKE).

Relacionado: [[supabase-rpc-security-definer-execute-public]] · [[defensa-cableada-vs-codigo-muerto]]
