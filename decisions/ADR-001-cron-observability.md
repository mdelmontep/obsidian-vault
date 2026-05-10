---
title: ADR-001 — observabilidad de crons via tabla cron_runs + Dokploy externo
date: 2026-05-11
status: accepted
tags: [adr, facturaia, observability, crons]
---

## Contexto
FacturaIA tenía 5 crons en Dokploy (`webhook-dispatcher`, `check-vencimientos`, `verifactu-process`, `storage-quota-check`, `run-module-suggestions`) sin observabilidad: si fallaban en silencio, nadie se enteraba hasta que un cliente reportaba algo roto. Necesitamos saber en qué estado están sin entrar a logs de Dokploy.

## Opciones consideradas
- **A** — `setInterval` dentro de Next.js: rápido pero se reinicia con cada deploy, no persiste hora, múltiples instancias = N ejecuciones.
- **B** — Worker dedicado (`node-cron` package): reinventa lo que Dokploy ya hace, sigue dependiendo de Dokploy para reiniciar el worker.
- **C** — Cron del SO dentro del contenedor: mezcla web server + scheduler, escala mal.
- **D** — `pg_cron` (Postgres): lógica TS (`buildCashflowData`, `notify…`) tendría que reescribirse en PL/pgSQL.
- **E** — Dokploy cron externo + tabla `cron_runs` propia + `withCronTracking` wrapper: aprovecha la infra existente (Dokploy ya programa 3 crons), añade observabilidad sin nueva infra.
- **F** — Temporal / Inngest / Trigger.dev: durabilidad transaccional + retries automáticos, pero infra entera para 5-10 crons es overkill.

## Decisión
**E** — Dokploy mantiene el scheduling externo; cada cron se wrappea con `withCronTracking('<name>', handler)` que inserta en `cron_runs` start/end/status/duration/summary/error y emite notif `cron_failed_<name>` al fallar. Panel admin `/admin/system/crons` muestra semáforo + últimas 10 ejecuciones por cron. Auto-purge >30 días.

Razón: 6 crons no justifican migración a Temporal/Inngest. Dokploy ya programa, solo faltaba el lado observable.

## Consecuencias
- **Compromete a futuro**: cualquier cron nuevo va con `withCronTracking` + entrada en `src/lib/cron/registry.ts` con descripción human-friendly + ejemplo real.
- **Cerramos como opción** (por ahora): durabilidad transaccional, retries automáticos con backoff, multi-instance coordination. Si en algún momento un cron se vuelve crítico para SLO de cliente, reabrir y migrar ESE a Temporal/Inngest (no toda la infra).
- **Cuándo revisitar**: cuando tengamos 20+ crons o un cliente exija SLO formal sobre ejecución.
