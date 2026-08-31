---
title: retell voice SDK — patrones y reglas
date: 2026-04-20
source: claude-md-migration
tags: [retell, voice, sdk, webhooks]
---

# Stack Retell / Voice SDK

- **Conversation Flow API — sin prefijo de versión** — `GET /get-conversation-flow/{id}` y `PATCH /update-conversation-flow/{id}`. Los paths `/v1/` o `/v2/` dan 404. El PATCH acepta solo el campo a cambiar (e.g. `{"global_prompt": "..."}`), no el objeto completo del flow.

- **`RetellWebClient` extiende `eventemitter3`** — tiene `.off(event, handler)`. Los listeners registrados en `useEffect` se acumulan entre remounts (HMR en dev o Strict Mode) si no los limpias. Guardar handlers como referencias con nombre y llamar `client.off(...)` en el cleanup:
  ```tsx
  const onStarted = () => { ... }
  client.on("call_started", onStarted)
  return () => client.off("call_started", onStarted)
  ```
- **Pre-check de micrófono con `navigator.mediaDevices.getUserMedia({ audio: true })`** antes de `startCall` → distingue `NotAllowedError` (permiso denegado) y `NotFoundError` (sin micro) con mensajes útiles para el usuario, en vez del error genérico del SDK que llega después
- **Timeout de seguridad en estado `connecting`** (10-15s) — si Retell no dispara `call_started`, el estado queda colgado indefinidamente. El orb late eterno y el usuario no entiende qué pasa
- **Singleton lazy del cliente** (`getRetellClient()` con try/catch que instancia en primer uso) evita crashes al cargar el módulo si el navegador no soporta WebRTC o mediaDevices
- **Normalizar la respuesta del webhook de Retell** — puede venir como `access_token`, `accessToken` o `token` según cómo lo construyas en n8n. Hacer `data.access_token ?? data.accessToken ?? data.token`
- **API de Retell — endpoints separados**: lectura con `GET /get-agent/{agent_id}` y `GET /get-retell-llm/{llm_id}`. Escritura con `PATCH /update-agent/{agent_id}` (voz, webhook) y `PATCH /update-retell-llm/{llm_id}` (prompt y tools). NO existe `/v2/agent/` — la API es v1 sin prefijo. El `llm_id` está en `response_engine.llm_id` del agente
- **`parameter_type` en custom tools debe coincidir con n8n**: si n8n lee `$json.body.args.X` (JSON anidado), la tool debe usar `"json"`. Con `"form"`, n8n recibe `body['args[name]']` en vez de `body.args.name` — la reserva falla silenciosamente
## API — importación y configuración

- **Importar agente JSON requiere crear LLM y agente por separado** — `POST /create-retell-llm` primero, después `POST /create-agent` con el `llm_id` devuelto. Eliminar campos read-only: `agent_id`, `version`, `is_published`, `last_modification_timestamp`, `llm_id`.
- **`voice_id` debe ser un ID válido de `GET /list-voices`** — formato: `{provider}-{name}` (ej: `cartesia-Isabel`). Filtrar por `accent: "Spanish"` para voces en español.
- **`transfer_call` funciona via JSON/API** — definir como tool con `type: "transfer_call"`, `name: "transfer_call"`, `number: "+34..."`.
- **Prompts de voz: priorizar concisión** — (1) URLs por nombre natural, solo deletrear si el cliente pide la dirección exacta, (2) no repetir lo que el cliente dijo — "Vale" basta, (3) tras confirmar dato, siguiente paso directo sin relleno.

- **Checklist antes de subir prompt Retell → n8n**:
  1. URLs de tools apuntan al dominio correcto (verificar DNS — EasyPanel y dominio custom pueden ser IPs distintas)
  2. Cada tool referenciada en el prompt existe en `general_tools` **y se nombra por su `name`, no por su `type`** — el modelo solo ve el `name`. El ejemplo clásico (`transfer_call`) esconde el fallo porque ahí los dos coinciden; con una tool `{type: "end_call", name: "colgar"}`, un prompt que ordena «cuelgas con `end_call`» nombra una función que el modelo no tiene (28-ago, Elphis Psicología). Cruza la lista en los **dos** sentidos: cableada sin nombrar, y nombrada sin cablear. Ver [[un-repo-coherente-consigo-mismo-no-prueba-el-nombre-que-vive-fuera]]
  3. Nombres de parámetros coinciden con los `Edit Fields` / `Set` del workflow n8n
  4. El workflow destino está activo y no archivado
  5. `parameter_type` es `"json"` si n8n espera `body.args.X`

## Migraciones de versión

- **API v3 list-calls (desde ~2026-06)** — `POST /v3/list-calls` (deprecated `/v2/`). Response: `{ items: RetellCall[], pagination_key?: string, has_more: boolean }` (antes array plano). Paginar con `has_more + pagination_key`, no `batch.length < LIMIT`.
- **retell-sdk 5.38.0: `webhook_auth` eliminado** — `/lib/webhook_auth.js` ya no existe. Reimplementar con `crypto.createHmac('sha256', apiKey).update(rawBody).digest('hex')` + `crypto.timingSafeEqual`. Ver [[retell-webhook-firma-hmac-body-mas-timestamp]].

## Versionado y publicación (agent + conversation flow)

- **`GET /get-agent/{id}` SIN `?version=N` devuelve el DRAFT más reciente, no lo publicado** — puede llevar meses sin publicar (visto real: un draft de junio idéntico al publicado, nunca tocado). Para saber qué versión usan las llamadas reales: `GET /list-agents`, filtrar por `agent_id` y coger la de `is_published: true` con el `version` más alto.
- **`PATCH /update-agent` y `PATCH /update-conversation-flow` sin `?version=N` editan el DRAFT en el sitio** (no crean uno nuevo si ya hay un draft sin publicar) — **antes de editar un draft heredado, diferéncialo contra el publicado** (`nodes` node-a-node): si es idéntico, es seguro construir encima; si no, hay trabajo ajeno sin publicar que no debe perderse a ciegas.
- **`PATCH /update-conversation-flow/{id}?version=N` sobre una versión YA publicada da 400** `"Cannot update published conversation flow"` — solo se puede patchear el draft (omite `version` o usa el número del draft, nunca el del publicado).
- **`POST /publish-agent/{id}` publica la versión que acabas de patchear Y abre un draft nuevo encima** — tras publicar, `list-agents` muestra dos filas `is_published: true` (la vieja publicada sigue marcada así en el histórico) — la que importa es la de mayor `version`. Verificar con `GET /get-agent/{id}?version=N` explícito, no fiarse del default.
- **`PATCH /update-conversation-flow` en el campo `nodes`: hay que mandar el array COMPLETO**, no solo el nodo que cambia — es reemplazo, no merge. Sacar la lista de "Valid Body Fields" con la doc oficial (`global_prompt`, `nodes`, `start_node_id`, `tools`, `model_choice`... — NO `conversation_flow_id`/`version`/`is_published`, son de solo lectura) y filtrar el objeto a esos campos antes de enviarlo.
