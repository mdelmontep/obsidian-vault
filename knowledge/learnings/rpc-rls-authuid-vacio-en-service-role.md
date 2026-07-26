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

## Tercera ocurrencia (2026-07-26): ahora con hook

Esta lección estaba escrita AQUÍ (2026-06-19) y también en
[[supabase-rpc-con-auth-uid-falla-con-service-role]] (2026-04-26). No lo evitó.

El 2026-07-26, en FacturaIA, se desplegaron dos RPC nuevas (`fiscal_reabrir`,
`recibida_eliminar`) con `IF NOT public.user_can_write_in_org(...)` dentro,
copiando el patrón de `fiscal_marcar_cuadrada` y `fiscal_marcar_presentada`, que
YA estaban rotas por lo mismo: o sea "marcar cuadrada" y "marcar presentada"
llevaban tiempo sin funcionar (encaja con que no hubiera ni una declaración con
`presentada_en` en producción). Las cuatro abortaban con 'forbidden' 42501.

Test que lo hace concluyente en un minuto, sin efectos: llamar la RPC con un
argumento que falle DESPUÉS del guard de permisos (p.ej. hash inválido). Si
devuelve 'forbidden' en vez del error esperado, nunca llega a la lógica.

Fix aplicado (mig 569): condicionar, no quitar a ciegas —
`IF auth.uid() IS NOT NULL AND NOT public.user_can_write_in_org(...)`. Autoriza el
endpoint con `withApiAuth({requireWrite})`, que tiene la sesión real, y el límite
de la función es el REVOKE a service_role.

**La corrección duradera NO fue esta nota: fue un check en `.githooks/pre-push`**
que bloquea el patrón en cualquier migración nueva. Dos notas no evitaron la
tercera ocurrencia. Ver [[feedback_loop_engineering_disciplina]].
