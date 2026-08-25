---
title: una fila de auditoría por corrida en multi-tenant es invisible para todas las demás orgs
date: 2026-08-25
source: agency-portal
tags: [multi-tenant, auditoria, rgpd, patron]
---
Los dos crons de flota (purga de transcripts y cierre por inactividad) anotaban
**una sola fila** de auditoría por pasada, colgada de la agencia con más
actividad. Parece un detalle de presentación y no lo es: `/agency/audit` filtra
por `agency_id`, así que **todas las demás agencias no veían en su timeline que
se habían purgado o cerrado datos suyos**. En un cron que borra datos personales
eso es un agujero de trazabilidad RGPD, no una molestia de UI.

Arreglo: un helper puro `groupByAgency(rows)` que reparte la corrida, y **una
fila por agencia afectada**, con el desglose `by_client` dentro y los totales de
la pasada en `run_*`. Si una agencia tiene varios clientes, la fila no se cuelga
de ninguno (`clientId: null`) en vez de atribuirla a uno al azar.

Regla general: **todo lo que un proceso de sistema escriba en un registro que se
lee filtrado por tenant tiene que escribirse una vez por tenant tocado.** El
mismo bug estaba en los dos crons, así que al encontrarlo en uno hay que ir a
buscar a sus hermanos. Ver
[[medir-alcance-en-multi-tenant-sin-agrupar-por-org-mezcla-la-sandbox]] — allí el
fallo era leer sin agrupar; aquí es escribir sin agrupar.
