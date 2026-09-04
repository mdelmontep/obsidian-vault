---
title: al recrear rpc postgres mantener firma idéntica o queda función huérfana
date: 2026-05-25
updated: 2026-09-04
source: claude-code-session
tags: [postgres, plpgsql, supabase, rpc]
---

> **REINCIDIÓ el 31-jul con este learning ya escrito.** Mig 601 de FacturaIA declaró
> `aplicar_movimientos_lotes(uuid, boolean)` con un `p_revertir` **inventado** que ni aparecía en el
> cuerpo; la firma real era `(uuid)`. Sobrecarga creada, vieja intacta, y todos los llamantes
> (`perform ...(p_factura_id)`) siguieron ejecutando la vieja: **el fix se desplegó muerto**.
> Lo que no avisa: `supabase db push` imprime `Finished` y `migration list` da la migración por
> aplicada. Solo se ve consultando `pg_proc`, y el síntoma es **dos filas donde debía haber una**.
> El paso 4 de abajo existía y no se usó: puesto en la 601, la transacción habría fallado en vez de
> mentir.

`CREATE OR REPLACE FUNCTION nombre(args) RETURNS X` reemplaza la función SOLO si `(nombre, args)` matchea exactamente. Si cambias firma — añades/quitas un arg, cambias tipo, cambias return — Postgres crea una función NUEVA y deja la vieja huérfana. Resultado: callers que invocan la firma antigua siguen ejecutando la vieja; los que usan la nueva ejecutan la nueva. División silenciosa.

PL/pgSQL compila el body en lazy (al primer EXECUTE), no en CREATE FUNCTION. Por eso una mig que referencia `OLD.columna_que_no_existe` se aplica sin error y solo falla en runtime al ejecutar el trigger/func (caso real TuFacturaIA mig 095 → mig 162: `OLD.entorno_verifactu` cuando la columna real era `verifactu_entorno`).

**Patrón seguro**:
1. Antes de recrear un RPC, `\df nombre` o grep migraciones para encontrar la firma exacta vigente.
2. Si necesitas cambiar la firma, primero `DROP FUNCTION nombre(args_viejos)` explícito, luego CREATE nuevo. Romperá callers — aceptable solo si los controlas todos.
3. Si el body referencia columnas nuevas/renombradas, ejecuta `SELECT nombre(test_args)` en la propia mig como verificación post-creación.
4. Tras un refactor de firma, añade un `DO $$ ... $$` que cuente sobre `pg_proc`/`pg_get_function_identity_arguments` las firmas esperadas (=1) y huérfanas (=0) y falle la transacción si quedó algo. Caso: `convertir_presupuesto_a_factura` (uuid,uuid) de mig 036 sobrevivió huérfana 6 migs (082/084/088/119) hasta el smoke de la 119.

Aplica también a triggers (`OLD.X` / `NEW.X`) y a constraints CHECK.

**Grants/ACL se preservan**: `CREATE OR REPLACE` (firma idéntica) NO toca los privilegios — un `REVOKE` de una mig previa sigue vigente; recrear NO resetea a PUBLIC. Misconcepción común en auditorías: creer que mig 216 al recrear `change_billing_status` "reconcedió" EXECUTE a anon/authenticated → falso, el REVOKE de mig 213 seguía aplicado. Para cambiar el ACL hace falta un `GRANT`/`REVOKE` explícito, no basta recrear.

**Caso especial — cambiar `RETURNS TABLE`**: PostgreSQL lanza hard error `42P13` ("cannot change return type of existing function") en lugar de crear función huérfana silenciosa. `DROP FUNCTION IF EXISTS` antes del `CREATE` es obligatorio, no opcional. Caso real: mig 236 TuFacturaIA añadió `org_nombre` a `storage_usage_by_org()` → fallo en `db push` hasta añadir el DROP.

**Añadir un parámetro con `DEFAULT` es el caso que más engaña**: parece compatible hacia atrás
y no lo es. Crea sobrecarga igual, y además con **las dos** firmas terminadas en `DEFAULT` una
llamada corta casa con ambas y Postgres la rechaza por ambigua (`42725`) — así que la vieja no
solo sobrevive: rompe a los llamantes que no tocaste. Aplicado bien en la mig 828 de FacturaIA
(4-sep-2026, ticket #171): `DROP FUNCTION` de la firma de 4 argumentos **dentro de la misma
transacción** que crea la de 5, más el `DO` del paso 4 contando firmas. Verificado por catálogo
tras el `db push`: una sola fila en `pg_proc`.
