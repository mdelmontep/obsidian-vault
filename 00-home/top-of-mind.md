---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

- **Simarro — continuar 2026-05-02 paso a paso con tests e2e** — verificar IDs TODO (task_type, responsible_user, sheet_id, calendar Ramón, salesbots, Supabase). Tests por flujo: Retell reservar/cancelar, WhatsApp bot reservar/cancelar/derivar, Formulario web, Recordatorios. Publicar agente Retell solo cuando todo pase. Ver `simarro/CLAUDE.md` sección "Próxima sesión"
- **Simarro 2026-05-03 BLOQUEANTES (en orden)**:
  1. Pedir a Ramón que **re-autorice cred Google Calendar** en n8n (`d3uDK7X9ZflAoumq` da `Forbidden`). Sin esto, agente WhatsApp/voz no consulta calendario y agente asignado no crea evento
  2. **Crear cred SMTP Gmail** en n8n con App Password de `simarroproperties@gmail.com`. Sin esto, ningún email sale (cred fantasma `oKRmYFhljczyvzV8`). Pasarme el ID y reasigno los 5 nodos
  3. **Confirmar que Borja metió `N8N_WEBHOOK_TOKEN`** en Vercel + mergeó PR #1 de simarro_web. Token: `simarro_Z2O40vQbqve2YZ3Ksn2JsEQCcJqAh6L8BO8mxvbqwTE`
  4. **Test E2E chatbot WhatsApp** escribiendo a `+34 919 93 28 52` — verificar respuesta + Kommo + lógica fin-de-semana → Derivar_agente
  5. **Test E2E voz Retell** llamando a `+34 919 93 28 52` (mismo número WhatsApp+voz). Antes publicar agente Retell (`is_published: true`)
- **Clinica Zen — Corregir email confirmación (2026-04-25)** — imágenes base64, verificar en Gmail/Apple Mail. Workflow `13Roz21TOBwy8gp8` nodo `Send Confirmation Email`
- **FacturaIA — smoke tests pendientes tras deploy 2026-05-02** — ejecutar y verificar manualmente: (1) Webhook delete híbrido: crear webhook prueba → eliminar sin entregas (debe desaparecer), crear otro → emitir factura → eliminar (debe quedar revocado, oculto por defecto, visible con toggle). (2) Editar URL webhook desde UI con icono lápiz, secret se conserva. (3) `GET /v1/clientes?q=...&limit=10` con Bearer real, verificar paginación cursor + sanitización `q` con caracteres `,()`. (4) `GET /v1/clientes/{id}` con UUID válido (200) e inválido (422) y de otra org (404). (5) Webhook E2E: emitir factura, esperar ≤1min, verificar `webhook_deliveries.status='delivered'` + sombra en portal. (6) Cron dispatcher Dokploy logs cada minuto exit 0. Bloquea cierre de la integración como "estable"

## Prioridades esta semana

- **FacturaIA — Presupuestos/Proformas/Abonos** — ~~backend voz proforma/abono~~ HECHO. Pendiente Bloque 1 form manual `generar-view.tsx`: SERIE_POR_TIPO mal (proforma=T, abono=A → debe ser F y B), no setea `tipo_documento` ni `factura_origen_id`, falta selector factura origen abono manual, GET `/api/render-pdf?tipo=&id=`, rama `presupuesto_id` en `/api/email/send`. Bloque 2 vistas separadas presupuesto/proforma + abonos en emitidas + estado `pagada`. Bloque 4 `/api/agent/query/*` queries naturales. Bloque 5 métricas tiempo medio + manuales con proforma/abono/modal series visibles
- **FacturaIA — rotar secrets que circularon en chat (2026-05-02)** — `fia_live_ZyuhX…` (API key) y `whsec_fia_q2x…` (webhook secret). Camino simple: crear nuevos en paralelo, sesión portal actualiza Dokploy, eliminar viejos. Ver [[webhook-delete-hibrido-hard-si-no-disparo-soft-si-tiene-historial]]
- **agency-portal PR #50 esperando review Borja** — fix detalle standalone para sombras `facturaia_direct` (`/agency/facturaia/[id]` Server Component + cliente lectura). En main todavía clickear factura fiscal lleva al listado, no al detalle individual. Cuando merge: redeploy portal, queda bug-free. https://github.com/AgentesIA-MAdrid/agency-portal/pull/50
- **FacturaIA — Voz WhatsApp pendientes** — Test 6 mensajes específicos en 403 toggles ("admin desactivó este canal", no error genérico). Probar invitación con novia tras deploy `98250b9`. Probar modal series tras deploy
- **FacturaIA — Asistente IA multi-canal** — conectar AI assistant al canal WhatsApp para consultas (vencidas, resúmenes, pendientes). Extensiones: cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API. Token storage per org, template editor con variables
- **FacturaIA — Canales Ingesta + Plan/Facturación (spec 2026-04-24)** — canales rediseño sin toggles, config expandible. Plan: página con planes reales, método pago, historial
- **FacturaIA — Conciliación bancaria IA (spec 2026-04-21)** — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes. Pendiente: plan de implementación
- **Tecnocloud — WhatsApp en FacturaIA** — obtener phone_number_id de Meta, guardar en org, webhook override
- **Simarro — preguntar a Ramón (pendiente)** — (1) ¿Cómo funcionan las citas? ¿Bot reserva directo o primero fecha provisional? (2) ¿Pipeline Kommo actual vale o ajustes? (alquiler ya descartado, bot/voz limpios)
- **Simarro — verificar salesbot 88183** — comprobar que tiene acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo
- **Simarro — IDs TODO en n8n** — `TASK_TYPE_ID_TODO`, `RESPONSIBLE_USER_ID_TODO`, `SHEET_ID_LEADS_WEB_TODO`, salesbots Recordatorios (87861/87863/87865/87871), calendar de Ramón (ahora `primary`), Supabase pending
- **Simarro — oportunidad monitor inmuebles** — sistema tipo StateFox: scraping Idealista/Fotocasa + alertas filtradas a clientes (precio/m²/zona). Apify igolaizola actors + n8n + Kommo. Pendiente: confirmar interés y presupuesto
- **Clínica Zen — status_id Kommo 'Cita cancelada'** — workflow `DkueIeGFWLKh8nTj` `Update leads1` → 400 `NotSupportedChoice` (104115987 heredado de Gonzalo). Pedir ID correcto en pipeline 13495347
- **Clínica Zen — configurar Retell en leads entrantes** — workflow `RN0wl8RaRmwLpnfQ`, verificar webhooks dominio CZ
- Notificaciones tickets dashboard → Slack `#01-tickets-soporte`
- Repo privado skill chatbot-chatwoot-replicator
- Tests FacturaIA: `orgHasFeature`, `getOrgBilling`, `isSuperadmin`
- Deploy prod FacturaIA: push + Dokploy + Traefik reload + test e2e OCR

## Bloqueos

_(ninguno activo)_

## Completado reciente

Ver `00-home/archive-completed.md`

- VeriFACTU integración completa (QR en PDFs todas las plantillas, toggle sincroniza BD, cron cada hora, migración aplicada, deploy prod) — 2026-04-27
- FacturaIA Sprint #6/#7 + workflow voz abono + invitaciones equipo + validación formato series + modal series con builder arrastrable — 2026-04-28
