---
title: una regla que compara contra «hoy» va en un trigger, nunca en un CHECK
date: 2026-09-18
source: facturaia
tags: [postgres, migraciones, data-integrity, fechas]
---
Un `CHECK (fecha <= current_date)` parece el techo barato y es una trampa: Postgres
**reevalúa el CHECK cada vez que se vuelve a tocar la fila**, así que una fila escrita
legítimamente en marzo es inválida en abril y cualquier `UPDATE` posterior —aunque no toque
la fecha— se rechaza. Con la tabla vacía entra limpio y explota meses después.

Lo que juzga solo la escritura del momento es un trigger `BEFORE INSERT OR UPDATE`:
- filtra el update que no cambia el dato con `new.fecha is distinct from old.fecha`, para que
  cambiar otra columna nunca reabra el juicio;
- lanza con el `errcode` que la app ya discrimina (`23514` imita al CHECK: el cliente no cambia);
- si el «hoy» tiene zona, escríbela — `(now() at time zone 'Europe/Madrid')::date`, espejo del
  helper de TS: el contenedor no declara `TZ` y entre 00:00 y 02:00 UTC marcaría ayer.

Caso: mig 918 de facturaia, techo de la fecha de expedición.
Ver [[comparar-fecha-date-string-vs-timestamp-iso-como-string-falla]].
