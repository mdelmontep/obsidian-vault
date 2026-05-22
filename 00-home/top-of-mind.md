---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Kanban: **NOW** = en lo que estás esta sesión (máx 3). **NEXT** = próximas 2 semanas (máx 7). **LATER** = todo lo demás.

## NOW

- **Centro Elphis — esperando datos cliente para activar prod** — Fases 0-4 cerradas (n8n + Chatwoot + Clientify + GCal + agente voz Retell `agent_543dcfc82ed751c131bf720075` + puentes Meta WA). Pendiente solo: (1) Dokploy env vars `META_PHONE_NUMBER_ID` + `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`; (2) token Meta real en cred n8n `meta-wa-elphis`; (3) webhook Meta Business Manager; (4) SIP trunk Twilio → Retell; (5) DPAs Enrique. HUB: `/Users/manueldelmonte/elphis/CLAUDE.md`
- **agency-portal — verificar extracción onboarding en prod tras PR #67** — REO RAFTING en curso. Confirmar que "Progreso por sección" y "Respuestas extraídas" se rellenan tras cada turno con dato extraíble. Si aparece `activity_event.action='onboarding.extraction_failed'`, abrir issue
- **agency-portal — smoke PR #72 onboarding sync+md+web** — tras merge: nuevo onboarding real (o el siguiente cliente) y verificar (a) botón Sincronizar puebla `clients.description`/`primary_contact_phone`/`website`/`assistant_name`/etc, (b) `.md` final incluye sección "Transcripción completa de WhatsApp", (c) si la nota del operador menciona web → bot pregunta dominio/colores/referencias/CTA antes de cerrar, (d) bot hace repaso `[N]` agrupado antes de `is_complete=true`. Ver [[Stack/onboarding-whatsapp]]

## NEXT (próximas 2 semanas)

