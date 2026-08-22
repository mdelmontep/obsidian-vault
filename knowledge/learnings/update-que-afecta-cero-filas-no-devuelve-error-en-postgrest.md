---
title: un update que afecta a cero filas no devuelve error en postgrest
date: 2026-07-30
source: claude-code-session
tags: [supabase, postgrest, rls, integridad, guardado-silencioso]
---
`await supabase.from(t).update(x).eq('id', id)` con `error === null` NO significa que se
haya escrito nada. Si la RLS filtra la fila, o el `id` no existe, o el estado ya cambió,
PostgREST responde 204 sin error → el endpoint contesta `{ok:true}` y la UI pinta
"Guardado" sobre una escritura que no ocurrió. Es la familia entera de fallos que destapó
la auditoría de TuFacturaIA (30 sitios).

Fix: el update tiene que **pedir la fila de vuelta** y comprobarla.
`.select('id').maybeSingle()` → si `data` es `null`, son cero filas → 409, no 200.
Envuelto en `updateOneOrThrow()` (`src/lib/api/update-one.ts`): error → 500, cero filas → 409.
Guard de conformidad en CI para que no vuelva a colarse un update sin `select`.

Y `updateOneOrThrow` solo cubre lo que pasa por la API: una escritura CLIENT-SIDE del
navegador directa a PostgREST no lo ve. Caso real (TuFacturaIA #2100, 22-ago): en una org
suspendida, Ajustes → Empresa guarda el `settings` (endpoint de servidor, cliente de servicio que
bypasea RLS) y DESCARTA las columnas de `organizations` (PATCH del navegador contra la policy con
`AND NOT is_billing_readonly(id)`). Mismo botón: media pantalla guarda y media no, sin un aviso.

Corolario para los mocks: en cuanto el código pasa por ahí, un mock que devuelve
`{data: null, error: null}` ya no es "da igual", es un 409. Ver
[[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]].
