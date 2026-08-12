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

**Y al medir la deuda, PARTE por el tipo de retorno o sobreestimas ×2,7** (FacturaIA 11-ago). El
recuento honesto «cuántas `SECURITY DEFINER` puede llamar `anon`» daba 35 sobre 207, y el titular
que salió de ahí —«35 expuestas al navegador»— era **falso**: las 35 devuelven `trigger`, y
**PostgREST no expone funciones que devuelven `trigger`** (no son invocables por RPC). Por `anon`
la superficie real era **CERO**; por `authenticated`, 23 de 63.

La query que sí mide lo que importa añade el join a `pg_type`:

```sql
select t.typname = 'trigger' as no_expuesta,
       count(*) filter (where has_function_privilege('anon', p.oid, 'EXECUTE')) as anon,
       count(*) filter (where has_function_privilege('authenticated', p.oid, 'EXECUTE')) as auth
from pg_proc p join pg_namespace n on n.oid=p.pronamespace join pg_type t on t.oid=p.prorettype
where n.nspname='public' and p.prosecdef and p.prokind='f' group by 1;
```

Y dentro de las invocables, la que discrimina riesgo de ruido es **si reciben `org_id` (o un id de
recurso) COMO PARÁMETRO**: es la forma de los dos incidentes reales. Las que solo leen la sesión
(`get_user_org_id`, `current_org_role`) no tienen nada que falsear y son la excepción legítima. Un
recuento sin esa partición manda a auditar 63 funciones cuando las candidatas son 16.

**Cerrada la deuda (FacturaIA mig 665, 12-ago): 23 → 8.** Para decidir función a
función hay que cruzar TRES fuentes; cualquiera sola se equivoca:
1. ¿La usa una política RLS? — **sin filtrar por esquema**, o te pierdes Storage
   ([[politicas-rls-fuera-del-esquema-public-no-salen-filtrando-pg-policies]]).
2. ¿Quién la llama desde el código y con qué cliente? `admin.rpc(...)` es
   service_role y no necesita el grant; `supabase.rpc(...)` en un componente o
   en el middleware sí.
3. ¿La invoca otra función, y esa es `SECURITY DEFINER`? Entonces corre como
   owner y tampoco lo necesita. Comprobarlo en `pg_proc.prosecdef`, no de
   palabra: «lo llama un trigger» fue la excusa que sostuvo el agujero de la
   mig 213 dos meses.

**Revocar una función `RETURNS trigger` es inocuo y conviene hacerlo igual**:
medido, el trigger sigue disparando porque el permiso se comprueba al CREAR el
trigger, no al dispararlo. Y no es invocable ni por PostgREST ni por SQL
(«trigger functions can only be called as triggers»).
