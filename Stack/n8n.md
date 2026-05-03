---
title: stack n8n — reglas y patrones
date: 2026-04-26
source: claude-md-migration
tags: [n8n, kommo, workflows, api]
---

# Stack n8n

## Infra

- `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` en compose para que `$env.VAR` funcione en Code nodes — sin esto, error `access to env vars denied`
- Nunca hardcodear keys en jsCode — usar `$env.VAR_NAME`. Supabase: usar JWT legacy (`eyJ...`), no `sb_secret_*`
- Filtrar workflows por prefijo de cliente antes de tocar nada en instancias multi-cliente
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
- **Headers HTTP con `{{ $env.X }}` requieren `=` al inicio del valor** — sin el `=`, n8n manda literal `Bearer {{ $env.X }}` y la API rechaza con 401. El `jsonBody` ya lleva `=` por defecto, los headers no
- **Redis GET node devuelve `$json.propertyName`, no `$json.value`** — IFs con `$json.value notEmpty` siempre dan FALSE pese a haber clave. Usar `$json.propertyName`
- **Claves Redis cross-workflow: normalizar el phone igual en productor y consumidor** — uno guarda `aia_ob:617314938`, otro busca `aia_ob:34617314938` → mismatch silencioso. Centralizar normalización (siempre con prefijo país)

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
- **Salesbot IDs**: `/api/v2/salesbot` es privado (404 externo). Obtener IDs desde el navegador en la cuenta Kommo: `fetch('/ajax/v4/bots/?limit=100').then(r=>r.json()).then(d=>console.log(JSON.stringify(d,null,2)))`

### Migración entre clientes

Actualizar: sub-workflow IDs, pipeline_id, status_id, field_id, amojo_id, bot_id, responsible_user_id, task_type_id, Google Calendar ID, credenciales n8n

### Credenciales fantasma heredadas (CRÍTICO al replicar de un cliente a otro)

Cuando los workflows se replican copiando blueprints, **los nodos quedan apuntando a credential IDs que NO EXISTEN en el n8n del cliente nuevo**. El error es invisible hasta que se ejecuta el workflow real:

- El workflow se importa OK
- El workflow se activa OK
- Al ejecutar, el nodo falla con `Credential with ID "XXX" does not exist for type "YYY"`
- Si es SMTP: silencio total (cliente no recibe nada)
- Si es Google Calendar: el agente WhatsApp/voz no puede consultar disponibilidad → todo flujo de citas se rompe en silencio

**El name engaña**. El `name` que aparece en `node.credentials.<type>.name` puede mostrar un nombre PARECIDO al real (ej. "Google Calendar Simarro") aunque el `id` apunte a una credencial INEXISTENTE. **Es solo el snapshot del momento del último guardado del nodo**, no refleja la realidad actual de n8n. Una misma cred ID fantasma puede aparecer con 3 nombres distintos según workflow.

**Caso real Simarro 2026-05**:
- 5 nodos referenciaban cred SMTP `oKRmYFhljczyvzV8` con name "SMTP account" → no existía
- 4 nodos referenciaban cred Google Calendar `W6EuUTZnvCtqCTjX` con names "Google Calendar Simarro" / "gonzaloautomatizaciones" / "GCAL_TODO_REPLACE_WITH_KOMMO_TASKS" → no existía
- Bug oculto durante toda la fase de configuración por confiar en el name

**Cómo detectar**:
- `"Credential with ID 'XXX' does not exist"` → fantasma total (no existe)
- `"Forbidden - perhaps check your credentials?"` → existe pero OAuth caducado o permisos mal
- Una cred con MÚLTIPLES `name snapshot` distintos para el MISMO `id` → señal fuerte

**Auditoría obligatoria antes de declarar workflow listo para test E2E**:

```python
import json, os, urllib.request
KEY = os.environ['N8N_API_KEY']
BASE = os.environ['N8N_BASE']
H = {"X-N8N-API-KEY": KEY}

# 1) Recolectar todas las creds referenciadas + name snapshots
all_creds = {}
wfs = json.loads(urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/v1/workflows?limit=100", headers=H)).read()).get('data', [])
for w in wfs:
    full = json.loads(urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/v1/workflows/{w['id']}", headers=H)).read())
    for n in full.get('nodes', []):
        for ctype, cinfo in (n.get('credentials') or {}).items():
            all_creds.setdefault((ctype, cinfo.get('id')), []).append((w['name'], n['name'], cinfo.get('name', '')))

# 2) Imprimir todas con sus snapshots
for (ctype, cid), refs in all_creds.items():
    snaps = set(s[2] for s in refs)
    if len(snaps) > 1:
        print(f"⚠ FANTASMA PROBABLE: {ctype} id={cid} aparece con names: {snaps}")
    for wname, nname, snap in refs:
        print(f"  {ctype} id={cid} | {wname:<35} → {nname:<30} | snap '{snap}'")

# 3) Para confirmar, ejecutar webhook real que use la cred. Errors:
# - "does not exist" = fantasma
# - "Forbidden" = existe pero auth rota
```

**Reasignación masiva via API** (cuando el cliente crea la cred real):

