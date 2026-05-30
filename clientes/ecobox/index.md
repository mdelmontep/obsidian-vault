---
title: EcoBox HUB
date: 2026-05-26
tags: [cliente, ecobox, hub]
---

# EcoBox 360 — HUB

Cliente AgentesIA · Taller de chapa y pintura + mecánica rápida · Las Rozas (Madrid). Onboarding 2026-05-20, despliegue 21-22, voz E2E funcional 2026-05-25.

## Identidad

- **Razón social**: ECOBOX 360 S.L · CIF B27609114
- **Domicilio**: Calle Rotterdam 3, 28232 Las Rozas (Madrid)
- **Contacto**: Cristian Sánchez Alonso — cristian@ecobox360.es
- **Web**: www.ecobox360.es
- **WhatsApp actual (app móvil personal)**: +34 636 521 315 (NO migrar — se queda con Cristian)
- **Slug interno**: `ecobox`

## Stack final desplegado

| Pieza | Detalle |
|---|---|
| Dokploy dedicado | `https://ecobox.agentesialabs.com` · server Stackscale `185.99.186.132:5251` |
| n8n self-hosted | `https://n8necobox.agentesialabs.com` · postgres17 + redis7 + n8n 2.18.7 |
| Chatwoot **dedicado EcoBox** | `https://chatecobox.agentesialabs.com` (pivot 2026-05-22: pasó de compartido a propio) |
| Retell agent voz | `agent_250ae0d683b8086fdcaaed9027` — Alex — modelo del flow `gpt-4o` (cambiado desde gpt-4.1 por latencia) |
| Retell Conversation Flow | `conversation_flow_5f455ab09cf4` — Rigid, 13 nodos, 4 tools custom |
| Retell KB | `knowledge_base_34f85cf8295d3369` — 11 chunks info taller |
| Número Retell inbound | **`+34919932797`** asignado al agente Alex (Zadarma SIP) |
| Voz | `custom_voice_ba7fd23dc476d2ac821f8edd10` **Pablo Fernández** ElevenLabs (tras descartar "Borja" 9cdd… por estar mal etiquetada — sonaba femenina pese al nombre) |
| Número transfer humano | **`+34617314938`** (definitivo Cristian, era placeholder +34636521315) |
| 1Password vault | "EcoBox" en agentesialab — 9 items |

## Estado workflows n8n (2026-05-25)

| WF | ID | Estado | Notas |
|---|---|---|---|
| Chatwoot Bot Alex | `lv7pee2XAU5OngOB` | ACTIVO | v1 sin tools (chat aún sin migrar) |
| Mirar_disponibilidad | `iO9m2aSifPYY9LuA` | **ACTIVO** | `alwaysOutputData=true` en GCal getAll (calendar vacío rompía downstream). Smoke OK |
| Reservar_cita | `bJwoFHSBO6BK7gUe` | **ACTIVO** | Guard `Validate input` (rechaza `{{from_number}}` literal y años !=2026/2027) + crypto module fix (FNV-1a puro en `Gen GCal event ID`) + fallback `phone` desde `call.from_number` cuando arg es placeholder/vacío + `onError: continueRegularOutput` en Email cliente (skip si no destinatario) + `Respond OK` corto sin doble readback |
| Buscar_reserva | `HHryz8eDv3GOxZMF` | **ACTIVO** | **Reescrito**: ya NO usa Chatwoot search (devolvía "Authorization failed for bots"). Ahora busca directo en GCal `q` por `+34XXX` con `timeMin=now`. Devuelve `event_id` |
| Cancelar_cita | `L2W64JNIQmd0IJLV` | **ACTIVO** | **Simplificado**: borra por `event_id` que viene de Buscar_reserva. Garantiza cancelar SOLO esa una, deja resto del histórico intacto. `onError: continueRegularOutput` |
| Recordatorios cron 48h+24h | `QVPf25PZyLv0UHII` | inactivo | depende de Meta token + plantillas HSM aprobadas |
| Meta token health check | `Jbf5rZepHYM21MPQ` | inactivo | depende de Meta token |
| TEST Email Templates | `DogJ9b1iOHmJeS2S` | ACTIVO | webhook `/test-email-templates` — verificado envío real |

