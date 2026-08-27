---
title: una columna de purga que ningún cron rellena es retención aparente
date: 2026-08-27
source: agency-portal
tags: [rgpd, retencion, migraciones, supabase]
---

La migración crea `evidence jsonb`, `evidence_purged_at` y su índice parcial
`where evidence is not null and evidence_purged_at is null`. Todo el aparato de
retención está ahí: catálogo verificable, índice pensado, comentario explicando el
sello. Y **ningún cron lo toca** — `grep evidence src/lib/fleet` no devuelve nada.

El engaño es que la revisión de la migración pasa: las columnas existen, el índice
existe, la intención está escrita. Lo que falta no se ve desde el SQL. En este caso
la tabla nueva citaba turnos literales de conversaciones, así que a los 90 días el
cron vaciaba transcripts y `call_logs.summary` y dejaba las citas vivas — la
retención abierta por la puerta de atrás, con apariencia de cubierta.

**Regla**: quien crea la columna de purga entrega en el MISMO track el cron que la
rellena, o la migración no entra. Verificación barata: por cada `*_purged_at`,
`*_until` o `retention_*` del esquema, un grep que devuelva su escritor.

Ver [[retencion-en-tabla-compartida-por-dos-superficies-una-ventana-borra-la-otra]].
