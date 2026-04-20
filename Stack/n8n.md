---
title: stack n8n — todas las reglas y patrones
date: 2026-04-20
source: claude-md-migration
tags: [n8n, kommo, workflows, api]
---

# Stack n8n

- `N8N_ENCRYPTION_KEY` debe ser idéntica en cualquier migración — si cambia, todas las credenciales quedan inutilizables
- Redis no necesita volumen persistente (es caché) — quitarlo evita problemas de estado
- Dominio real con DNS configurado antes de OAuth o webhooks de Meta — traefik.me es rechazado
- `DB_POSTGRESDB_DATABASE` es obligatorio en los servicios `n8n` y `n8n-worker` del compose — sin él n8n no sabe a qué base de datos conectar
- `N8N_HOST` debe estar configurado en Dokploy antes de configurar OAuth2 — si no, n8n genera el callback con dominio traefik.me que es rechazado por los proveedores OAuth

## Expresiones en nodos HTTP

- **`isExecuted` no valida si Redis devolvió datos** — es `true` aunque el nodo no encontrara el key. Siempre añadir `&& $('Nodo').first().json.value != null` a la condición, o la URL queda con `null` y da 404.
- **Expresiones con `&&` en campo URL se rompen en el editor inline** — el editor interpreta `&&` como salto de línea. Usar el editor de expresión completo (icono `=`) o resolver el valor en un nodo Set previo y referenciar `$json.campo` en la URL.
- **IF no permite AND/OR mixto** — solo permite AND para todas las condiciones o OR para todas. Para lógica mixta, usar una sola condición con expresión JS que evalúe a `true`: `{{ $json.body.event === 'X' && ($json.body.status === 'a' || $json.body.status === 'b') }}`

## Kommo

- Long Lived Token: Ajustes → Integraciones → Crear integración privada → Keys and scopes → "Generate long-lived token". No existe clave API tradicional en Kommo.
- OAuth2 redirect URL debe ser exactamente `https://<dominio>/rest/oauth2-credential/callback` — no solo el dominio base
- `amojo_id` es por cuenta, se obtiene con `GET /api/v4/account?with=amojo_id`. Los workflows lo tienen hardcodeado — hay que actualizarlo por cliente al migrar
- `bot_id` en HTTP Request nodes corresponde a salesbots de Kommo — también cambia por cuenta, actualizar igual que el `amojo_id` al migrar
- **amojo API v1 usa token de sesión propio, NO OAuth2 ni Long Lived Token** — `amojo.kommo.com/v1/chats/{amojo_id}/{chat_id}/messages` requiere header `X-Auth-Token` con un amojo_token (Centrifugo session token, expira ~24h). OAuth2 access_token y Long Lived Token dan 401 en ese endpoint
- **Patrón Laserys para amojo_token dinámico** — `POST {account_url}/ajax/v1/chats/session` con OAuth2 (scope "Chats") + `X-Requested-With: XMLHttpRequest` + body `request[chats][session][action]=create`. Respuesta: `response.chats.session.access_token` (amojo_token fresco) y `response.chats.session.account.id` (amojo_id). Cada nodo de envío llama primero a este endpoint → token sin expiración efectiva
- **Scope "Chats" puede no aparecer en la UI de Kommo** — ni al crear ni al editar integraciones privadas. Crear una nueva integración no ayuda. Solución: contactar `support@kommo.com` pidiendo habilitar el Chat API scope (según docs oficiales, debería estar disponible para integraciones privadas)
- **Webhook Kommo para mensajes entrantes WhatsApp** — seleccionar SOLO "Mensaje entrante recibido" en la config de webhooks. Seleccionar todas las acciones genera eventos `talk[update]` sin contenido del mensaje, y `add_message` puede no llegar
- **Long Lived Token: hasta 5 años pero sin refresh** — una vez expira hay que regenerar manualmente. OAuth2: access_token 24h + refresh_token 3 meses (rolling). n8n renueva OAuth2 automáticamente. Para workflows que solo usan la API REST de Kommo (leads, contacts), LLT a 5 años es suficiente. Para workflows que necesitan amojo API, usar OAuth2 con scope "Chats"
- **Long Lived Token requiere subdominio de la cuenta, NO `api-c.kommo.com`** — las llamadas API con LLT deben ir a `https://<cuenta>.kommo.com/api/v4/...`. Usar `api-c.kommo.com` devuelve 401 "Account not found" aunque el token sea válido
- **Task types NO se pueden crear vía API** — `POST /api/v4/tasks/types` devuelve 404/405. Solo se crean desde la UI de Kommo (Ajustes → Tareas → Tipos). Después se consultan con `GET /api/v4/account?with=task_types`
- **Testing workflows Kommo+WhatsApp** — simular el webhook de Kommo (`POST /webhook/<path>` con payload `add_message`) solo prueba la lógica del agente pero NO envía respuesta a WhatsApp ni aparece en Kommo. Para test end-to-end visible en Kommo se necesita inyectar mensajes via amojo API, que requiere scope "Chats". Sin ese scope, el único test end-to-end real es enviar WhatsApp manualmente desde un móvil