## Credenciales n8n (10)

| Tipo | Cred ID | Notas |
|---|---|---|
| Google Calendar OAuth | `LbmjQyqyDIWblulm` | Cuenta `ecobox360taller@gmail.com` — autorizado 2026-05-25 |
| OpenAI | `O7HC4LlEMW9qnNs9` | rotado 2026-05-22 |
| Postgres EcoBox interno | `QFMXn2QCNc74b4Us` | |
| Redis EcoBox interno | `2DcMeBcStZb57rcI` | |
| Chatwoot Bot Header (EcoBox dedicado) | `n8Zq72EUU23qB9cp` | |
| Chatwoot Admin Header (EcoBox) | `XP8mZAkDC0QRQNMI` | |
| Chatwoot Bot Header (legacy compartido) | `09Sm4jv8M6R6RcGG` | sin uso |
| SMTP Gmail | `BqK8VZqSh1ylDONz` | **App password** `ecobox360taller@gmail.com` — FROM = `EcoBox <ecobox360taller@gmail.com>` (cambio a `notificaciones@ecobox360.es` requiere Send-As alias o Workspace) |
| Meta WhatsApp Bearer | `dczhQTAKaeGVe1gr` | PLACEHOLDER — pendiente token Meta |
| Telegram | `ramEttKmAly4wflv` | PLACEHOLDER — descartado (sin Telegram alerts) |

## Google Workspace EcoBox

- Cuenta operativa: `ecobox360taller@gmail.com` (2FA + app password generada)
- **GCAL_ID**: `ecobox360taller@gmail.com` (calendario principal — no se creó "Peritajes" dedicado por petición del cliente)
- **DRIVE_FOLDER_FOTOS**: `1yrD1PlG9H42tKQSfWfFLZNPqL66fM2Eo`
- Drive/Sheets APIs habilitadas en el GCP project (pero no se usan en el stack final — pivot a Chatwoot dedicado)

## Pipeline conversacional Alex (voz — operativo)

```
n-welcome ("Hola, soy Alex de EcoBox, ¿en qué te puedo ayudar hoy?")
  → n-extract-1 (intent + nombre)
  → n-classifier
    ├─ nueva_cita
    │   → n-collect-damage (subagent: nombre, daño, coche, matrícula, seguro si aplica)
    │   → n-collect-date (subagent + Mirar_disponibilidad: OBLIGATORIO consultar agenda real)
    │   → n-confirm-cita (subagent + Reservar_cita: confirma teléfono "¿te guardo este número?" → resumen → reserva → confirmation_text corto)
    │   → n-end-cita
    ├─ gestionar_cita (subagent + Buscar_reserva + Cancelar_cita)
    │   ├─ CASO A cancelar → pregunta "¿con este nº o con otro?" → Buscar → confirmar → Cancelar by event_id → fin
    │   ├─ CASO B cambio fecha → "mándanos un mensaje por WhatsApp" (NO transfer)
    │   ├─ CASO C ¿cómo va? → pide matrícula → "déjame consultar..." → "están avanzando, te avisarán" → solo transfer si insiste
    │   └─ CASO D pide humano explícito → transfer
    ├─ info_rapida → KB
    └─ humano / fuera idioma → transfer +34617314938
```

## Decisiones clave acumuladas

- [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo]] — Chatwoot **dedicado** EcoBox (2da revisión: compartido → propio)
- [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode]] — Rigid €0.135/min
- **Notificaciones** = nativas Chatwoot (sin Telegram)
- **Email** solo en chatbot WhatsApp (por voz es incómodo). Por voz solo va email a Cristian (alert interno)
- **Plantillas email**: 2 (confirmación cliente HTML + alert Cristian)
- **Recordatorios HSM 48h/24h**: descartados (workflows desplegados pero inactivos)
- **Sin Sustitución / Recogida** ofrecidas por iniciativa de Alex — solo si el cliente las pregunta
- **Voz**: probadas en orden 11labs-Santiago, cartesia-Manuel, custom Borja, **custom Pablo Fernández** (final)
- **Modelo flow**: `gpt-4o` (más rápido que gpt-4.1, suficiente para Rigid)
- **Latencia**: `responsiveness=1.0`, `enable_backchannel=true` con "ajá/vale/claro", `begin_message_delay_ms=500`

