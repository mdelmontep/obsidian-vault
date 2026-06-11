---
title: stack n8n — reglas y patrones
date: 2026-04-26
source: claude-md-migration
tags: [n8n, kommo, workflows, api]
---

# Stack n8n

## Infra

- `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` en compose para que `$env.VAR` funcione en Code nodes — sin esto, error `access to env vars denied`
- **Dokploy: env nueva = editar panel Y composeFile YAML**. `compose.environment:` es la lista exacta que se exporta al container; panel solo aporta valores. Ver [[n8n-compose-env-vars-yaml-y-panel]]
- `NODE_FUNCTION_ALLOW_BUILTIN=crypto` para `require('crypto')` en Code nodes. NO añade `URL` global — para parsear URLs usar regex inline. Ver [[n8n-task-runner-sandbox-sin-url-global]]
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
- **Public API `PUT /workflows/:id` rechaza `settings` con keys extra** (`callerPolicy`, `binaryMode` que vienen del GET). Filtrar a solo `executionOrder`; n8n re-aplica resto del estado anterior. Ver [[n8n-public-api-put-workflow-settings-keys]]
- **Inventario callers auth: `endswith('.code')` deja fuera `toolCode` y `httpRequest`** — al migrar headers `x-service-key` o similar, inspeccionar `parameters` JSON-serializado en TODOS los tipos. Ver [[n8n-inventario-auth-incluye-toolcode-y-httprequest]]
- Set node reemplaza `$json` — referenciar nodo fuente: `$('Webhook').first().json.body.args.X`
- **Headers HTTP con `{{ $env.X }}` requieren `=` al inicio del valor** — sin el `=`, n8n manda literal `Bearer {{ $env.X }}` y la API rechaza con 401. El `jsonBody` ya lleva `=` por defecto, los headers no
- **Redis GET node devuelve `$json.propertyName`, no `$json.value`** — IFs con `$json.value notEmpty` siempre dan FALSE pese a haber clave. Usar `$json.propertyName`
- **Claves Redis cross-workflow: normalizar el phone igual en productor y consumidor** — uno guarda `aia_ob:617314938`, otro busca `aia_ob:34617314938` → mismatch silencioso. Centralizar normalización (siempre con prefijo país)
- **`$json.foo || null` en jsonBody manda `null` literal al destino** — si el receptor usa Zod `.optional()` plano falla con 400. Usar `nullishOptional()` en el receptor o construir el body con `if (val) obj.key = val` para omitir clave. Ver [[zod-optional-rechaza-null-en-webhooks-n8n]]
- **TTL Redis para flags cross-workflow ≠ ventana 24h Meta** — si el lifecycle del flag depende de respuesta del cliente (p. ej. `aia_ob:{phone}` para routing de onboarding), 24h se queda corto: cliente tarda más, expira, próximos mensajes ramifican al bot normal. Subir a 30d como tirita; fix estructural = consultar BD como source of truth, Redis como caché

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
- **Wait node con `parameters: {}` = webhook-type, exec stuck infinita** — sin `resume`/`amount`/`unit` el nodo espera un webhook externo que nunca llega. Síntoma: ejecución running >5min. Fix: PUT REST API con `{"resume":"timeInterval","amount":2,"unit":"seconds"}`. Verificar con `jq '.nodes[] | select(.type=="n8n-nodes-base.wait") | {name,parameters}'`. Ver [[n8n-wait-node-vacio-webhook-type-stuck]]
- **n8n ↔ Supabase self-hosted Dokploy = REST API por default**, no Postgres directo via Docker network. Ver [[n8n-supabase-selfhosted-default-rest-api-no-postgres]]
- **Agente que crea entidad relacionada (abono→factura) → tool de lookup OBLIGATORIA** — sin tool `consultar_X`, el agente inventa datos vacíos al referenciar entidades existentes. Patrón: tool de lookup + prompt que la fuerce + agente devuelve `{error}` si no encuentra + endpoint receptor rechaza explícitamente si falta el id origen. Ver [[agente-ia-genera-entidad-relacionada-necesita-tool-lookup-de-referencia]]
- **Wrapper webhook que envuelve un sub-workflow con resultados opcionales = `alwaysOutputData: true` obligatorio en los nodos posteriores al ExecuteWorkflow** — si el sub-workflow puede devolver 0 items (ej. RPC Supabase con filtros que no matchean), el ExecuteWorkflow propaga 0 items y los siguientes nodos NO se ejecutan en absoluto, aunque tengan código `if (!found) return [{json: ...}]`. El webhook devuelve 200 con body vacío (no JSON, ni error) — fallo invisible. Fix: marcar `alwaysOutputData: true` al menos en ExecuteWorkflow + Code de formato + RespondToWebhook. Caso real Simarro 2026-05-04 wrapper `Voz_buscar_viviendas` para Retell: smoke test "0 resultados" devolvía body vacío; el agente voz se quedaba mudo
- **Code node heredado de otra fuente = shape mismatch silencioso hasta producción** — al replicar un workflow y cambiar el nodo "fuente" (ej. Google Calendar trigger → Kommo Tasks node), el Code aguas abajo sigue iterando con el shape ANTIGUO (`evento.start.dateTime`, `summary`) y peta cuando llega data real (`_embedded.tasks[].complete_till`, `text`). El error solo aparece en la primera ejecución cron real, no durante config. Síntoma: `TypeError: Cannot read properties of undefined`. Fix: tras cambiar la fuente de un Code node, ejecutar manualmente el workflow una vez y leer la última execución antes de declarar listo. Caso real Simarro 2026-05-04: workflow Recordatorios fallando cada 30min durante días sin que nadie lo viera