- **EcoBox — nuevo cliente AgentesIA (taller chapa+pintura Las Rozas)** — voz Retell + chat Chatwoot compartido + emails confirmación+alert. Todo desplegado y enchufado en `n8necobox.agentesialabs.com`. Pendiente Cristian: número provider, WABA en portfolio `1011127821491282`, plantilla HSM `confirmacion_cita` Utility, GCal compartido, app-password SMTP, logo+color. Pendiente Manu: OAuth Google en n8n UI. HUB: [[clientes/ecobox/index|EcoBox HUB]] · [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo]] · [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode]]
- **FacturaIA Copiloto — PR-A3.1 smoke E2E prod** — desplegado 2026-05-21. Script smoke listo en `tests/smoke/copiloto-a3-1.mjs` (encadena `searchMovimientos` → `explainMovimiento` → `analyzeMovimientoPattern`). Bloqueado por storageState/OTP headless; backend + vitest 10/10 verificados 2026-05-22. Commits 5d10cdf + 26a0f2a
- **FacturaIA — smoke UI PR #65 conciliación vinculación visible** — spec listo en `tests/e2e/smoke/conciliacion-vinculacion.spec.ts` (5 tests). Mig 131 verificada en prod 2026-05-22 (PostgREST hint signature 3-args). Falta solo ejecución headless. Test 5 destructivo (consume 1 asignación)
- **FacturaIA — exportar storageState Chrome para desbloquear smokes E2E headless** (~5min) — sin esto Copiloto PR-A3.1 + PR #65 conciliación + Multi-org Equipo + Anular ⋯ /emitidas + /sin-acceso quedan bloqueados por el mismo gate OTP no automatizable. Guardar en `~/Downloads/facturaia-state.json`, 5 smokes E2E corren autónomos
- **FacturaIA — UI fiscal-panel mostrar aeat_health derivado** (~30 líneas) — endpoint `/api/admin/config/fiscal` ahora devuelve health derivado (verde/ámbar/rojo/gris) + last_10 pero panel sigue mostrando solo HealthRow certs. Añadir segundo HealthRow + lista compacta. Commit b6014de
- **FacturaIA — Email_log Fase B** — webhook Resend (delivered/bounced/complained/opened) + UI panel listado + reenvío 1-click + cablear OTP/team_invite/team_added/team_removed/team_role_changed (kinds ya en CHECK constraint mig 143). Fase A en prod commit 7861b0d
- **FacturaIA — 3 envs `.env.test` para activar casos A/B del smoke middleware** (~5min) — `E2E_SUPERADMIN_TEST_ORG_ID`, `E2E_UNVERIFIED_EMAIL`, `E2E_UNVERIFIED_PASSWORD`. Sin ellos solo corre caso C (sanity). Commit cafc8dc
- **FacturaIA — coherencia `manual-usuario.md` vs `manual-admin.md` §31 Equipo** — 3 puntos: etiqueta "Inactivo" (usuario L536) vs estados internos `revocado/expirado`; acción "revocar invitación" del menú ⋯ (L551) no en admin; "transferencia de propiedad" (L558) no documentada en admin. Decidir si UI existe y unificar
- **GitHub Actions billing — decidir** — 3 opciones: (a) esperar reset día 1 mes siguiente; (b) repo público (ilimitado pero expone); (c) tarjeta + spending limit 10$/mes. Mientras: trabajar local, push solo cuando despliegue necesario. Ver [[github-actions-org-private-free-tier-2000-min]]
- **FacturaIA — smokes E2E post-PR Conciliación #73/#74** — filtros chip URL `?filter=`, bulk-confirm toast undo (8s), drawer confirm dialog del sistema, iOS no-zoom inputs drawer, primer cron `anomaly-batch` automático verde 2026-05-21 18:00. Pendiente validar en `app.tufacturaia.com` con cuenta real (multi-org)
- **FacturaIA — crear cron Dokploy `cashflow-alerts`** (`30 7 * * *`, curl con `$FACTURAIA_SERVICE_KEY`) tras deploy. Smoke test: ver `/admin/system/crons` con los 6 crons en verde a las 24h
- **FacturaIA — decidir VerifACTU worker en Dokploy** (hoy Disabled). Si va a quedar off, eliminar entrada. Si se activa, hacer Run Now y verificar facturas pendiente_envio → aceptada
- **FacturaIA — Stripe en activación de add-ons** — hoy CTA "+XX€/mes" redirige a `/settings?tab=plan` sin cobro real. Conectar checkout para que el toggle = compra. Conciliación 19€ y Anti-fraude 9€ ya seedeados
- **FacturaIA — Cobros backend** (módulo del recomendador IA) — recordatorios escalados configurables (3/10/25 días, tono, hora). 6 opciones config con badge Próximamente esperan
- **FacturaIA — decidir cliente live vs congelado** — hoy snapshot fiscal al crear factura (datos cliente embebidos). Si editas cliente, PDFs viejos conservan datos antiguos (legalmente correcto, confunde UX). Decisión producto: ¿añadir botón "Re-emitir con datos actuales" o dejar congelado siempre?
- **FacturaIA OTP — patch n8n delivery status** — generar key nueva en `n8n.tufacturaia.com/Settings/API` y ejecutar `python3 ops/n8n-patches/apply-delivery-status.py` (~5min)
- **FacturaIA — quitar dominio viejo `facturaia.agentesia.world` de IONOS + Dokploy** — repo y `.env.local` ya limpios (2026-05-20). Queda solo infra externa: DNS IONOS + entrada stack Dokploy. Limpiar para evitar confusión futura
- **FacturaIA OTP — copiar `docs/legal/privacy-otp-update.md`** a política privacidad pública (RGPD art 13)
- **FacturaIA OTP — smoke tests restantes** — cambio teléfono re-auth, fallback forzado provider_degraded_until, banner grandfathering visual, superadmin impersonando bypass, lockout 15min
- **FacturaIA — Daily Briefing trigger → escribe `00-home/daily-briefing.md`** — comando `/daily` listo. Falta cron Dokploy o trigger automático
- **agency-portal — fix estructural n8n router consulta Supabase como source of truth** — TTL 30d en `aia_ob:{phone}` es tirita. Endpoint nuevo `/api/onboarding/is-active-by-phone` + nodo HTTP en router del workflow `ChatBOT mejorado` antes del IF de Activo + Redis pasa a caché con re-seed si portal dice activa. Ver [[Stack/n8n]] + [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding]]
- **FacturaIA #47 smoke test prod** — verificar entries en `audit_log` tras marcar cobrada / reenviar email / anular / DELETE vía API v1
- **FacturaIA #48 smoke test prod** (mergeado 2026-05-19, mig 095 aplicada) — (1) Settings → Fiscal → toggle Verifactu off → confirm dialog → Guardar → recargar → persiste. (2) Con usuario rol `solo_lectura`/`comercial`: PUT `/api/settings/verifactu` → 403. (3) Cambio deja fila en `audit_log` con `accion='verifactu_settings_changed'`, `user_id`, `ip`, `user_agent`, `detalles.{verifactu_activo,entorno_verifactu}.{old,new}`
- **FacturaIA — auditar otras columnas regulatorias con misma vulnerabilidad que Verifactu tenía** — `org_member_update` policy permite UPDATE a cualquier miembro. Candidatos a proteger con trigger guard de rol + auditoría: `regimen_iva`, `nif`, `iae`, `verifactu_num_instalacion`, `entorno_verifactu`. Ver [[Stack/facturaia]] "Vulnerabilidad latente"
- **Agentesia chatbot ticketing — test cliente real** — pedir teléfono al cliente "Soporte técnico" + verificar respuestas AI a TICKET_CREATED/APPENDED/ERROR_NO_CLIENTE. Limpiar workflow temporal `a96XVFKX4WujMCKW`
- **Simarro — preguntar a Ramón** — (1) ¿Citas: bot reserva directo o fecha provisional? (2) ¿Pipeline Kommo actual vale o ajustes?
- **Simarro — verificar salesbot 88183** — comprobar acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo
- **Clínica Zen — status_id Kommo 'Cita cancelada'** — workflow `DkueIeGFWLKh8nTj` da 400 NotSupportedChoice. Pedir ID correcto pipeline 13495347
- **Tecnocloud — PR #3 voice-webhook-tickets** pendiente review Dani — buildSubject 14 palabras + skip self-emails gmail-poll + audio Retell en UI ticket. Tras merge → smoke test E2E con llamada real