## Meta WhatsApp Cloud API (LIVE 2026-05-28)

Número `+34 910 05 48 13` (provider Netelip) llegó CONNECTED + CLOUD_API + VERIFIED tras 3h de iteración:
1. WABA original (`1277706597676685`) + Phone original (`1124445220757479`) quedaron huérfanos cuando Cristian desvinculó el número de la app móvil WhatsApp Business (Meta hizo auto-cleanup que invalidó las referencias — el token retuvo validez pero perdió acceso a esos objects).
2. User recreó WABA + Phone vía API en mismo Portfolio — IDs nuevos abajo.
3. PIN 2FA custom seteado vía `POST /register`.
4. 3 plantillas HSM creadas (PENDING review Meta).

| Activo | ID |
|---|---|
| Portfolio empresarial | `1011127821491282` |
| **WABA actual** (Ecobox 360) | `1488289103073845` |
| **Phone Number ID actual** | `1136826222847102` (`+34 910 05 48 13`, CLOUD_API, CONNECTED, VERIFIED) |
| WABA huérfana (legacy) | ~~`1277706597676685`~~ |
| Phone huérfano (legacy) | ~~`1124445220757479`~~ |
| Message template namespace | `7049d1fc_3cb6_4dd5_b2fa_168acb7376ef` |
| System User `ecobox-api` (control total) | `61590397051384` |
| App Meta `Ecobox360` | App ID `1643186026903792` |
| **Token permanente + PIN 2FA** | `Ecobox/.credentials.local` (`META_PERMANENT_TOKEN`, `META_PHONE_PIN`). Pendiente espejar a 1P EcoBox cuando sesión `op` se reabra. |
| Plantillas HSM (PENDING review) | confirmacion_cita_ecobox `980688254703968` · recordatorio_48h_ecobox `2117110505903801` · recordatorio_24h_ecobox `2156080465190409` |
| App Secret / Verify Token webhook | NO entregados — solo bloquean INBOUND (cliente WhatsApp → bot). Outbound (recordatorios + confirmaciones) ya funcional. |

## Bloqueadores externos restantes

1. ✅ ~~Crear WABA + Permanent Access Token Meta~~ — hecho 2026-05-28.
2. ✅ ~~Migrar +34910054813 a Cloud API + verificación~~ — DONE 2026-05-28 (vía recreación WABA + Phone tras desvincular app móvil).
3. ⏳ **Esperar aprobación HSM Meta** — 3 plantillas en PENDING desde 2026-05-28 (UTILITY suele aprobar <1h). Cuando aprueben, activar workflows `Recordatorios cron` (`QVPf25PZyLv0UHII`) y `Meta token health check` (`Jbf5rZepHYM21MPQ`) tras actualizar cred n8n `dczhQTAKaeGVe1gr` con el token.
4. ⏳ Regenerar API key n8n (la del `.credentials.local` devuelve 401 desde el PUT bot v2). Sin esto no puedo actualizar la cred Meta Bearer ni validar bot v2 E2E.
5. ⏳ App Secret + Verify Token webhook Meta — solo necesario cuando activemos inbound (cliente WhatsApp → bot Chatwoot). Outbound ya operativo.
6. ⏳ Conectar inbox Chatwoot al Phone Number ID `1136826222847102` (Chatwoot Cloud channel WhatsApp). Sin esto, ningún mensaje cliente llega al bot.
7. ⏳ Logo PNG público + color marca hex (defaults `#0F1B2D` + `#E76F51`) + firma email.
8. ⏳ URL Google Maps corta de Rotterdam 3.
9. ⏳ Confirmar definitivamente cómo gestionar "cómo va mi reparación" — Alex finge consulta hoy.

## Learning capturado 2026-05-28