## WhatsApp Cloud API

- **Ventana 24h**: si el destinatario no ha escrito a la business en últimas 24h, solo se entregan templates pre-aprobados. Un `text` libre devuelve `wamid` exitoso pero NO llega al destinatario (Meta lo descarta sin error). Producción: crear template aprobado en Meta Business Manager y enviar `type: 'template'`. Para tests: que el destinatario escriba primero al número business para abrir la ventana

---

## Gotchas Simarro voz (mayo 2026)

### Kommo node parámetro `with` requiere ARRAY no string
```javascript
// MAL — error críptico "options.with.join is not a function"
"options": {"with": "leads"}
// BIEN
"options": {"with": ["leads"]}
```

### httpRequest devuelve `{data: "stringified..."}` por defecto
Para que n8n parsee JSON automáticamente:
```json
"options": {"response": {"response": {"responseFormat": "json"}}}
```
Sin esto, downstream Code nodes ven `lead.data` como string y `lead.custom_fields_values` es undefined.

### n8n public API — settings allowed list para PUT
Solo estos campos pasan validación al hacer PUT `/api/v1/workflows/:id`:
```
executionOrder, timezone, saveExecutionProgress, saveManualExecutions,
saveDataErrorExecution, saveDataSuccessExecution, executionTimeout,
errorWorkflow, callerPolicy, callerIds
```
**No incluir**: `availableInMCP`, `binaryMode`, ni otros internos. Filtrar antes de PUT o devuelve 400 `"settings must NOT have additional properties"`.

### Loop polling exit guard para tests
Patrón: `Get a call → If [status==ended] → ...async... | Wait → loop`. En test playground el call nunca llega a `ended` → loop eterno (hasta cancelación manual).

Fix: añadir OR al If con `combinator: 'or'`:
```
$json.call_status == 'ended'  OR
$('Webhook1').item.json.body.call.call_type == 'web_call'
```
En test el web_call exit-ea al primer ciclo. En producción inbound (`phone_call`) sigue polling hasta end real.

### Insert nodes con `onError: continueRegularOutput`
Los nodos Postgres/Insert que dependen de datos del call de Retell fallan en test porque `Get a call` devuelve null. Para que el error no rompa el flow:
```json
{"onError": "continueRegularOutput"}
```
En producción funcionan normal (datos reales). En test el insert falla silently y el workflow termina success.

