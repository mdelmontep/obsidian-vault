---
title: archivo de tareas completadas
date: 2026-04-26
tags: [home, archivo]
---

# Completado

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
