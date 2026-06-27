---
title: smokear un trigger/migración SQL contra prod con una tx que hace ROLLBACK
date: 2026-06-27
source: claude-code-session
tags: [postgres, supabase, testing, smoke]
---
Validar un trigger/migración nuevos contra el SCHEMA REAL de prod, sin merge ni deploy ni contaminar datos:
`BEGIN; <CREATE OR REPLACE de la migración>; <op que dispara el trigger>; <SELECT de aserción>; ROLLBACK;` en una sola conexión psql. DDL+DML son transaccionales en Postgres → el ROLLBACK revierte TODO (incluida la redefinición de la función y cualquier `pg_net` encolado, que solo se envía en COMMIT).

Gotcha clave: **UPDATE una fila REAL con una transición battle-tested** (la que el cron ya hace en prod), NO un INSERT sintético — insertar p.ej. una factura emitida dispara la cadena de huella fiscal Verifactu y otros triggers pesados. Cambiar el estado de una fila existente es la operación que prod ya ejecuta a diario → segura.

Construir el script con `cat` del `.sql` (no heredoc con sustitución de shell) para no expandir los `$$` del dollar-quoting.

Caso real: mig 406 `factura.vencida` validada así (UPDATE→vencida + assert outbox + rollback, 0 persistido).
