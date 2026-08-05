---
title: ADR-048 — TuFacturaIA se queda en Supabase Cloud; autoalojar se reabre solo por encima de ~150 $/mes
date: 2026-08-05
status: accepted
tags: [adr, facturaia, infra, supabase, coste]
---

## Contexto

Pregunta recurrente: si la app ya corre en hierro propio (Dokploy/Docker, más n8n autoalojado), ¿por qué la BD sigue en Supabase Cloud y no se trae todo? El objetivo declarado era **dejar de pagar Supabase sin perder nada**.

Medidas reales del proyecto de prod `Dashboard` (`lahqlyaxvobqjgdiftag`, eu-west-1), tomadas el 5-ago-2026:

- BD **481 MB**. Compute **Micro**: 2 vCPU compartidas, **1 GB RAM**, ~10 $/mes.
- Tabla mayor `cron_runs` 172 MB (36%), volumen legítimo de 30 días con retención ya programada. Ver [[facturaia]] y `docs/architecture/gotchas.md` §Crons.
- Segundo proyecto en la org (`facturaia-stock-test`) sin addons de compute.
- **Factura real: 20 $/mes.** Storage y egress no aparecen como partida, así que la hipótesis de "el dinero está en los PDF" quedó descartada al medir.

Lo único cloud es Supabase (Postgres + Auth + Storage). El resto o ya es nuestro o es un tercero no localizable (Stripe, Meta, OpenAI, AEAT VeriFACTU, FNMT TSA, B2, SMTP).

## Opciones consideradas

- **A. Seguir en Supabase Cloud** — 20 $/mes, backups y PITR incluidos y probados por otro, upgrades ajenos. Contra: 1 GB de RAM, latencia de internet por query, `db_max_rows` fijo en 1.000 (origen del truncado silencioso).
- **B. Autoalojar Supabase en el VPS** — ahorra ~20 $/mes, latencia sub-ms, RAM a voluntad y `db_max_rows` configurable. Contra: asumimos PITR, drills de restauración, upgrades de GoTrue/Storage/PostgREST/Realtime, y migrar `auth.users` conservando el JWT secret (si cambia, mueren todas las sesiones de todos los clientes a la vez). Riesgo ya documentado: un slot de Realtime roto llena el disco vía WAL sin límite, y Realtime se usa en 6 sitios.
- **C. Podar y quedarse** — retención de logs, apagar el proyecto de test, mover PDFs fríos a B2. Al medir resultó casi vacía: la purga de `cron_runs` ya existía y no hay partida de Storage que recortar.

## Decisión

**A**, con umbral de revisión explícito. El ahorro máximo son **240 $/año** y el downside es perder la BD fiscal de clientes que pagan, con obligación de conservación VeriFACTU. La apuesta es asimétrica en la dirección mala, y las horas de montar y **probar** backups propios valen más que el premio.

**Umbral para reabrir**: factura por encima de ~150-200 $/mes, o un cliente que exija residencia de datos. Antes de eso, no se discute.

## Consecuencias

- Si el compute aprieta, **subir de Micro a Small (~15 $ más) antes que plantear cualquier migración**: comprar RAM siempre sale más barato que comprar nuestro tiempo.
- El tope de 1.000 filas de PostgREST se queda como constraint permanente del diseño, no como algo a esquivar cambiando de hosting. El trinquete `max-rows` sigue siendo la defensa.
- Si algún día se ejecuta B, el requisito de salida es un **drill de restauración probado**, no una tarea posterior.
- Queda cerrado como opción traer la BD "a local" en el sentido de oficina o portátil: `supabase start` es para desarrollo y tests de integración, no para servir producción.
