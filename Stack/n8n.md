---
title: stack n8n — reglas y patrones
date: 2026-04-26
source: claude-md-migration
tags: [n8n, kommo, workflows, api]
---

# Stack n8n

## Infra

- `N8N_ENCRYPTION_KEY` idéntica en migración — si cambia, credenciales inutilizables
- Redis sin volumen (es caché). Dominio real antes de OAuth/webhooks Meta
- `DB_POSTGRESDB_DATABASE` obligatorio en compose (n8n + worker)
- `N8N_HOST` antes de OAuth — sin él, callback usa traefik.me
- Compose prod: healthcheck HTTP, pruning 168h/5000, memory 2G, versión fija (no `:latest`)
- Community nodes requieren restart contenedor Docker

## Expresiones

- `isExecuted` no valida si Redis devolvió datos — añadir `&& .json.value != null`
- `&&` en campo URL inline se rompe — usar editor de expresión completo o nodo Set previo
- IF no permite AND/OR mixto — expresión JS en una sola condición
- `$('Nodo')` falla si no se ejecutó — usar `$if($('Nodo').isExecuted, ..., fallback)`
- Set node reemplaza `$json` — referenciar nodo fuente: `$('Webhook').first().json.body.args.X`

## Kommo

- Long Lived Token: integración privada → Keys and scopes. Hasta 5 años sin refresh
- LLT requiere subdominio cuenta, NO `api-c.kommo.com`
- OAuth2 redirect: `https://<dominio>/rest/oauth2-credential/callback` exacto
- `amojo_id` hardcodeado por cuenta — actualizar al migrar
- amojo API usa token sesión propio, NO OAuth2/LLT. Patrón Laserys: `POST /ajax/v1/chats/session`
- Scope "Chats" puede no aparecer en UI — contactar support@kommo.com
- Webhook "Mensaje entrante recibido" SOLO — otras acciones generan eventos sin contenido
- `status_lead` dispara en TODOS los cambios — filtrar con IF `status_id == X`
- Custom field names cambian entre cuentas — verificar al migrar
- Task types NO se crean vía API — solo UI Kommo
- Salesbots pueden mover leads sin n8n — revisar acciones GUI

### Migración entre clientes

Actualizar: sub-workflow IDs, pipeline_id, status_id, field_id, amojo_id, bot_id, responsible_user_id, task_type_id, Google Calendar ID, credenciales n8n

## API

- `GET /credentials` no expone valores. `POST /credentials` crea (passwords alfanuméricos simples)
- `PUT /workflows/{id}`: solo name, nodes, connections, settings, staticData
- `POST /workflows` crea inactive. `POST /workflows/{id}/activate` activa (no PATCH)
- JSON con Code nodes: escribir a /tmp con Python, `curl -d @file`. Parsear con `strict=False`
- `executeWorkflowTrigger` v1.1 requiere input schema — usar v1.0 si no necesitas validación
- HTTP multipart: `parameterType: "formBinaryData"` con `inputDataFieldName` dentro de bodyParameters
- Binary filesystem: `getBinaryDataBuffer(0, 'data')`, nunca `$binary.data.data`

## AI Agents

- Nombres de tools en prompt deben coincidir EXACTAMENTE con name de nodos
- `memoryPostgresChat` NO persiste tool calls — tools de escritura se re-ejecutan. Mitigar con frase-ancla de cierre
- Nunca llamar write-tool sin todos los datos — regla explícita en prompt
- `toolHttpRequest` sin parámetros + GPT-4.1 = ignora tool-calling. Usar marcador textual + lógica determinista
- Tool description write-tools: ~280 chars con consecuencias de no llamar
- `toolWorkflow onError`: siempre `continueErrorOutput`
- `onError: continueRegularOutput`: output es `{error: {message, name}}`, no `{statusCode, body}`
- PGVector Embeddings: conexión `ai_embedding`, no `ai_vectorStore`
- `$fromAI()` en toolCode puede fallar — usar variable global `query` y parser manual
- `fetch` no existe en sandbox — usar `this.helpers.httpRequest`
- `httpRequest returnFullResponse` sigue lanzando en non-2xx — parsear status del catch
- `memoryPostgresChat` session key es teléfono, no conversation ID. Tabla: `id, session_id, message` (jsonb LangChain)
- 0 eventos Calendar = todo libre (regla explícita en prompt + Think)
- Weekday: incluir `$now.weekday` + fórmula + ejemplos
- Worker valida TODOS los nodos — plugins no instalados bloquean en "Queued"
- `N8N_BLOCK_ENV_ACCESS_IN_NODE` bloquea `$env.X` en todos los nodos
- Google Sheets tool: `columns.value: {}` vacío = filas en blanco sin error
- Webhook síncrono: `responseMode: "responseNode"` + nodo `respondToWebhook`
- IF/Switch v2.2+: requieren `conditions.options.version: 2`, `caseSensitive`, `typeValidation: "strict"`
- Tests contra webhooks prod disparan acciones reales — usar datos que no activen side effects
