---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Kanban: **NOW** = en lo que estás esta sesión (máx 3). **NEXT** = próximas 2 semanas (máx 7). **LATER** = todo lo demás.

## NOW

- **Centro Elphis — nuevo cliente Agentesia (voz + chat + CRM + agenda)** — diseño cerrado en `/Users/manueldelmonte/elphis/CLAUDE.md`. Stack: Retell + ElevenLabs ES + Twilio · Chatwoot + 360dialog · Clientify único CRM · Google Calendar como agenda-service (Doctoralia sin API, ver [[ADR-001-doctoralia-google-calendar]]) · n8n + Postgres dedicados en Dokploy. Pendiente: confirmar 8 bloqueantes con Elphis ([[bloqueantes-elphis]]) + arrancar Fase 0 Dokploy. HUB: [[clientes/centro-elphis/index|Centro Elphis HUB]]
- **agency-portal — verificar extracción onboarding en prod tras PR #67** — REO RAFTING en curso. Confirmar que "Progreso por sección" y "Respuestas extraídas" se rellenan tras cada turno con dato extraíble. Si aparece `activity_event.action='onboarding.extraction_failed'`, abrir issue
- **agency-portal — smoke PR #72 onboarding sync+md+web** — tras merge: nuevo onboarding real (o el siguiente cliente) y verificar (a) botón Sincronizar puebla `clients.description`/`primary_contact_phone`/`website`/`assistant_name`/etc, (b) `.md` final incluye sección "Transcripción completa de WhatsApp", (c) si la nota del operador menciona web → bot pregunta dominio/colores/referencias/CTA antes de cerrar, (d) bot hace repaso `[N]` agrupado antes de `is_complete=true`. Ver [[Stack/onboarding-whatsapp]]

## NEXT (próximas 2 semanas)

- **FacturaIA — test e2e middleware/proxy activo** (~1-2h) — disparado por incidente 2026-05-20 donde se creyó (erróneamente) que `proxy.ts` no se ejecutaba durante 3 semanas. Smoke test que verifica que `impersonate_org` cookie behavior end-to-end. Detalle en hub Ideas crudas
- **agency-portal — extraer `extractError` a helper compartido** (~1h) — hoy lo arreglé en 3 sitios con copy-paste (auto-emit, pdf/[shadowId], handler manual fetch). Extraer a `lib/facturaia/extract-error.ts` + tests + reemplazar las 3 copias
- **FacturaIA — rotar OpenAI key (higiene, expuesta en transcript 2026-05-21) + fix typo `ssk-ant-` → `sk-ant-` en env Anthropic Dokploy** (~5min, P2) — no bloquea nada hoy (OpenAI funciona, Anthropic no se usa); higiene + tener fallback
- **FacturaIA Copiloto — PR-A3.1 (3 tools movimientos)** — `suggest_note`, `explain_movimiento`, `analyze_movimiento` para contexto conciliación
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
