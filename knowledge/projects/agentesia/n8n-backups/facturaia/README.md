# n8n workflow backups

Snapshots JSON de workflows n8n previos a cada patch reproducible
(`ops/n8n-patches/*.py`). Se commitean intencionalmente al repo para que el
rollback no dependa del disco local del operador que aplicó el patch.

## Convención de nombre

`<YYYYMMDD-HHMMSS>-<workflow-slug>-pre-<patch-name>.json`

Ejemplos:

- `20260517-002928-receptor-pre-delivery-patch.json`
- `20260511-232237-facturaia-receptor-v2-pre-stop.json`

## Rollback

```bash
curl -X PUT "$N8N_URL/api/v1/workflows/$WORKFLOW_ID" \
     -H "X-N8N-API-KEY: $N8N_API_KEY" \
     -H "Content-Type: application/json" \
     -d @ops/n8n-backups/<file>.json
```

Cada patch del directorio `ops/n8n-patches/` documenta su propio comando
exacto de rollback en el docstring (incluye allowlist de `settings` al PUT).

## Reglas inviolables — no commitear secrets

El endpoint `GET /api/v1/workflows/:id` de n8n devuelve solo
`credentials.id` (referencias por ID), nunca los valores reales de la
credencial. Aun así, **antes de cada commit verifica con grep que el dump
no contiene literales sensibles**:

```bash
# Debe devolver 0 matches:
grep -E 'sk-[A-Za-z0-9]{20,}|eyJ[A-Za-z0-9_\-]{20,}|xoxb-|ghp_|AIza[0-9A-Za-z_\-]{30,}' \
  ops/n8n-backups/<nuevo-archivo>.json
```

Si aparece algo, NO commitees el backup tal cual: enmascara el valor con
`***REDACTED***` o regenera el dump desde el panel n8n (que ofusca creds).

## Por qué NO en `.gitignore`

Considerado y descartado. Los workflows son el músculo operativo del
producto en producción y un mal patch sin red de seguridad git puede dejar
el receptor v2 inoperativo (todas las WhatsApp entrantes se pierden).
Cambiar a gitignore obligaría a coordinar el backup por canal aparte
(Drive / Slack), que es exactamente el flujo frágil que estos snapshots
existen para evitar.