- [[meta-waba-orfana-tras-desvincular-app-movil-recrear-via-api]] (NUEVO) — al eliminar la cuenta WhatsApp Business app, Meta puede dejar la WABA + Phone Number en estado huérfano (token válido pero `Object does not exist` en Graph API). Solución: recrear via API directamente, no esperar a que Meta libere los IDs antiguos.
- [[whatsapp-cloud-api-vs-business-app-numero-exclusivo]] ya confirmado con caso real: un número en app móvil aparece como `platform_type=ON_PREMISE + status=DISCONNECTED` aunque no esté en On-Premise legacy real.
- [[chatwoot-3x-whatsapp-cloud-display-phone-number-bug-doble-plus]] — Chatwoot 3.x `Webhooks::WhatsappEventsJob#get_channel_from_wb_payload` concatena `"+"` siempre al `display_phone_number`. Meta real envía sin `+` así que no afecta producción, pero rompe simulaciones curl con `+` literal.

## Fixes 2026-05-29 — Smokes chat tool calls

**Bug 1 — Bot Chatwoot llama tools con args NULL** (4 agentes en consenso). Causa raíz: `parameters.jsonBody` envuelto en `={{ JSON.stringify({...}) }}` global con todos los `$fromAI()` dentro. n8n langchain 1.9 NO puede extraer schema individual desde esa sintaxis. El LLM ve la tool como `query: {}` opaco → llama con objeto vacío. Retell funciona porque define JSON Schema explícito con `required:[...]`. **Fix aplicado**: los 4 `toolHttpRequest` (`mirar_disponibilidad`, `reservar_cita`, `buscar_reserva`, `cancelar_cita`) ahora tienen `jsonBody` literal JSON con `"={{ $fromAI('field', 'desc', 'type') }}"` por valor. Learning para vault: [[n8n-langchain-toolhttprequest-jsonbody-no-envolver-en-jsonstringify-global]].

**Bug 2 — Workflow Reservar_cita acepta args null y miente al bot**. Cuando args null: Edit Fields colapsa todo a null, GCal create falla con "Bad request" pero `onError: continueRegularOutput` deja seguir, Respond OK devuelve `"Listo, . Te llega un WhatsApp"` con coma huérfana, emails se envían con basura. **Fix aplicado**: nuevo nodo `Validate input` después de Edit Fields con 3 conditions AND (name notEmpty, matricula notEmpty, preferred_date startsWith "2026"). Si rechaza → `Respond ValidateError` con `confirmation_text` instructivo que el bot lee al cliente. Learning para vault: [[n8n-workflow-validate-input-guard-evita-mentir-cuando-bot-manda-null]].

**Bug 3 — Edit Fields sin optional chaining colapsa todo a null cuando body no tiene `args` wrapper**. Las expresiones usaban `$json.body.args.name || $json.body.name || 'Cliente'`. Cuando el bot chat manda directo `body.name` (sin `args` wrapper), `body.args.name` lanza `TypeError: Cannot read property 'name' of undefined` y n8n silently devuelve null. Por eso voz Retell (que sí wrapea `body.args`) funcionaba, chat no. **Fix aplicado**: cambiadas todas las expresiones de Edit Fields a `$json.body?.args?.name || $json.body?.name || 'Cliente'` con optional chaining. Learning para vault: [[n8n-expressions-optional-chaining-obligatorio-cuando-body-args-puede-faltar]].

**Smokes pasados tras los 3 fixes** (2026-05-29):
- Args null → workflow rechaza con `confirmation_text: "No pude reservar porque faltan datos..."` ✓
- Args válidos test mode (`matricula=ZZZ0000`) → entra a Respond TEST sin tocar GCal ✓
- Pendiente: smoke real desde Chatwoot bot con cliente final → debe crear evento GCal en `ecobox360taller@gmail.com` + enviar email

## E2E multi-perspectiva 2026-05-29 — verificación post-fixes

**4 agentes paralelos** (happy path chat, edge cases chat, voz Retell simulada via webhooks, auditor estado). Hallazgos:

