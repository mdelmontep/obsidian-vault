---
title: Onboarding WhatsApp (agency-portal)
date: 2026-05-20
source: claude-code-session
tags: [agency-portal, onboarding, whatsapp, llm, agentesia]
---

# Onboarding WhatsApp — HUB

Flujo por el que un cliente nuevo de Agentesia rellena el alta vía conversación de WhatsApp con AIA. El operador prepara variables iniciales en el portal, el bot (LLM con tool calling `emit_turn`) conversa con el cliente, extrae datos a campos estructurados, y al cierre se genera un `.md` final + sincronización a la tabla `clients`.

## Componentes

| Pieza | Path | Función |
|---|---|---|
| Webhook entrada msgs | `src/app/api/onboarding/conversation/route.ts` | recibe mensajes desde Chatwoot/n8n, resuelve sesión por `chatwoot_conversation_id` / `session_id` / phone, llama `handleOnboardingMessage` |
| Webhook eventos n8n | `src/app/api/webhooks/whatsapp-onboarding/route.ts` | research_complete / session_started / response / conversation_complete |
| Núcleo conversación | `src/lib/onboarding/conversation.ts` | llama OpenAI con tool `emit_turn`, persiste `client_onboarding_responses` |
| System prompt | `src/lib/onboarding/system-prompt.ts` | catálogo de campos por sección + reglas + dinámicas según intake |
| Tool schema | `src/lib/onboarding/llm-tool-schema.ts` | JSON schema strict de `emit_turn(reply_text, extracted_fields, upsell_interest, is_complete)` |
| Sync a clients | `service.ts:syncOnboardingToClient` + `autoSyncSafeField` | mapea `field_key` → columna `clients` |
| .md final | `src/lib/onboarding/document.ts` (`buildOnboardingMarkdown`) | descarga vía `GET /api/onboarding/[id]/document` |
| Notify completion | `notify-completion.ts` | Slack + in-app + email cuando `is_complete=true` |
| UI tab | `src/app/(portal)/agency/clients/[id]/onboarding-tab.tsx` | progreso por sección, fields checklist, botón Sincronizar |

## Tablas Supabase

- `client_onboarding_sessions` — sesión: status (`pending_review`/`approved`/`in_progress`/`completed`/`cancelled`), `intake_variables`, `active_modules`, `plan_tier`, `chatwoot_*_id`, `upsell_interest`, `final_document_md`, `bot_paused_at`, `closed_manually`.
- `client_onboarding_responses` — UPSERT por `(session_id, field_key)` con `value`, `mapped_to`, `source ∈ {whatsapp, research, manual, operator}`.
- `onboarding_messages` — transcripción rol/contenido/timestamp + adjuntos.

## Modelo de campos

Tres prioridades en el catálogo (`ONBOARDING_FIELDS_BY_SECTION` en `types.ts`):
- **[C] Crítico** — sin esto no se puede construir. Bot DEBE cubrirlos antes de cerrar.
- **[N] Normal** — calidad. Bot intenta cubrirlos todos; repaso obligatorio antes de cerrar (regla 10 desde 2026-05-20).
- **[O] Opcional** — solo se extraen si surgen espontáneamente; no se preguntan.

Denominador del progreso UI (`ONBOARDING_SECTION_EXPECTED`) cuenta `[C]+[N]`, no `[O]`.

## Mapeo extracción → clients (gotcha histórico)

Las claves de `ONBOARDING_AUTO_SYNC_MAP` / `MANUAL_SYNC_MAP` (`types.ts`) **DEBEN coincidir** con los `field_key` que el LLM produce en `emit_turn` (definidos en `EXTRACTION_INSTRUCTIONS` de `system-prompt.ts`). Antes del PR #72 (2026-05-20) las claves estaban desincronizadas — el bot extraía `descripcion` pero el mapa esperaba `descripcion_corta`, `telefono` vs `telefono_whatsapp`, `web` vs `pagina_web`, etc. Resultado: pulsar **Sincronizar** producía UPDATE casi vacío en `clients`. Ver [[Stack/incidents]] entrada 2026-05-20.

Fix de diseño: comentario en el mapa que recuerda esta dependencia. Cambio futuro de un `field_key` en el catálogo del prompt requiere update en el mapa en el mismo PR.

