---
title: n8n api put workflows rechaza settings desconocidos
date: 2026-04-20
source: claude-code-session
tags: [n8n, api, bug]
---

Al hacer `PUT /api/v1/workflows/{id}`, solo enviar estos campos en `settings`:
- `executionOrder`
- `callerPolicy`
- `errorWorkflow`
- `saveExecutionProgress`
- `saveManualExecutions`
- `saveDataErrorExecution`
- `saveDataSuccessExecution`
- `executionTimeout`
- `timezone`

Campos como `binaryMode`, `availableInMCP`, `timeSavedMode` causan error:
> "request/body/settings must NOT have additional properties"

**Solución**: al descargar un workflow con GET y re-subirlo con PUT, filtrar settings antes:

```python
valid = {'executionOrder', 'callerPolicy', 'errorWorkflow'}
settings = {k: v for k, v in settings.items() if k in valid}
```

El payload de PUT solo acepta: `name`, `nodes`, `connections`, `settings` (filtrado).

**Update 2026-05-22**: en `n8n.tufacturaia.com` (versión n8n mayo 2026) también rechaza `callerPolicy` y `binaryMode` — la whitelist válida varía por versión. Apuesta segura: enviar **solo `executionOrder`** y dejar que el server restaure defaults en el siguiente GET.

**Strip top-level también** (read-only que el GET incluye pero PUT rechaza): `id, createdAt, updatedAt, active, tags, versionId, meta, pinData, triggerCount, shared, isArchived, homeProject, sharedWithProjects`.

Tras filtrar, `active` puede quedar en false → re-activar con `POST /workflows/{id}/activate` (exige `Content-Type: application/json` con body explícito). Confirmado de nuevo en EcoBox 2026-06-01. Ver [[n8n-public-api-no-permite-update-credentials-recrear-y-repuntar]].