- ✅ **Voz Retell funciona al 100%** — 6 tests webhook con formato `body.args + body.call` pasan + 2 citas reales creadas hoy en producción + flujo cancel E2E OK
- 🔴 **Bot Chatwoot rompía** — bot llamaba tool con `query:{}` y alucinaba "cita confirmada". Causa raíz: el `jsonBody` con expresiones `={{ JSON.stringify(...) }}` o `"={{ $fromAI }}"` o `"{{ $fromAI }}"` no se interpolaba — n8n mandaba el body LITERAL con las expresiones como strings al webhook. **Fix definitivo** (fix6): cambiar a `specifyBody: "keypair"` con `parametersBody.values[]` declarados uno por uno con `valueProvider: modelRequired/modelOptional`. Tras fix6, exec 197 confirmada con args reales + GCal event creado + emails HTML generados.

Learning para vault: [[n8n-langchain-toolhttprequest-specifybody-keypair-es-el-formato-correcto-para-fromai]] — solo `specifyBody: "keypair"` permite a n8n declarar el schema correcto al LLM. Las formas `json` con `JSON.stringify` o expresiones inline NO funcionan porque n8n no parsea las expresiones dentro del jsonBody string a menos que TODO el campo empiece con `=` (lo cual rompe el JSON literal).

Bonus de la auditoría: **plantillas HSM Meta ya APROBADAS** las 3 (`confirmacion_cita_ecobox_2`, `recordatorio_24h_ecobox`, `recordatorio_48h_ecobox`).

## Pendientes (al cierre 2026-05-29, post 6 fixes encadenados)

1. **Smoke real bot chat E2E del user** — conversación turn-by-turn desde WhatsApp `+34617314938`. El sistema YA está verificado E2E con POST simulado pero aún no con WhatsApp real (formato Meta entregando webhook completo). El POST simulado y el webhook real son idénticos en estructura, pero conviene confirmar.
2. **Smokes funcionales adicionales chat**:
   - Buscar reserva existente ("ver mi cita")
   - Cancelar cita ("cancela mi cita")
   - Info rápida ("a qué hora abrís", "dónde estáis")
   - Handoff humano ("quiero hablar con persona") → label `humano` aplicado
   - Pregunta fuera de scope ("hacéis ITV") → derivación
3. **Cron diario actualizar fecha en Retell flow**: el `global_prompt` tiene `"HOY es viernes, 29 de mayo de 2026"` hardcoded. Crear workflow n8n cron diario 00:00 Madrid que PATCH al flow Retell con fecha del día (formato `dddd, D de MMMM de YYYY` en español) + recordatorio de fin de semana cerrado si aplica.
4. **Recordatorios cron** (`QVPf25PZyLv0UHII`) tiene nodos `noOp` TODO send HSM. Implementar `httpRequest` POST a Meta Cloud API `/messages` con template `confirmacion_cita_ecobox_2` + nodo `postgres` que update `reminders_sent`. Activar cuando plantillas HSM aprueben.
5. **Plantillas HSM**: las 3 siguen PENDING review Meta desde 2026-05-28. Revisar cada hora. UTILITY simples suelen aprobar <24h.
6. **Meta health check** workflow (`Jbf5rZepHYM21MPQ`) tiene bug en nodo `IF error` ("Conversion error: string '' can't be converted to object"). El endpoint Meta /me responde 200 OK. El bug es del workflow, no del token. Cosmético — no urgente.
7. **App Meta en dev mode**: solo recipients autorizados (Manu `+34617314938`). Para clientes reales → publicar app (necesita URL privacidad → necesita web).
8. **App Secret + Verify Token Meta** para validar firma `X-Hub-Signature-256`. Chatwoot tolera sin esto pero es buena práctica. Añadir cuando haya web.
9. **Logo PNG + color marca hex + firma email + URL Maps Rotterdam 3** (Cristian).
10. **Decisión definitiva "¿cómo va mi reparación?"** — Alex finge consulta hoy.

## Cambios infra reciente

