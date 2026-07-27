---
title: Dokploy API — `schedule.runManually` para Run Now de un cron sin tocar UI
date: 2026-05-23
source: smoke cron cashflow-alerts cashflow v2
tags: [dokploy, api, crons, ops]
---

## Necesidad

Forzar la ejecución de un cron Dokploy "ya" (Run Now) sin tener que abrir el panel UI ni esperar a su schedule natural. Útil para smokes post-deploy, debug de un cron que silenciosamente falla, o validar un fix de cron sin sleep al cron expression.

## Solución

```bash
DPLY_KEY="..."   # x-api-key del panel
DPLY_BASE="https://dokploy.tufacturaia.com/api"

# 1. Listar schedules del compose para obtener scheduleId
curl -sS "$DPLY_BASE/schedule.list?id=<composeId>&scheduleType=compose" \
  -H "x-api-key: $DPLY_KEY"

# 2. Lanzar ejecución manual
curl -sS -X POST "$DPLY_BASE/schedule.runManually" \
  -H "x-api-key: $DPLY_KEY" -H "Content-Type: application/json" \
  -d '{"scheduleId":"<scheduleId>"}'
# → devuelve `true` si dispara OK
```

## Endpoints que NO funcionan (probados)

- `POST /api/schedule.run` → `404 Not Found`
- `POST /api/schedule.execute` → `404 Not Found`

El nombre canónico es **`schedule.runManually`** — no documentado oficialmente.

## Listar schedules requiere ambos params

```bash
# ❌ FAIL: "Input validation failed" — id and scheduleType required
curl "$DPLY_BASE/schedule.list" -H "x-api-key: $KEY"

# ✅ OK
curl "$DPLY_BASE/schedule.list?id=<composeId>&scheduleType=compose" -H "x-api-key: $KEY"
```

`scheduleType` válido: `application | compose | server | dokploy-server`. Para crons del stack tufacturaia-app: `compose` con el `composeId=56B2b1ypWx3Xzdr06eYtG`.

## Verificación post-run

Una vez disparado, el cron escribe en `cron_runs` (mig 063 `withCronTracking`). Verificable con:

```sql
SELECT cron_name, status, started_at, finished_at, duration_ms, summary, triggered_by
FROM cron_runs
WHERE cron_name = '<nombre>'
ORDER BY started_at DESC
LIMIT 3;
```

El `triggered_by` aparece como `'dokploy'` independientemente de si fue auto o manual — Dokploy no distingue. Si quieres trazabilidad de Run Now manual vs schedule auto, hace falta meta-tag adicional (no hay hoy).

## Caso real cashflow-alerts 2026-05-23 22:55

Disparo manual desde la API:
- scheduleId: `yLMQQOIAEpT-v2lHwm2Pz`
- Resultado: `true`
- `cron_runs` 806ms success summary `{total_orgs:5, checked:3, no_alert:1, alerted:0, skipped_no_feature:2, skipped_dedupe:2, errors:0}`.

## `schedule.create` — alta de un cron nuevo (2026-07-25)

`POST /api/schedule.create` funciona (200 + el objeto creado con su `scheduleId`). **No inventes el payload: cópialo de un schedule que ya funciona** en el mismo compose (`schedule.list` → toma uno de molde) y sustituye solo `name`/`cronExpression`/`command`. Así heredas `shellType` y `serviceName`, que son justo los campos que hacen que el cron no se ejecute si faltan (ver [[dokploy-schedule-sin-servicename-no-se-ejecuta]]).

Payload que entró bien en `tufacturaia-app`:

```json
{"name":"…","cronExpression":"25 * * * *","command":"sh /app/ops/cron/sign-call.sh /api/internal/… POST",
 "scheduleType":"compose","composeId":"56B2b1ypWx3Xzdr06eYtG","shellType":"bash","serviceName":"facturaia","enabled":true}
```

Idempotencia: no la da la API. El script debe abortar si el `name` ya está en `schedule.list` — si no, duplica el cron.

## Cross-ref

- Reference `reference-dokploy-facturaia` en memory del agente — añadir esta sección al endpoint list.
- `src/lib/cron/track.ts:withCronTracking` — patrón canónico TuFacturaIA para crons.
- Botón Run Now en `/admin/system?tab=crons` hace lo mismo via `loadHandler` interno + Request sintético (no sale a Dokploy API).
