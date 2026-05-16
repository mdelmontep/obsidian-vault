---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Kanban: **NOW** = en lo que estás esta sesión (máx 3). **NEXT** = próximas 2 semanas (máx 7). **LATER** = todo lo demás.

## NOW

- **FacturaIA — pestaña notificaciones por org** — siguiente paso natural. Inbox unificado: anomalías OCR + sugerencias IA + vencimientos + errores. Campana topbar + drawer feed. Base ya construida (`module_events`). ~1-2 días. Spec: `docs/MODULOS-PRODUCTO.md`
- **FacturaIA — smoke test post-deploy 2026-05-07** — pendiente: (1) anular factura emitida → ver abono ligado en banner rojo del modal + tab "Abonos" con count correcto; (2) crear presupuesto/proforma desde `/generar` (serie P/F + Ver PDF sin 404); (3) probar 3er botón "Emitir como pendiente" (Verifactu sí, email no, estado=`pendiente`); (4) dashboard KPIs no inflados con borradores; (5) menú 3 puntitos sin Editar/Eliminar en factura emitida, sin Anular en abono. Tests Vitest pendientes: proformas + abonos rectificativos
- **agency-portal PRs abiertos** — #54 quotes actions, #55 actor passthrough, #56 unificación facturas (hoy). Esperando review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` + populate

## NEXT (próximas 2 semanas)

- **FacturaIA — crear cron Dokploy `cashflow-alerts`** (`30 7 * * *`, curl con `$FACTURAIA_SERVICE_KEY`) tras deploy. Smoke test: ver `/admin/system/crons` con los 6 crons en verde a las 24h
- **FacturaIA — decidir VerifACTU worker en Dokploy** (hoy Disabled). Si va a quedar off, eliminar entrada. Si se activa, hacer Run Now y verificar facturas pendiente_envio → aceptada
- **FacturaIA — Stripe en activación de add-ons** — hoy CTA "+XX€/mes" redirige a `/settings?tab=plan` sin cobro real. Conectar checkout para que el toggle = compra. Conciliación 19€ y Anti-fraude 9€ ya seedeados
- **FacturaIA — Cobros backend** (módulo del recomendador IA) — recordatorios escalados configurables (3/10/25 días, tono, hora). 6 opciones config con badge Próximamente esperan
- **FacturaIA — decidir cliente live vs congelado** — hoy snapshot fiscal al crear factura (datos cliente embebidos). Si editas cliente, PDFs viejos conservan datos antiguos (legalmente correcto, confunde UX). Decisión producto: ¿añadir botón "Re-emitir con datos actuales" o dejar congelado siempre?
- **FacturaIA — manuales actualizar Bloque 1** — `manual-usuario.md` y `manual-admin.md` describen flujo viejo: 2 botones generar (no 3 con "Emitir como pendiente"), no mencionan anular ni tab Abonos ni los nuevos pills/badges
- **FacturaIA OTP — patch n8n delivery status** — generar key nueva en `n8n.tufacturaia.com/Settings/API` y ejecutar `python3 ops/n8n-patches/apply-delivery-status.py` (~5min)
- **FacturaIA OTP — quitar dominio viejo `facturaia.agentesia.world`** Dokploy Domains + DNS IONOS (causa confusión testing, mismo prod)
- **FacturaIA OTP — copiar `docs/legal/privacy-otp-update.md`** a política privacidad pública (RGPD art 13)
- **FacturaIA OTP — smoke tests restantes** — cambio teléfono re-auth, fallback forzado provider_degraded_until, banner grandfathering visual, superadmin impersonando bypass, lockout 15min
- **FacturaIA — Daily Briefing trigger → escribe `00-home/daily-briefing.md`** — comando `/daily` listo. Falta cron Dokploy o trigger automático
- **agency-portal #56 smoke test post-merge** — badge fiscal en row, redirect 301 `/agency/facturaia/*`, botones según estado/origen, modal motivo R1-R5 obligatorio, doble-click sin duplicar (Idempotency-Key)
- **FacturaIA #47 smoke test prod** — verificar entries en `audit_log` tras marcar cobrada / reenviar email / anular / DELETE vía API v1
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
- **FacturaIA cleanup mockup AgentesiaLab** — plan SQL elaborado, retomar cuando quieras. Org `ea201784-...`
- **Tecnocloud — WhatsApp en FacturaIA** — phone_number_id de Meta + webhook override
- **Simarro — IDs TODO en n8n** — TASK_TYPE_ID, RESPONSIBLE_USER_ID, SHEET_ID_LEADS_WEB, calendar de Ramón, Supabase pending
- **Simarro — oportunidad monitor inmuebles** (StateFox) — scraping Idealista/Fotocasa + alertas precio/m²/zona. Confirmar interés y presupuesto
- **Clínica Zen — configurar Retell en leads entrantes** — workflow `RN0wl8RaRmwLpnfQ`, verificar webhooks dominio CZ

## Bloqueos

_(ninguno activo)_

## Vistas por cliente

- [[facturaia]] · [[agentesia]] · [[simarro]] · [[clinica-zen]] · [[tecnocloud]]

## Completado reciente

Ver `00-home/archive-completed.md`