## LATER

- **FacturaIA — backends módulos pendientes** — Fiscal (modelos AEAT 303/111/115/347), Firma eIDAS, Cashflow IA forecast. ~21 opciones config con badge Próximamente
- **FacturaIA — conexión bancaria automática** (Plaid/GoCardless/BBVA Open Banking) — desbloquea Conciliación al 100%
- **FacturaIA — Asistente IA multi-canal** — copiloto WhatsApp para consultas (vencidas, resúmenes, cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal). Spec `[[facturaia-bloque-4-agent-query-spec]]`
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API
- **FacturaIA — Canales Ingesta + Plan/Facturación** (spec 2026-04-24) — rediseño canales sin toggles, página planes reales con método pago e historial
- **FacturaIA — Conciliación bancaria IA** (spec 2026-04-21) — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes
- **Tecnocloud — WhatsApp en FacturaIA** — phone_number_id de Meta + webhook override
- **Simarro — IDs TODO en n8n** — TASK_TYPE_ID, RESPONSIBLE_USER_ID, SHEET_ID_LEADS_WEB, calendar de Ramón, Supabase pending
- **Simarro — oportunidad monitor inmuebles** (StateFox) — scraping Idealista/Fotocasa + alertas precio/m²/zona. Confirmar interés y presupuesto
- **Clínica Zen — configurar Retell en leads entrantes** — workflow `RN0wl8RaRmwLpnfQ`, verificar webhooks dominio CZ

## Bloqueos

_(ninguno activo)_

## Vistas por cliente

- [[facturaia]] · [[agentesia]] · [[simarro]] · [[clinica-zen]] · [[tecnocloud]] · [[clientes/centro-elphis/index|centro-elphis]]

## Completado reciente

Ver `00-home/archive-completed.md`