### TZ parsing — Madrid local NUNCA reconvertir
Si el input es `"YYYY-MM-DD HH:MM"` sin offset/Z, **ya viene en hora Madrid**. NO hacer:
```javascript
new Date("2026-05-12 13:30")  // V8 con TZ UTC interpreta como UTC
+ Intl.DateTimeFormat({timeZone:'Europe/Madrid'})  // suma +2h DST → 15:30
```

Patrón correcto — extraer componentes del string:
```javascript
const m = s.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})/);
if(m) return {y:+m[1], mo:+m[2], d:+m[3], h:+m[4], mi:+m[5]};  // ya es Madrid
```

Para weekday usar `Date.UTC(y,mo-1,d).getUTCDay()` (NO timezone-shift, es matemática de calendario).

### Severar paths multi-trigger
Si dos triggers (HTTP voz + executeWorkflow chat) convergen en un mismo `Edit Fields`, los inputs difieren y ramas downstream corren con datos parciales/vacíos. Cada trigger su propio preprocessor; lógica común a sub-workflow.

Caso real Simarro: `Webhook Retell` (voz) disparaba `Edit Fields` (chat preprocessor) además de `Edit Fields Retell`. La rama `Es cancelación?` del chat se ejecutaba con datos vacíos → ramas peligrosas (`Buscar Ainhoa/Carlos/Pedro/Ramon` con query=Lead_id vacío) borraban TODOS los eventos del calendario.

### Respond temprano en webhook + async branch
Para latencia baja con escritura externa (Kommo, Calendar, WA), patrón:
- Webhook → Edit Fields → [paralelo: Componer FAST → Respond FAST] + [async: lookup → create lead → calendar → WA]
- `responseMode: responseNode` responde con el PRIMER respond alcanzado → FAST gana siempre.
- Resto se ejecuta en background.
- Ahorro: 800-1500ms perceptibles vs esperar a creación.

### Code node modo
- `runOnceForAllItems`: permite `$input.first()`, `$input.all()`, `$('NodeName').item.json`. Default y más versátil.
- `runOnceForEachItem`: NO permite `$input.first()` — error `Can't use .first() here`. Solo si necesitas iterar item-by-item con `$json` y poco más.

## Gotchas Code + If (mayo 2026)

- **`If` v2 strict — `null != 0` ⇒ TRUE**. Rompe detección "este id existe?" con `notEquals 0`. Patrón seguro: emitir flag booleano `_has_X = !!X` en el Code anterior, If `boolean.true` sobre el flag. Ver [[n8n-if-strict-null-not-equals-0-evalua-true]].
- **Final response que lee `$('NodeX').first().json` crashea si NodeX no se ejecutó** (rama de cortocircuito, validation fail, dry_run). Patrón: chequear `$input.first().json._short_circuit === true` primero, passthrough. Lookup específico siempre envuelto en try/catch. Ver [[n8n-code-final-response-leer-input-no-nodo-concreto-si-hay-branches]].
- **`executeWorkflowTrigger` con `inputSource:"workflowInputs"` filtra campos no declarados**. Añadir nuevos campos al schema del trigger en TODOS los sub-workflows downstream (cascade). Ver [[n8n-executeworkflowtrigger-schema-estricto-filtra-campos]].

## Gotchas n8n LangChain 2.x (mayo 2026)

### `@n8n/n8n-nodes-langchain.toolHttpRequest` typeVersion 1.1 — invocaciones secuenciales rotas
Cuando el AI Agent invoca dos tools en la misma conversación con `jsonBody` que usa expressions tipo `={{ $('NodoX').first().json.Y }}`, el SEGUNDO tool peta con `The node "@n8n/n8n-nodes-langchain.toolHttpRequest" has a "supplyData" method but no "execute" method`. El primer tool funciona OK. El bug está en n8n-core `WorkflowExecute.runNode`: cae al fallback `execute()` cuando solo existe `supplyData`.

