---
title: un guard de una migración ajena bloquea el db push entero, incluidas las tuyas
date: 2026-07-25
source: claude-code-session
tags: [supabase, migraciones, deploy, facturaia]
---

`supabase db push` aplica en orden y **para en la primera que falla**. Si prod va
varias migraciones por detrás de `main`, tus migraciones nuevas no se aplican por un
guard de otra rama que exige intervención manual. Caso real: la 558 abortaba con
"quedan 3 asignaciones con importe_aplicado <= 0, resuélvelas siguiendo el runbook",
y con eso bloqueaba la 559 y la 560, que no dependían de ella.

Antes de prometer un deploy: `select max(version) from
supabase_migrations.schema_migrations` y contar el hueco contra `ls
supabase/migrations`. El hueco es deuda de deploy ajena y aparece como TU bloqueo.

Salida: si las tuyas son independientes, aplicarlas dirigidas
(`supabase db query -f <ruta ABSOLUTA>`, el `-f` relativo se resuelve contra
`--workdir`, no contra el cwd) y registrar la versión. Si `migration repair` no está
disponible, el DDL queda aplicado sin fila en `schema_migrations`: no pasa nada
**si las migraciones son re-ejecutables** (`ADD COLUMN IF NOT EXISTS`,
`DROP FUNCTION IF EXISTS` + `CREATE`), que es otra razón para escribirlas así.
Ver [[aplicar-migracion-por-psql-y-registrar-version-cuando-el-cli-supabase-esta-bloqueado]].

Gotcha operativo: `db push` **no imprime progreso** hasta terminar, así que parece
colgado. Con `--debug` sí se ve qué migración está aplicando. Un push "colgado" que
no toca la BD (comprobable con `pg_stat_activity` vacío) es buffering, no un lock.

Desenlace del caso: otra sesión desbloqueó la 558 horas después y su `db push`
repasó las 559/560 ya aplicadas **sin efecto y registrándolas**, cerrando el hueco
del historial sin intervención. Escribirlas re-ejecutables no fue una precaución
teórica: fue lo que hizo que la deuda se arreglase sola.
