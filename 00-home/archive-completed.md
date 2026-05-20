---
title: archivo de tareas completadas
date: 2026-04-26
tags: [home, archivo]
---

# Completado

- 2026-05-20 FacturaIA PR-A3 Copiloto v2 backend+UI desplegado — 4 tools (getKPIs, searchFacturas, getDeudaPorCliente, composeCobroMessage), runner dual-provider Anthropic/OpenAI tool-use, endpoints `/api/copiloto/message`+`/threads`, drawer v2 reemplaza ai-assistant v1, tool result cards. Multi-turno verde tras bugfix `380110c` (replay tool_calls+results emparejados). Commits `51e9979` → `380110c`. Bloqueado por quota OpenAI/Anthropic key (entry NEXT). Ver [[llm-tool-use-multi-turno-replay-tool-calls-y-results-emparejados]]
- 2026-05-19 FacturaIA PR #48 mergeado + mig 095 aplicada — toggle Verifactu unificado en columna `verifactu_activo`, guard rol (API route + trigger BD), trigger AFTER UPDATE en `audit_log` con IP/UA via `current_setting('request.headers')`. Auditado con 3 agentes paralelos (UI/UX + estructura + seguridad). Ver [[Stack/facturaia]] "Toggle Verifactu". Smoke pendiente en NEXT.
- 2026-05-18 FacturaIA cleanup AgentesiaLab — cuenta a 0 ejecutada (102 facturas `pendiente_envio` ninguna a AEAT → seguro borrar, + 23 ppttos + 31 clientes + 51 bandeja + 1 recordatorio, contadores series reseteados). En portal: 75 sombras `facturaia_documents` borradas + 3 entries stale en `api_idempotency`. Replicados desde portal: P2026-0001..0007 + A2026-0001 (Tecnocloud, particular sin NIF por decisión usuario). Ver [[Stack/facturaia]] "Reset cuenta a 0".
- 2026-05-18 FacturaIA portal apuntaba al dominio antiguo caído — `FACTURAIA_API_URL` cambiado de `facturaia.agentesia.world` (404) a `app.tufacturaia.com`. La "migración" fue solo cambio de dominio (misma BD Supabase `lahqlyaxvobqjgdiftag`, misma API key). Cliente HTTP del portal llevaba semanas fallando silenciosamente. Ver [[dominio-renombrado-no-es-migracion-verificar-mismo-backend]].
- 2026-05-10 → 2026-05-18 FacturaIA pestaña notificaciones por org — inbox unificado completo. Commits: `becb81e` feat inicial campana topbar + drawer + tabla `notifications`, `91280a1` `notify_upsert` atómico ON CONFLICT + triggers auto-resolución (factura cobrada cierra vencida), `7763283` fix crash Realtime channel reuse en StrictMode, `f86016b` + `2708f12` polish drawer compacto coloreado por categoría + stale-while-revalidate, `ad5d8a4` fix `unread-count` snooze + cleanup, `056ff94` (2026-05-18) a11y — focus trap Tab/Shift+Tab + `aria-controls` bell + `aria-labelledby` h2 + live region `role=status` para Realtime. Tabla `notifications` separada de `module_events` con `dedupe_key` UNIQUE. RLS + withApiAuth + effectiveOrgId verificado por 4 agentes audit (cero vulns multi-tenant). 7 kinds NON_SILENCEABLE_KINDS hardcoded + prefijo `cron_failed_*`. Bell badge `severity IN ('warning','critical')` con bumpSeverityOnRepeat. Docs: manual-admin §22 completo, gotchas.md §Frontend (radiogroup pattern + drawer modal a11y obligatorio). NO confundir con módulo OCR/cobros — esta es la **bandeja in-app** que ve el cliente.
- 2026-05-18 agency-portal PR #67 mergeado — tool calling con `tool_choice` forzado para extracción onboarding LLM (gpt-4o-2024-11-20 + Structured Outputs strict). Elimina silent fail `extracted_fields:[]` que tenía progreso UI siempre en 0%. Ver [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding]]
- 2026-05-18 agency-portal PR #66 mergeado — helper `nullishOptional` para webhooks n8n + meta-test anti-regresión. Cierra incident 95% tráfico onboarding fallaba con 400 tras PR #65. Ver [[zod-optional-rechaza-null-en-webhooks-n8n]]
- 2026-05-17 agency-portal — TTL Redis `aia_ob:{phone}` subido 24h → 30d en workflow `AIA Onboarding — Research y arranque` (tirita hasta fix estructural pendiente en NEXT)
- 2026-05-13 agency-portal PRs #54/#55/#56 mergeados (quotes actions, actor passthrough, unificación facturas)
- 2026-05-10 ⭐ FacturaIA módulo Voz F1+F2 + admin completo — 17 commits sobre `main` (`88626e0` → `4e98d76`): endpoints `/api/voice/find-presupuesto` + `convert-presupuesto` + `/api/internal/{voice-system-prompt,voice-chat-bindings}` + `/api/modules/generador_voz/{prompt,history,restore,preview,playground}` + `/admin/voice` (tabla overrides). 6 migraciones (053-058 voice_invocations/idempotency/chat_bindings/prompt_versions/grants+purge/pg_cron). Sistema híbrido del prompt (12 variables tipadas + modo Avanzado). Workflow `zYcHHa8jWXB6dY5i` patcheado vía API (consultar_presupuestos toolCode + branch convertir_presupuesto post-confirmación). 5 hardenings detectados E2E (PGRST203 RPC overload, feature_gate, iva_pct min/max, invalid_json, ocr-audit FK). Primera prueba real con WhatsApp reveló 2 bugs UX: resumen 0€ y matching estricto con typos Whisper — fixeados con lookup HTTP en `Parsear y Calcular Totales` y system prompt mejorado (matching permisivo + lista candidatos numerados + fallback últimos abiertos + memoria conversacional). Manuales actualizados (usuario sección "Convertir presupuesto" + admin sección 23.11/23.12). 101 tests E2E reales contra Supabase prod, 60/60 unit, lint/typecheck/build OK
- 2026-05-08 FacturaIA PR #47 mergeado — audit log en marcar-cobrada/reenviar-email/anular/DELETE + idempotency en DELETE (`logAgentAction` con actor=agent:api)
- 2026-05-08 agency-portal PR #56 abierto — unificar Facturas + Facturas fiscales: sidebar -1 entrada, detalle único con fallback portal→sombra, modal motivo R1-R5 obligatorio en anular (era R5 hardcoded), redirect 301, FacturaiaActions reemplaza acciones locales cuando hay shadow
- 2026-05-07 FacturaIA sesión grande — 31 commits a main: tests prioritarios HMAC + cursor + idempotency + SERIE_BY_TIPO + IVA + rate-limit (175 tests); withApiAuth wrapper aplicado a 19 endpoints session + rate limit auto en 26 admin via requireAdmin; UI primitives Button/Card/Input/Modal; 14 modales con role=dialog + Pressable helper; FacturaMeta badges (✉/AEAT/abono) con Icon SVG (no emojis); tabs Facturas/Abonos en /emitidas; fix bug fiscal informes IVA + dashboard excluyen borradores/anuladas; fix EstadoPill MAP (anulada faltaba mostraba "Pendiente" en azul); 3er botón "Emitir como pendiente" en /generar; menú 3 puntitos condicional por estado; CI integration job con Supabase local funcional; RLS en migration_037; .env.example expandido (28 vars); migrations 047/048/049 desbloqueando supabase CLI; deploy verde + Supabase migration 046 RLS aplicada en prod; 5 learnings nuevos al vault, 5 reglas nuevas a CLAUDE.md proyecto
- 2026-05-06 FacturaIA: sistema módulos premium completo (catálogo + plan/add-on + recomendador IA con 2 evaluators reales + activity feed + métricas conectadas + validación rangos + control admin total + 137 tests Vitest, 6 opciones config cableadas y verificadas; CLAUDE.md global con 5 reglas nuevas + 1 al proyecto)
- 2026-05-06 FacturaIA: cron Dokploy del recomendador IA configurado y validado (1 sugerencia generada para AgentesiaLab: antifraud, ratio max/min 151x)
- 2026-05-07 Simarro BLOQUEANTES — re-auth GCal Ramón, SMTP cred, N8N_WEBHOOK_TOKEN Vercel + PR #1, smoke E2E chatbot WhatsApp y voz Retell
- 2026-05-07 Clínica Zen — hero_overlay.jpg subida a `email-assets/clinica-zen/` y emails actualizados
- 2026-05-07 FacturaIA smoke tests deploy 2026-05-02 — webhook delete híbrido, edit URL, GET clientes con paginación cursor + sanitización, GET clientes/[id] con UUID, webhook E2E delivered + sombra portal, cron dispatcher Dokploy
- 2026-05-07 FacturaIA smoke tests audit creación deploy 2026-05-05 — factura dashboard, presupuesto WhatsApp, factura/presupuesto portal con actor, conversión presupuesto→factura
- 2026-05-07 FacturaIA secrets rotados — `fia_live_ZyuhX…` API key + `whsec_fia_q2x…` webhook secret reemplazados (nuevos en paralelo, portal actualiza Dokploy, viejos eliminados)
- 2026-05-07 agency-portal PR #50 mergeado — fix detalle standalone para sombras `facturaia_direct`
- 2026-05-07 agency-portal main local — 4 commits sin pushear resueltos con Borja
- 2026-05-07 FacturaIA Presupuestos/Proformas/Abonos completos — emisión funcional desde form manual + voz (Bloques 1, 2 y abonos en emitidas con estado pagada). Pendiente solo: tests proformas + rectificativas
- 2026-05-07 FacturaIA Voz WhatsApp en producción — 10 puntos verificados (e2e orgs, OCR receptor v2, presupuestos, textos WA, 403 toggles, invitación novia, modal series, duplicados BD, response limpio, sub-workflows archivados)
- 2026-05-07 Notificaciones tickets dashboard → Slack `#01-tickets-soporte`
- 2026-05-07 Repo privado skill chatbot-chatwoot-replicator
- 2026-05-07 Tests FacturaIA `orgHasFeature` + `getOrgBilling` + `isSuperadmin` (incluidos en los 137 tests Vitest)
- 2026-05-07 Deploy prod FacturaIA — push + Dokploy + test e2e OCR
- Simarro — chatbot WhatsApp respuesta lenta arreglada (2026-05-04): Wait node debounce con `parameters:{}` era webhook-type → stuck. Fix: PUT REST API + Redis restaurado en compose. Chatbot vuelve a ~2s por mensaje