Verificación: `grep -c "execute" .../ToolHttpRequest/ToolHttpRequest.node.js` → 0 (solo tiene `supplyData`).

Workarounds:
1. Esperar n8n 2.21+ con fix (typeVersion 1.2+).
2. Migrar tools a `toolWorkflow` con sub-workflows (cada sub-workflow hace el HTTP con credential, devuelve JSON al agente). Más nodos pero estable.
3. Mantener `toolCode` viejo (jsCode) con `$env.X` y aceptar `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` con threat model documentado. Pragmático.

Caso real TuFacturaIA 2026-05-16: refactor para eliminar `$env.X` del workflow Receptor v2 reveló este bug. Rollback al estado pre-refactor + deuda documentada en hub.

### `$fromAI()` en jsonBody requiere `placeholderDefinitions` o falla igual
El error "supplyData but no execute" también lo dispara `$fromAI('param', 'desc', 'string')` en el body sin declarar el placeholder. Para que funcione: añadir `placeholderDefinitions.values` con cada param.

### `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` no sandboxea Code node contra `process.env`
El flag solo bloquea `$env.X` en expressions. Un Code node puede hacer `process.env.X` o `require('child_process').execSync('env')` y leer todo igual. **No es medida de seguridad real ante RCE en n8n container** — solo protege contra "editor n8n con permisos limitados", escenario que NO existe en Community Edition single-admin.

Documentar el flag como "defensa marginal" en threat model, no como bloqueante.

### Envs en n8n Dokploy: doble registro obligatorio
Para que el container lea una env:
1. Pestaña **Environment** del proyecto Dokploy → añadir `VAR=valor`.
2. Pestaña **Compose** → en `environment:` añadir `- VAR=${VAR}` (referencia, Dokploy sustituye al Deploy).

Si solo está en Environment pero NO referenciado en compose, el container no la recibe. Diagnóstico: `docker exec <ct> printenv VAR` debe devolver el valor.

### n8n Dokploy Deploy real vs Reload
- **Deploy**: recrea el container con compose nuevo. Usar siempre tras editar Compose o Environment.
- **Reload**: solo recarga el panel, NO toca containers.
- **Diagnóstico post-Deploy**: `docker ps --format "{{.Names}} {{.Status}}"` debe mostrar "Up xxs/min" (recién creado). Si sigue "Up xxh", Deploy NO recreó (típicamente porque no se pulsó Save antes de Deploy, o no se editó realmente nada).

### Bypass SSH a compose es temporal
Modificar `/etc/dokploy/compose/<stack>/code/docker-compose.yml` via SSH funciona para el siguiente `docker compose up -d --force-recreate`, pero Dokploy regenera el archivo desde su BD interna en el siguiente Deploy del panel. Bypass solo de emergencia; el cambio permanente vive en el panel.

## Gotchas Code node + HTTP node (mayo 2026)

### Code sandbox sin `URLSearchParams` ni `URL`
Tira `URLSearchParams is not defined`. Si está dentro de try/catch fail-open queda silente. Usar concat manual con `encodeURIComponent`. Ver [[n8n-code-sandbox-no-tiene-urlsearchparams]]

### `sessionId` viene sin `+` — endpoints E.164 estrictos lo rechazan
Workflow normaliza `34617314938` (solo dígitos). Endpoint Zod `regex(/^\+[1-9]\d{7,14}$/)` devuelve 400. Combinado con fail-open → persist nunca ocurre, sin alerta. Normalizar a `+34...` antes del POST. Ver [[n8n-sessionid-sin-plus-vs-endpoint-e164]]