| Pieza | Antes | Después (2026-05-29) |
|---|---|---|
| LLM bot Chatwoot | gpt-4o-mini | **gpt-4o** (mismo que voz) |
| jsonBody tools bot | `JSON.stringify({...})` global | literal con `$fromAI` por valor |
| Edit Fields Reservar_cita | `body.args.X || body.X` (sin `?.`) | `body?.args?.X || body?.X` (optional chaining) |
| Reservar_cita workflow | sin validate input | + nodo `Validate input` + `Respond ValidateError` |
| Retell global_prompt | "HOY es lunes 25 de mayo" hardcoded | "viernes 29 de mayo" hardcoded (TODO: cron diario) |
| Retell n-confirm-cita | "PASO 4 — Reservar_cita" suave | "PASO 4 ← TOOL OBLIGATORIA NO TERMINES SIN EJECUTARLA" |
| Backup workflows pre-fix | — | `Ecobox/wf_bot_backup_pre_fix4.json` + `Ecobox/wf_reservar_backup_pre_fix4.json` + `Ecobox/retell_flow_backup_2026-05-29_pre_fix.json` |

## Bot Chatwoot v2 con tools (2026-05-28)

Workflow `lv7pee2XAU5OngOB` actualizado: 17 nodos = 13 originales + 4 `toolHttpRequest` (`mirar_disponibilidad`, `reservar_cita`, `buscar_reserva`, `cancelar_cita`) reusando los mismos webhooks que la voz Retell. System prompt v2 enseña al LLM cuándo usar / cuándo no usar cada tool. Text del agente inyecta `[ctx phone=… name=…]` dinámico desde Edit Fields para que el bot no pida el phone al cliente. Verificado via API (nueva key n8n regenerada): 17 nodos activos + 4 conexiones `ai_tool`. Falta smoke E2E con mensaje real cuando Meta termine handshake webhook.

## Chatwoot WhatsApp Cloud inbox (LIVE 2026-05-28)

| Activo | Valor |
|---|---|
| Inbox ID | `2` (Channel::Whatsapp, provider=whatsapp_cloud) |
| Phone | `+34 910 05 48 13` apuntando a Meta phone_number_id `1136826222847102` |
| Callback URL (la que va en Meta App → Webhooks UI) | `https://chatecobox.agentesialabs.com/webhooks/whatsapp/+34910054813` |
| Verify token (debe coincidir con Meta UI) | guardado en `.credentials.local` `CW_INBOX_WHATSAPP_VERIFY_TOKEN` |
| Account webhook (Chatwoot → n8n bot) | id=1, only `message_created`, HMAC secret guardado |
| Meta app suscrita a WABA | `POST /v18.0/1488289103073845/subscribed_apps` OK 2026-05-28 |
| Plantillas HSM importadas auto al crear inbox | 3 PENDING (confirmacion_cita, recordatorio_48h, recordatorio_24h) |

Webhook Meta UI (Manu) configurado 2026-05-28. Field `messages` suscrito. App en dev mode aún — entrega solo a WhatsApp de usuarios con rol app o en lista de recipients (campo "A" del use case). Por eso mensajes reales del user no llegaron hasta que confirmó número (+34617314938 era el suyo, no de Cristian — error de mi memoria, hub corregido).

**Pipeline E2E verificado**: POST simulado `FIX_1779984161` (2026-05-28 18:02) → conv id 6 creada en Chatwoot → bot Alex respondió "Parece que no tengo tu nombre completo. ¿Cómo te llamas?" (LLM funcionando con system prompt v2).

**Bug Chatwoot 3.x descubierto durante el debug**: `Webhooks::WhatsappEventsJob#get_channel_from_wb_payload` siempre concatena `"+"` al `display_phone_number` del payload (`"+#{metadata.display_phone_number}"`). Si el payload viene con `+` (como mis simulaciones curl), construye `"++34..."` → no encuentra channel → `channel.blank?` → return early silencioso. Meta real envía sin `+` según spec oficial, no afecta producción. Mover este learning a [[chatwoot-3x-whatsapp-cloud-display-phone-number-bug-doble-plus]] en próximo /obsidian-1.

## Bugs conocidos / cleanup pendiente