- Integración FacturaIA ↔ agency-portal viva en prod — PRs A1-A3 mergeados, smoke test E2E OK, webhook con cliente_nombre poblado tras fix `cliente:clientes(...)` embed en GET singular. Cron Dokploy cada 1min. Pendiente: rotar secrets que circularon en chat (2026-05-02)
- FacturaIA ↔ agency-portal: integración completa — 7 PRs apilados (P1-P7) en portal + auditoría con 7 fixes commiteados (transient HMAC, UPSERT remote_id, path traversal, schema cache, signed URL proxy, PostgREST .or() injection, TS narrowing). Stripe-style sync (webhook + cron + backfill). PR-A3 facturaia #32 pendiente cerrar (2026-05-01)
- FacturaIA: modal series con builder arrastrable y picker inline (impeccable+polish+audit+critique+guidelines+baseline+typeset) (2026-04-28)
- FacturaIA: validación formato series — mig 021 CHECK `is_valid_series_format` + API + UI con feedback (2026-04-28)
- FacturaIA: invitaciones equipo — `org_member` directo tras inviteUserByEmail + promover invitado→activo en primer login (2026-04-28)
- FacturaIA: fix workflow voz abono — tool `consultar_facturas` + prompt obliga validar factura origen + endpoint rechaza abono sin `factura_origen_id` (2026-04-28)
- FacturaIA: limpieza BD mockup org de testing + serie A restaurada (2026-04-28)
- FacturaIA: Sprint #6/#7 — proforma/abono BD+voz+toggles UI WhatsApp deployados (2026-04-28)
- Clínica Zen: cancelar cita Retell — fix `$if(isExecuted)` en `Update leads1` + error handler con `JSON.stringify` y campos extra (description/http_code/details). Workflow `DkueIeGFWLKh8nTj` (2026-04-29)
- FacturaIA: billing banner + feature-locked rediseñados (2026-04-26)
- FacturaIA: datos fiscales completos clientes/proveedores (2026-04-26)
- FacturaIA: simplificación workflow voz WhatsApp (2026-04-26)
- FacturaIA: rediseño formulario nueva factura + envío email (2026-04-25)
- FacturaIA: generador facturas por voz — n8n workflows desplegados (2026-04-25)
- FacturaIA: system_config + admin config page (2026-04-25)
- FacturaIA: security hardening (2026-04-25)
- FacturaIA: plantillas de factura con PDF pixel-perfect (2026-04-25)
- FacturaIA: admin limits/storage fix (2026-04-25)
- FacturaIA: UI improvements + filtros + mobile responsive (2026-04-25)
- FacturaIA: vitest 22 tests billing/features/admin (2026-04-25)
- FacturaIA: complimentary orgs MRR (2026-04-25)
- FacturaIA: KPI cards clickables admin (2026-04-25)
- FacturaIA: Email Ingesta OAuth Gmail (2026-04-24)
- FacturaIA: WhatsApp multi-tenant matching (2026-04-24)
- FacturaIA: Canales Ingesta + Plan/Facturación spec aprobada (2026-04-24)
- n8n.agentesia.world: compose healthcheck + pruning + memory limit (2026-04-22)
- FacturaIA: Full impersonation proxy client (2026-04-22)
- FacturaIA: WhatsApp ingesta + Canales de Ingesta UI (2026-04-21)
- FacturaIA: Admin Panel + Feature Flags 24 tareas (2026-04-21)
- FacturaIA: Conciliación bancaria spec (2026-04-21)
- Clinica Zen: chatbot + voz completado (2026-04-23)
- Obsidian inbox procesado 25→1 (2026-04-25)
- FacturaIA: Fases 1-5 completadas
- FacturaIA: rediseño visual completo
- CLAUDE.md global optimizado

## 2026-05-18

- FacturaIA — smoke test post-deploy 2026-05-07 (5 puntos auditados OK + fix borrador anular + 7 E2E tests). Cubierto por sesión cumplimiento fiscal full.
