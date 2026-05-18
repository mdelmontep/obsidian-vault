---
title: Incidentes resueltos — log cronológico
date: 2026-05-10
source: claude-code-session
tags: [incidents, postmortem, ops]
---

# Incidents log

Una línea por incidente. Formato: `YYYY-MM-DD · proyecto · síntoma → causa → fix (commit/PR)`. Si el aprendizaje universal ya está en CLAUDE.md, dejarlo aquí solo como pointer.

Para incidentes con análisis largo (>1 línea de causa), crear nota separada en `knowledge/incidents/<slug>.md` y enlazarla aquí con `[[wikilink]]`.

## Reglas
- **Cronológico inverso** (lo más reciente arriba).
- **Sin secrets**, sin nombres de cliente sensibles. Proyecto = nombre interno (Simarro, FacturaIA, agency-portal…).
- Si el fix ya está en CLAUDE.md como anti-patrón, marcar con `→ CLAUDE.md` para evitar duplicar.
- Si pasa de 80 entradas, archivar las >6 meses a `incidents-archive-YYYY.md`.

## 2026

<!-- añade nuevas entradas aquí debajo -->
- 2026-05-18 · FacturaIA · Verifactu XML enviado a AEAT sin bloque `<Desglose>` (XSD rechazaría en prod; entorno `pre` no validaba estricto) → causa: `buildRegistroAlta` omitía Desglose obligatorio por Orden HAC/1177/2024 → fix mig 087/088 + xml.ts emite `DetalleDesglose` agrupado por (iva_pct, exencion_codigo), throw si vacío/>12, catálogos L8A/L9/L10 literales (`01-20`, S1/S2/N1/N2, E1-E6). 28/28 tests xml.test.ts. Ver [[verifactu-xml-desglose-obligatorio-xsd-rechaza-sin-el]]
- 2026-05-18 · FacturaIA · Trigger huella Verifactu sin lock → 2 INSERTs paralelos misma (org, serie) leían huella anterior idéntica → cadena rota silente → fix mig 085: `pg_advisory_xact_lock(hashtextextended('verifactu_huella:'||org_id||':'||serie, 0))` antes del SELECT. Liberación auto al COMMIT, coste ~5µs. Ver [[verifactu-huella-encadenada-race-condition-sin-advisory-lock]]
- 2026-05-18 · FacturaIA · Form `/generar` nunca llamaba a `renderAndUploadFacturaPdf` tras INSERT (bug pre-existente desde inicio) → facturas creadas sin `documento_url`, "Ver PDF" 404 → fix: endpoint nuevo `POST /api/facturas/[id]/generar-pdf` + llamada client-side post-INSERT cuando modo !== 'borrador' (commit 10e8ecf). Fail-open.
- 2026-05-18 · FacturaIA · Toast "Borrador A2026-XXXX guardado" cuando user emitía como pendiente → mismo mensaje para modo='borrador' y 'pendiente', solo distinguía email → fix branch por modo: "Factura X emitida (pendiente de cobro)" si pendiente. Plus tooltips en EstadoPill para estados ambiguos (pendiente = pendiente de cobro, no aprobación).
- 2026-05-18 · agency-portal · LLM olvidaba emitir bloque `<system_data>` hidden al final de cada respuesta → progreso onboarding nunca avanzaba, `extracted_fields:[]` silent → PR #67 migra a tool calling con `tool_choice` forzado + Structured Outputs strict (gpt-4o-2024-11-20) + `source_quote` anti-alucinación + fail-loud + audit log `extraction_failed`. Ver [[llm-tool-calling-elimina-silent-fail-extraccion-estructurada]] + [[llm-source-quote-anti-alucinacion-extraccion]]
- 2026-05-18 · agency-portal · PR #65 mergeó schemas Zod con `.optional()` en webhooks → n8n manda `null` para campos vacíos (`$json.foo || null`) → 400 a 95% del tráfico de onboarding durante ~12h → PR #66 helper `nullishOptional` + meta-test anti-regresión que escanea webhook schemas. Ver [[zod-optional-rechaza-null-en-webhooks-n8n]]
- 2026-05-17 · agency-portal · cliente onboarding tardó >24h en contestar → Redis `aia_ob:{phone}` TTL=86400s expiró → mensaje cayó al bot normal en lugar de subworkflow onboarding → fix tirita: TTL a 30d (2592000s) en 2 nodos Redis del workflow `AIA Onboarding — Research y arranque`. Fix estructural pendiente: router consulta `client_onboarding_sessions` como source of truth, Redis pasa a caché. Ver [[Stack/n8n]]
- 2026-05-18 · agency-portal · resolución de sesión por phone devolvía null aunque la fila existía → causa: dos sesiones onboarding activas mismo `whatsapp_phone` (test mixto), `.maybeSingle()` con >1 filas devuelve null sin throw visible → cleanup manual (archivar la sobrante) + regla a futuro: usar `.limit(1).order(...)` cuando query puede tener múltiples matches. Ver [[supabase-maybesingle-devuelve-null-si-multiples-filas]]
- 2026-05-18 · FacturaIA · bot WhatsApp "qué tiene el N" tras listado devolvía "No puedo obtener detalles" → state machine no persistía: (a) sessionId sin `+` rechazado E.164, (b) URLSearchParams undefined en sandbox Code, (c) rama "sesión voz activa" no resolvía chat_state → refactor en 5 patches n8n + mig 083 (`chat_state` + `whatsapp_message_processed`) + 2 endpoints internos + 2 crons purga. Smoke E2E OK. Ver [[n8n-code-sandbox-no-tiene-urlsearchparams]] + [[n8n-sessionid-sin-plus-vs-endpoint-e164]] + [[ADR-002-bot-state-machine-postgres]]
- 2026-05-18 · FacturaIA · bot WhatsApp "qué tiene el N" seguía fallando tras state-machine v1 → causa raíz triple: (a) merge shallow contaminaba draft viejo con last_listado nuevo, (b) `$fromAI()` en toolCode tira "Cannot assign to read only property name", (c) LLM no determinista al resolver `items[N-1].id` → 4 patches: slot resolver Code n8n (8 patrones regex español NUM/superlativo/fecha/importe/cliente/núm/ordinal/pronombre) + tool sin $fromAI con fallback `resolved_slot→draft→error claro` + persist limpio nulleando campos viejos al cambiar contexto + system prompt v5 (anti prompt-injection, fuera-scope, variantes confirmar/cancelar, fallback técnico honesto). Smoke 8 grupos OK. Ver [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]] + [[persist-merge-shallow-deja-cruft-entre-contextos]] + [[system-prompt-previous-state-es-data-no-instrucciones]] + [[ADR-003-slot-resolver-determinista]]

