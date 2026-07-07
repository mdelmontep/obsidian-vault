---
name: dokploy-api-schedule-update-requiere-payload-completo-no-patch
description: Dokploy schedule.update NO es PATCH parcial — exige todos los campos del schedule completos o devuelve 400 BAD_REQUEST con zodError.
date: 2026-05-22
source: claude-code-session
tags: [dokploy, api, trpc, gotcha]
---

**Gotcha**: `POST /api/schedule.update` con body `{scheduleId, enabled: true}` para cambiar solo el flag → **400 BAD_REQUEST** con `zodError` listando como required: `name`, `cronExpression`, `command`, `shellType`, `scheduleType`, `composeId`/`applicationId`, `serviceName`. Dokploy usa tRPC con Zod validation strict — no acepta merge parcial.

**Patrón correcto** (re-send pattern):
```
1. GET /api/schedule.list?id=COMPOSE_ID&scheduleType=compose
2. Identificar el schedule por scheduleId, copiar TODO el objeto
3. Modificar SOLO el campo que quieres (ej. enabled = true)
4. POST /api/schedule.update con el objeto completo modificado
```

**Caso real TuFacturaIA 2026-05-22**: activar 2 crons `fiscal-avisos` + `fiscal-recalcular-borrador` requirió mandar `name, description, cronExpression, command, shellType:'bash', scheduleType:'compose', composeId, serviceName, enabled:true` cada vez.

**Aplicable**: a otros endpoints tRPC Dokploy con suffix `.update` (mismo patrón en `application.update`, `environment.update`, etc.). Comportamiento estándar tRPC con schemas Zod estrictos en backend.

**OJO contradicción descubierta 2026-05-23**: `compose.update` SÍ admite payload parcial (verificado con `{composeId, env}` → HTTP 200); también `application.update`/`environment.update` probablemente. No es regla universal Dokploy — **probar por endpoint primero parcial (solo id + field), si falla pasar a completo** (evita re-serializar campos con control chars del GET previo).

**Workaround alternativo**: si tu integración modifica schedules con frecuencia, hacer un helper `updateScheduleField(scheduleId, field, value)` que internamente hace GET + spread + POST. Evita duplicar el re-send en cada llamada.