```python
OLD = "fantasmaXXX"
NEW = "realYYY"
TYPE = "googleCalendarOAuth2Api"
ALLOWED = {'executionOrder','timezone','saveManualExecutions','errorWorkflow','saveExecutionProgress','saveDataSuccessExecution','saveDataErrorExecution'}
for w in wfs:
    full = json.loads(urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/v1/workflows/{w['id']}", headers=H)).read())
    changed = []
    for n in full['nodes']:
        creds = n.get('credentials') or {}
        if TYPE in creds and creds[TYPE].get('id') == OLD:
            creds[TYPE] = {'id': NEW, 'name': 'Reasignado'}
            changed.append(n['name'])
    if changed:
        s = {k:v for k,v in (full.get('settings') or {}).items() if k in ALLOWED} or {"executionOrder":"v1"}
        payload = {"name":full['name'],"nodes":full['nodes'],"connections":full['connections'],"settings":s,"staticData":full.get('staticData')}
        H2 = {**H, "Content-Type":"application/json"}
        urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/v1/workflows/{w['id']}", data=json.dumps(payload).encode(), headers=H2, method="PUT"))
        urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/v1/workflows/{w['id']}/activate", headers=H2, method="POST"))
        print(f"✓ {w['name']}: reasignados {changed}")
```

**Regla práctica**: antes de cada test E2E con cliente nuevo, ejecutar la auditoría. Coste 5 min. Sin esto, debugueas horas un flujo que falla en silencio porque la cred parecía correcta por su nombre.

## API

- `GET /credentials` no expone valores. `POST /credentials` crea (passwords alfanuméricos simples)
- `PUT /workflows/{id}`: solo name, nodes, connections, settings, staticData
- `POST /workflows` crea inactive. `POST /workflows/{id}/activate` activa (no PATCH)
- JSON con Code nodes: escribir a /tmp con Python, `curl -d @file`. Parsear con `strict=False`
- `executeWorkflowTrigger` v1.1 requiere input schema — usar v1.0 si no necesitas validación
- HTTP multipart: `parameterType: "formBinaryData"` con `inputDataFieldName` dentro de bodyParameters
- Binary filesystem: `getBinaryDataBuffer(0, 'data')`, nunca `$binary.data.data`
- **HTTP Request 4xx NO marca ejecución en rojo** — n8n las pone success y mete el error en `data.main[0][0].json.error`. Para diagnosticar 401/404 mirar el output del nodo, no el status global de la ejecución

## AI Agents

- Nombres de tools en prompt deben coincidir EXACTAMENTE con name de nodos
- `memoryPostgresChat` NO persiste tool calls — tools de escritura se re-ejecutan. Mitigar con frase-ancla de cierre
- Nunca llamar write-tool sin todos los datos — regla explícita en prompt
- `toolHttpRequest` sin parámetros + GPT-4.1 = ignora tool-calling. Usar marcador textual + lógica determinista
- Tool description write-tools: ~280 chars con consecuencias de no llamar
- `toolWorkflow onError`: siempre `continueErrorOutput`
- `toolWorkflow.workflowId.cachedResultName` puede mentir tras clonar — validar `value` contra workflows reales. Ver [[n8n-toolworkflow-cachedresultname-puede-mentir]]
- Replicar entre clientes: diff por nombres de nodo + vaciar IDs origen a placeholders TODO. Ver [[replicar-cliente-n8n-vaciar-ids-cz-no-disfrazar]]
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
- **Button replies (interactive) = workflow run NUEVO** — al pulsar Confirmar/Corregir/Cancelar, n8n arranca otra ejecución con `msg_type='interactive'`. El estado del run anterior (audio/texto, JSON del agente, productos detectados...) se pierde. Si necesitas algo del run original (ej: caption "por voz" vs "por texto"), persistirlo en BD/sesión cuando arranca el flujo, leerlo en el run del button. `n8n_chat_histories` (Postgres Chat Memory) sirve si añades metadata, o crear tabla pequeña `voice_pending_sessions(phone, source, expires_at)`.
- **`SUPABASE_SERVICE_ROLE_KEY` hardcodeado en Code nodes es leak silencioso** — cualquiera con login al UI de n8n.X.com ve el JWT en el source del node. Rotar la key no protege si sigue ahí (el patcher la actualiza pero queda visible). Patrón obligatorio: `const SUPABASE_KEY = $env.SUPABASE_SERVICE_ROLE_KEY`. Aplica a cualquier secret.
- **Public API `PUT /workflows/{id}` solo acepta `name + nodes + connections + settings.executionOrder`** — si pasas el `settings` completo del GET (con `callerPolicy`, `availableInMCP`, `binaryMode`...) devuelve 400 `request/body/settings must NOT have additional properties`. Patrón: limpiar a `{ executionOrder: wf.settings?.executionOrder || 'v1' }` antes del PUT.
- **Queue mode + Wait nodes ~60s atascado** — en `EXECUTIONS_MODE=queue`, Wait con segundos parece poll cada 60s aunque el unit sea correcto. Workaround `QUEUE_RECOVERY_INTERVAL=5` (no 100% verificado). Ver [[n8n-queue-mode-wait-nodes-poll-cada-60s]]
- **n8n ↔ Supabase self-hosted Dokploy = REST API por default**, no Postgres directo via Docker network. Ver [[n8n-supabase-selfhosted-default-rest-api-no-postgres]]
- **Agente que crea entidad relacionada (abono→factura) → tool de lookup OBLIGATORIA** — sin tool `consultar_X`, el agente inventa datos vacíos al referenciar entidades existentes. Patrón: tool de lookup + prompt que la fuerce + agente devuelve `{error}` si no encuentra + endpoint receptor rechaza explícitamente si falta el id origen. Ver [[agente-ia-genera-entidad-relacionada-necesita-tool-lookup-de-referencia]]

## WhatsApp Cloud API

- **Ventana 24h**: si el destinatario no ha escrito a la business en últimas 24h, solo se entregan templates pre-aprobados. Un `text` libre devuelve `wamid` exitoso pero NO llega al destinatario (Meta lo descarta sin error). Producción: crear template aprobado en Meta Business Manager y enviar `type: 'template'`. Para tests: que el destinatario escriba primero al número business para abrir la ventana