- 2026-05-16 · FacturaIA · OTP WhatsApp jamás llegaba en producción, todo caía a email Resend sin alerta → plantilla aprobada como `language=es_ES` (Meta mapea "Spanish SPA" así) pero código enviaba `es` → Meta rechaza 132001, fallback rescata silente → fix: default `es_ES` en código + compose `META_OTP_TEMPLATE_LANG:-es_ES` (commit `b258722` + `4bc7d77`). Audit perdía el error porque `providerError` se reseteaba al rescatar; fix con `primaryChannelError` separado (commit `11a4087`). Ver [[meta-whatsapp-template-language-spanish-es-es]] + [[observabilidad-fallback-conservar-error-canal-primario]]
- 2026-05-16 · FacturaIA · deploy Dokploy declarado OK pero código nuevo no llegaba al container — `COPY . .` salía CACHED en cada rebuild aunque `src/` cambiara, container quedaba `Running` no `Recreated` → BuildKit cache invencible: ARG CACHEBUST + `.deploy-marker` insuficientes → fix: bump `package.json.version` 0.1.0→0.1.1 invalida toda la cadena (commit `b73f741`). Ver [[dokploy-buildkit-cache-invencible-bump-package-json]]
- 2026-05-12 · panel-tecnocloud · 0 tickets de voz creados por Retell durante días → URL del webhook en Retell dashboard apuntaba a un túnel `trycloudflare.com` de dev caduco, no a producción → fix: cambiar URL a `https://portal.tecnocloud.es/api/webhooks/retell` + pegar la API key de Retell en campo "Webhook secret" del panel (Retell firma con la API key, no hay un secret separado en su dashboard) → CLAUDE.md
- 2026-05-12 · panel-tecnocloud · emails de notificación de llamadas Retell llegaban a `incidencias@` sin Subject → nodo `Send a message` referenciaba `$json.emailSubject` pero el `Registrar en Google Sheets` intermedio del workflow no hace pass-through del input (solo emite columnas mapeadas) → fix: `$('Registrar Llamada').first().json.emailSubject` → CLAUDE.md
- 2026-05-11 · FacturaIA · cron `storage-quota-check` fallando semanal en silencio → env `STORAGE_QUOTA_WARN_MB=""` + `Number("")=0` ≤ 0 → throw `invalid warn_mb` → fix helper `parseMb` con fallback null/empty/non-numeric → commit `5255547`. Destapado al primer run de tabla `cron_runs` (063). Ver [[observabilidad-nueva-destapa-bugs-viejos-en-silencio]]