## .md final — qué contiene

`buildOnboardingMarkdown` arma el `.md` con (en orden):
1. Header (nombre cliente, fecha, plan, módulos activos, WhatsApp).
2. Variables iniciales del operador (`renderIntakeContext`).
3. Investigación automática n8n (`research_data`).
4. Una sección por cada sección activa (módulos) + campos rellenados.
5. Secciones extra que llegaron del bot fuera del scope activo.
6. Interés en upsell detectado.
7. **Transcripción completa de WhatsApp** (añadido PR #72) — para máxima fidelidad de lo que el LLM no marcó como `extracted_fields`.
8. Footer con timestamp.

## Pausa/reanudación bot

`bot_paused_at` not null → el operador ha tomado el control (vista de mensajes en `onboarding-chat-realtime.tsx`). Acciones: `pauseBotAction` / `resumeBotAction` / `sendOperatorMessageAction` (operator escribe directo). Idempotencia de mensajes por `wa_message_id`.

## Auto-sync vs Manual-sync

- **Auto** (`autoSyncSafeField` desde webhook `event_type='response'`): campos seguros (nombre, contacto, web, horarios, agente) se mergean a `clients` en cuanto el bot los extrae. Sin acción del operador.
- **Manual** (`syncOnboardingToClient` desde botón UI): incluye los sensibles fiscales/legales (`razon_social`, `nif_cif`, `domicilio_fiscal`, `registro_mercantil`, `email_legal`).

`razon_social → fiscal_name` (no `legal_name`) desde PR #72: es la columna que consumen facturas, quotes, prospects y la UI del cliente.

## Notas operador → triggers dinámicos

`intake_variables.additionalNotes` se inserta en el prompt como instrucción del operador. Desde PR #72: si la nota menciona web/landing/sitio/página y `modules.web=false`, `additionalServiceRules` añade al prompt un bloque pidiendo al bot recoger dominio, colores, referencias y CTA antes de cerrar.

Patrón replicable para futuros servicios adicionales: detectar keyword en notas + añadir bloque condicional al prompt.

## Trade-offs de diseño actuales

- **[O] no se piden** (regla 2 prompt) — visibles en UI solo si están rellenados, lo demás como contador colapsado "+ N opcionales".
- **Cliente puede decir "luego"** — bot apunta y recapitula al cierre (reglas 9+10). No insiste turno a turno.
- **`is_complete=true` solo tras repaso [N]** — bloqueado por regla 10. Aunque el cliente diga "nada más" antes de tiempo, bot devuelve el repaso primero.

## Modelo LLM

`gpt-4o-2024-11-20` pinned (`conversation.ts:25`). NO alias `gpt-4o` para evitar drift de snapshots. Próxima revisión 2026-Q3. Timeout 20s (subworkflow n8n tiene 25s).

## PR #72 — fix sesión 2026-05-20

`fix/onboarding-sync-and-md-fidelity`. Tres bloques:
1. Alineadas 21 claves de `ONBOARDING_AUTO_SYNC_MAP` / `MANUAL_SYNC_MAP` con los `field_key` reales del LLM. `razon_social → fiscal_name`.
2. Transcripción WhatsApp añadida al `.md`.
3. `additionalServiceRules` para preguntar por web cuando lo indican las notas.

Segundo commit en el mismo PR (1+2 sobre [O]/[N]):
- UI: oculta `[O]` no rellenados (counter colapsado).
- Prompt regla 2: `[N]` = objetivo de calidad.
- Prompt regla 9: pendientes recapitulan en cierre.
- Prompt regla 10: repaso `[N]` obligatorio en bloque (máx 5/msg, 3 salidas: ahora/te lo busco/luego) antes de `is_complete=true`.

Smoke pendiente: nuevo onboarding real → ver `clients` poblado tras Sincronizar + `.md` con transcripción + bot pregunta web con nota operador + bot hace repaso `[N]`.

## Decisiones relacionadas

- [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding]] — por qué `emit_turn` tool calling en vez de JSON schema strict en `response_format`.

## Links

- HUB cliente: [[00-home/agentesia]]
- Incidente: [[Stack/incidents]] 2026-05-20 sync map
- Workflow n8n: [[Stack/n8n]] router con TTL 30d (ítem NEXT en top-of-mind)