## Migración de workflows Kommo+n8n entre clientes

Al migrar workflows a una nueva instancia/cuenta, revisar y actualizar estos IDs en todos los workflows (no solo el principal):

1. **Sub-workflow IDs** — los workflows referenciados como herramientas cambian por instancia
2. **pipeline_id** — diferente por cuenta Kommo
3. **status_id** — diferente por cuenta Kommo
4. **field_id** — campos personalizados de leads/contactos, diferentes por cuenta
5. **amojo_id** — hardcodeado en URLs `amojo.kommo.com/v1/chats/{amojo_id}/`, diferente por cuenta
6. **bot_id** — ID de salesbot, diferente por cuenta
7. **responsible_user_id** — ID de usuario Kommo, diferente por cuenta
8. **task_type_id** — ID de tipo de tarea, diferente por cuenta
9. **Google Calendar ID** — diferente por integración/cuenta
10. **Credenciales n8n** — verificar que los IDs de credenciales del workflow existen en la instancia destino

## n8n API — credenciales

- **`GET /api/v1/credentials` no expone valores reales** — lista nombre, tipo e ID pero nunca devuelve tokens ni passwords. No intentar extraer secrets por la API pública.
- **`POST /api/v1/credentials` crea credenciales** — body: `{name, type: "smtp", data: {host, port, secure, user, password}}`. Caracteres especiales (`$`, `{`, `}`, `~`, `)`) en passwords pueden fallar incluso con escaping — usar passwords alfanuméricos simples, misma regla que Docker Compose

## n8n API — actualización de workflows vía API

El endpoint `PUT /api/v1/workflows/{id}` solo acepta:

```json
{
  "name": "...",
  "nodes": [...],
  "connections": {...},
  "settings": { "executionOrder": "v1" },
  "staticData": null
}
```

Cualquier otro campo (`createdAt`, `updatedAt`, `active`, `binaryMode` en settings) devuelve error `"request/body must NOT have additional properties"`.

## n8n API — creación y activación de workflows

- `POST /api/v1/workflows` acepta los mismos campos que PUT (`name`, `nodes`, `connections`, `settings`). Los workflows nuevos **nacen `active: false`**
- Activar con `POST /api/v1/workflows/{id}/activate` (endpoint separado, no se puede hacer en la creación)

## Set nodes y pérdida de datos en downstream

- **Un nodo Set que extrae campos de `$json.body.args.*` reemplaza `$json`** — los nodos posteriores (tras Switch, IF, etc.) ya no tienen acceso a `$json.body` original. Fix: referenciar el nodo fuente directamente con `$('Webhook').first().json.body.args.X` en vez de `$json.body.args.X`.

## `onError: continueRegularOutput` — formato del error

- **En non-2xx el output NO es `{statusCode, body}`** — es `{error: {message: "404 - \"{...}\"", name: "AxiosError"}}`. Parsear status code con `msg.match(/^(\d{3})/)` y detectar errores conocidos con `msg.includes('client_not_found')`. Sin esto, `item.statusCode || 200` defaulta a 200 y el error pasa como éxito.

## Tests contra webhooks de producción

- **Un POST de test a un webhook real dispara acciones reales** (Slack, email, Sheets, Calendar) — antes de testear, verificar que la cadena no notifica al equipo o usar datos que no activen las ramas con side effects. Si no es posible, avisar al equipo antes.

## Webhooks con respuesta síncrona del agente

- Para chats web o cualquier consumidor HTTP que necesite la respuesta del AI Agent en la misma request: en los parámetros del nodo Webhook usar `"responseMode": "responseNode"` **y** añadir un nodo `respondToWebhook` al final del flow con el output del agente
- Sin esto el webhook devuelve `{"message":"Workflow was started"}` al instante y el cliente no recibe la respuesta real

## Google Sheets tool — mapping de columnas

- Con `mappingMode: "defineBelow"`, el campo `columns.value` **debe tener mapeo explícito por columna**: `$fromAI('NombreCampo', 'descripción', 'string')` para datos que el agente extrae, o literal para columnas fijas (Fecha, Estado, Channel)
- Si `columns.value: {}` (vacío) las filas se insertan **en blanco sin error** — pérdida silenciosa de datos. El workflow de WhatsApp tiene este bug heredado, revisar si hay que arreglarlo