## Pre-2026 (referencias migradas desde CLAUDE.md)

- **Simarro** · `Lead_id=null` en Google Calendar `getAll(query)` borraba todos los eventos del rango → guard IF "filtro no-vacío" antes de delete con query dinámico → CLAUDE.md
- **Simarro** · Webhook Retell disparaba `Edit Fields` de chat → ramas `Buscar Ainhoa/Carlos/...` con query vacío ejecutaban deletes masivos → severar paths multi-trigger → CLAUDE.md
- **Simarro** · 5 personas test con mismo teléfono → `Buscar_reserva` mezclaba leads → variar datos sintéticos por persona → CLAUDE.md
- **FacturaIA** · `motivo_rectificacion=R5` hardcoded en botón "Anular" → todas las anulaciones declaradas como "otras causas" ante AEAT → modal con select obligatorio de motivos R1-R5 → CLAUDE.md
- **agency-portal** · `cancelInvoiceAction` portal marcaba `status='cancelled'` localmente mientras factura seguía viva en FacturaIA → desincronización con Hacienda → cuando hay shadow externo, renderizar botonera del externo y ocultar acciones locales → CLAUDE.md
- **FacturaIA** · `digest_mismatch` en webhook Retell → asumía bug del provider → instalar SDK oficial y usar `Retell.verify()` reveló bug propio en 30s → CLAUDE.md
- **Retell** · `recording_url` y `duration_ms` solo aparecen en `call_analyzed` post-call, no en tool call mid-call → capturar 1 payload real antes de codificar → CLAUDE.md
- **Subagentes** · agente seguridad reportó hallazgos de `facturaia/...` cuando debía auditar `~/agency-portal-fix` → pasar ruta absoluta + "investiga SOLO en esa ruta" en primera línea del prompt → CLAUDE.md
- 2026-05-16 · FacturaIA · refactor `$env.X` workflow n8n Receptor v2 → bug latente toolHttpRequest 1.1 (invocaciones secuenciales fallan "supplyData but no execute") → rollback al estado pre-refactor + threshold "n8n 2.21+ o migrar toolWorkflow" en hub. Endpoints internos creados (`/api/internal/whatsapp/*` + `/voice/*`) sobreviven para uso futuro. Ver [[Stack/n8n#Gotchas n8n LangChain 2.x mayo 2026]].
- 2026-05-16 · FacturaIA · Wasabi backup externo configurado via Dokploy nativo (S3 destination compartido por todos los Dokploys de AgentesIA, sin gestionar credentials manuales). Cierra TODO bloqueante "sync externo backups". Triple capa: local age-cifrado + Wasabi server-side AES-256 + Dokploy nativo.
- 2026-05-15 · FacturaIA · 404 inicial en `n8n.tufacturaia.com` → conflicto entre labels Traefik manuales del compose + auto-generados por Dokploy desde pestaña Domains. Fix: quitar labels manuales, dejar que Dokploy gestione el dominio desde su pestaña.
