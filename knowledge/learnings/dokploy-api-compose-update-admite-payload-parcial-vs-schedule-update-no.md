---
name: dokploy-api-compose-update-admite-payload-parcial-vs-schedule-update-no
description: Dokploy compose.update SÍ acepta PATCH parcial (solo composeId + field) — contrario a schedule.update que exige payload completo.
date: 2026-05-23
source: claude-code-session
tags: [dokploy, api, trpc, gotcha]
---

**Hallazgo contradictorio**: en Dokploy, `compose.update` y `schedule.update` se comportan distinto pese a ser endpoints "hermanos" tRPC:

- **`schedule.update`**: exige payload COMPLETO. Body `{scheduleId, enabled: true}` → 400 BAD_REQUEST con zodError listando `name, cronExpression, command, ...` como required. Patrón obligatorio: GET schedule → modificar field → POST objeto entero. Ver [[dokploy-api-schedule-update-requiere-payload-completo-no-patch]].
- **`compose.update`**: acepta PATCH parcial. Body `{composeId: "X", env: "VAR=val\n..."}` → HTTP 200 OK y devuelve compose completo actualizado. Funciona para actualizar solo `env`, `description` o `command` sin pasar el resto de campos.

**Cómo me di cuenta**: intentando enviar payload completo a `compose.update` con todos los campos del compose, recibí 400 "Invalid JSON". Resultó ser un control char en alguno de los campos copiados del GET previo. Probar payload mínimo (solo `composeId + env`) funcionó → confirmé que compose.update tiene schema Zod más laxo.

**Implicación**: el patrón seguro Dokploy es **probar primero parcial**. Si rechaza, hacer GET + spread + POST. Si acepta, ahorras un GET round-trip y evitas problemas de re-serializar campos sensibles a control chars.

**Endpoints aproximados** (no exhaustivo, comportamiento puede cambiar entre versiones Dokploy):
- Aceptan parcial: `compose.update`, probablemente `application.update`, `environment.update`
- Exigen completo: `schedule.update`

No hay regla universal Dokploy — verificar por endpoint.