- ✅ ~~Eventos smoke acumulados en GCal `ecobox360taller@gmail.com`~~ — 5 borrados 2026-05-28 vía workflow oneshot `_cleanup_smoke_gcal` (1 en junio 2024 + 4 en mayo 2026). Re-run idempotente devuelve 0. Workflow oneshot eliminado tras éxito.
- ⏳ API key n8n empezó a devolver 401 tras PUT del bot v2 — healthz OK, webhooks OK, sólo `/api/v1/*` rechaza. JWT sin `exp` → probable rotación externa o restart del contenedor. Regenerar en `n8necobox.agentesialabs.com → Settings → API` y actualizar `.credentials.local` `N8N_API_KEY`.
- ⏳ Retell flow audit hallazgo menor: `global_prompt` y nodo `n-collect-date` tienen "2026" hardcoded — debería usar `{{ano_actual}}` (como ya hace `n-confirm-cita`). No bloqueante.

## Archivos locales

- `/Users/manueldelmonte/Ecobox/CLAUDE.md` — estado completo
- `/Users/manueldelmonte/Ecobox/ARQUITECTURA.md` — diseño Chatwoot
- `/Users/manueldelmonte/Ecobox/CHECKLIST_ARRANQUE.md` — 14 pasos para arrancar
- `/Users/manueldelmonte/Ecobox/email_templates.md` — 2 plantillas
- `/Users/manueldelmonte/Ecobox/email_previews/` — HTMLs navegables
- `/Users/manueldelmonte/Ecobox/whatsapp_templates.md` — sintaxis Meta `{{N}}`
- `/Users/manueldelmonte/Ecobox/.credentials.local` — IDs y tokens
- `/Users/manueldelmonte/Ecobox/retell_flow_backup_2026-05-25.json` — backup pre-restructure tools

## Learnings de esta sesión (2026-05-25/26)

- [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
- [[retell-tools-conversation-flow-require-tool-id-field]]
- [[retell-knowledge-base-api-requiere-multipart-form-data]]
- [[retell-subagent-nodes-dividen-agentes-monoliticos-en-especializados]]
- [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]]
- [[chatwoot-custom-attribute-definitions-endpoint-v3-renombrado]]
- [[chatwoot-bot-token-vs-admin-token-scopes-distintos]]
- [[chatwoot-search-contact-api-no-autorizada-para-bot-token]] (NUEVO 2026-05-25)
- [[n8n-network-external-true-falla-en-dokploy-sin-pre-create]]
- [[n8n-postgres-webhook-lastnode-solo-devuelve-primer-row]]
- [[n8n-public-api-google-oauth-schema-buggy-crear-en-ui]]
- [[n8n-crypto-module-bloqueado-en-task-runner-usar-fnv-puro]] (NUEVO 2026-05-25)
- [[n8n-public-api-no-permite-update-credentials-solo-post-delete]] (NUEVO 2026-05-25)
- [[n8n-respondtoWebhook-json-mode-requiere-expresion-objeto-no-literal]] (NUEVO 2026-05-25)
- [[n8n-gcal-getall-empty-no-propaga-downstream-usar-alwaysOutputData]] (NUEVO 2026-05-25)
- [[n8n-emailsend-onError-continueRegularOutput-skip-si-sin-destinatario]] (NUEVO 2026-05-25)
- [[n8n-gcal-create-additionalFields-description-escapar-newlines-no-backslash]] (NUEVO 2026-05-25)
- [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]
- [[gcal-eventid-charset-restriction-a-v0-9-base32hex]] (NUEVO 2026-05-25)
- [[gcal-q-search-no-encuentra-eventos-recien-creados-eventual-consistency]] (NUEVO 2026-05-25)
- [[retell-custom-voice-labels-pueden-estar-mal-etiquetadas-pese-al-nombre]] (NUEVO 2026-05-25)
- [[retell-from_number-no-auto-sustituye-en-tool-args-necesita-fallback-n8n]] (NUEVO 2026-05-25)
- [[retell-tool-call-strict-mode-no-fuerza-ejecutar-tool-solo-valida-args]] (NUEVO 2026-05-25)
- [[retell-zadarma-sip-no-popula-retell_llm_dynamic_variables-from_number]] (NUEVO 2026-05-25)
- [[llm-conversational-current-date-debe-inyectarse-explicito-en-prompt]] (NUEVO 2026-05-25)
- [[retell-boosted-keywords-stt-letras-españolas-zeta-efe]] (NUEVO 2026-05-25)