### HTTP node `responseFormat: 'json'` revienta con 404 HTML de Traefik
Durante ventanas de redeploy Dokploy, Traefik devuelve `404 page not found\n` (text/plain) brevemente. El parser JSON tira antes de aplicar `neverError`. Fire-and-forget → `responseFormat: 'text'` + `neverError: true`. Crítico → `options.retry: { tries: 3, waitBetweenTries: 1500 }`. Ver [[n8n-http-responseformat-json-rompe-con-404-traefik]]

### Persist con merge shallow deja cruft entre contextos
Endpoints state machine que UPSERT con `{...existing, ...incoming}` contaminan al cambiar contexto: campos viejos coexisten con nuevos en el JSONB. Mandar `field: null` explícito desde el cliente para los que deben morir. Simétrico: al guardar draft, nullear last_listado. Ver [[persist-merge-shallow-deja-cruft-entre-contextos]]


### Google OAuth credentials NO se pueden crear via Public API
Schema buggy: `useDynamicClientRegistration` controla if/else en allOf pero no está en `properties` (`additionalProperties: false`). Workaround: crear cred OAuth en n8n UI (browser, requiere OAuth dance anyway). Vía API solo `openAiApi`, `postgres`, `redis`, `smtp`, `httpHeaderAuth`, `telegramApi`. Ver [[n8n-public-api-google-oauth-schema-buggy-crear-en-ui]]

### Postgres node con responseMode lastNode solo devuelve primer row
`SELECT` que retorna N filas + webhook `lastNode` → solo primera fila en respuesta HTTP. Engaña pensando que las queries no corrieron. Fix: agregar con `array_agg()` o `json_agg()`, o usar `responseNode` con JSON.stringify($items()). Ver [[n8n-postgres-webhook-lastnode-solo-devuelve-primer-row]]

### Compose con networks external:true falla en Dokploy nuevos
Dokploy AgentesIA pre-crea la network; Dokploys nuevos en Stackscale (Docker no-Swarm) no. Container queda `state=created` con error "network not found". Fix: quitar `external: true`. Ver [[n8n-network-external-true-falla-en-dokploy-sin-pre-create]]

### Fan-out post-create paralelo (log + side effects no críticos)
Tras crear entidad principal (Calendar event, fila DB, etc.), abrir N salidas paralelas: respond webhook rápido + emails + Sheet/Log append. Cada salida con `onError: continueRegularOutput` para que side effects opcionales no rompan flow primario. Ej. EcoBox `Reservar_cita`: GCal → [Email cliente, Email Cristian, Respond Retell, Sheet append]. Ver [[ADR-014-ecobox-log-universal-sheet-vs-chatwoot-voice-conversation]]

### emailReadImap v2: `from` es objeto, no string
`$json.from` en typeVersion 2 devuelve `{value:[{address,name}], text}`. Hacer `.toLowerCase()` directamente tira `is not a function`. Normalizar: `const raw = $json.from; const from = (typeof raw === 'string' ? raw : (raw?.text || raw?.value?.[0]?.address || '')).toLowerCase();`

### Code node después de Postgres `alwaysOutputData:true` recibe el `{}` del Postgres, no el dato del trigger
`$input.first()` sube un solo nivel. Si hay un nodo Postgres entre el IMAP trigger y el Code con `alwaysOutputData:true`, el Code lee `{}` en silencio. Fix: referenciar el nodo fuente por nombre: `$('IMAP Trigger').first().json`.

### `executeWorkflow` workflowInputs: IIFE `(function(){...})()` falla con "invalid syntax"
Las expresiones en `workflowInputs` no admiten IIFEs. Si la expresión es compleja, calcular en un Code node previo y pasar como `$json.campo`.

### IMAP trigger deja de hacer polling tras ciclos repetidos deactivate/activate
`staticData` queda en estado corrompido (`{}`). No llega ninguna ejecución aunque la cred y los filtros sean correctos. Diagnóstico: leer `staticData` del workflow via API. Fix: **reiniciar el contenedor n8n** desde Dokploy (no basta con desactivar/activar el workflow). Ver [[elphis-doctoralia-email-sync-2026-06-11]]