## AI Agents n8n — reglas críticas del system prompt

- **Los nombres de herramientas en el prompt deben coincidir EXACTAMENTE con los `name` de los nodos tool**. Si el prompt dice `"Agendar"` pero el nodo se llama `"Reservar"`, el LLM no encuentra la tool y **salta la llamada silenciosamente, sin error**. Verificar siempre que cada tool referenciada en el prompt existe como nodo con el mismo nombre
- **`memoryPostgresChat` NO persiste tool calls**, solo mensajes user/assistant. El agente **re-ejecutará** tools de escritura (Sheets append, Slack notify, Calendar create) en turnos posteriores aunque ya las haya llamado — porque la memoria no contiene evidencia de la llamada previa. Mitigación obligatoria: regla explícita en `<reglas>` del prompt listando las tools afectadas + una frase-ancla de cierre ("el equipo te llama en un ratito", "listo [nombre]") que el agente use para detectar que el flujo ya se cerró y no re-disparar
- **Corolario**: si el agente puede ejecutar una tool de escritura al oír "confirmo"/"perfecto" antes de tener todos los datos, añadir regla explícita "NUNCA llames a [tool] sin tener X, Y, Z". El agente rellena parámetros vacíos si no se le fuerza el orden
- **`toolHttpRequest` sin parámetros + GPT-4.1 = tool-calling ignorado** — el LLM produce el texto correcto pero no llama a las tools. Para acciones críticas (handoff, labels, asignaciones), usar marcador textual (`[HANDOFF]`, `[FIN]`) + lógica determinista en el workflow (IF + Code node) en vez de confiar en tool-calling del LLM
- **PGVector `Embeddings OpenAI` se conecta vía `ai_embedding`, no `ai_vectorStore`** — al crear conexiones por API, el tipo correcto es `{"ai_embedding": [[{"node": "VectorStore", "type": "ai_embedding", "index": 0}]]}`. Con `ai_vectorStore` n8n muestra error "No node connected to required input Embedding"
- **`$fromAI()` en toolCode puede lanzar "No execution data available"** (verificado en n8n 2.15.x) — usar la variable global `query` (string) que el AI Agent pasa al toolCode, y parsear los parámetros manualmente. El LLM puede enviar JSON, JS object literal o key-value por líneas — implementar parser que maneje los 3 formatos
- **`fetch` no existe en el sandbox de toolCode** — usar `this.helpers.httpRequest`. Funciona siempre que no se combine con `$fromAI()` (que es lo que rompe el contexto de ejecución)
- **`this.helpers.httpRequest` con `returnFullResponse: true` sigue lanzando excepción en non-2xx** — para manejar 404/400, usar sin `returnFullResponse` y parsear el status code desde `err.message` en el catch
- **`memoryPostgresChat` session key es el teléfono, no el conversation ID** — resolver conversación en Chatwoot NO limpia la memoria del agente. Para limpiar: `DELETE FROM n8n_chat_histories WHERE session_id = '<telefono>'`
- **Google Calendar tool con 0 eventos = todo libre** — cuando `getAll` devuelve 0 items para un rango, significa que no hay citas reservadas = todos los huecos dentro del horario están libres. Los LLMs interpretan lista vacía como "no hay disponibilidad". Añadir regla explícita en system prompt Y en la Think tool: "0 eventos = todos los huecos están LIBRES, ofrece el horario pedido"
- **Cálculo de fechas: incluir `$now.weekday` + fórmula + ejemplos** — los LLMs calculan mal la conversión día-de-semana→fecha (ej: "lunes" desde sábado 19 → calculó domingo 20 en vez de lunes 21). Fix: incluir `{{ $now.weekday }}` (1=lun...7=dom) en la Think tool + fórmula `días = objetivo - actual; si <=0 sumar 7` + ejemplos concretos + paso de verificación "¿coincide el día con la fecha?". También corregir offset estacional: +02:00 abril-octubre (CEST), +01:00 noviembre-marzo (CET)
- **Tool description de write-tools críticas: describir consecuencias** — una descripción genérica ("Usa esta herramienta para reservar cita", 74 chars) hizo que el LLM generara texto de confirmación sin ejecutar la tool. Expandir a ~280 chars explicando "sin esta llamada la cita NO queda registrada en el sistema" forzó la ejecución. Patrón: para toda tool que realice una acción irreversible, describir qué pasa si NO se llama
