---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

- **Simarro 2026-05-04 BLOQUEANTES (en orden)**:
  1. Pedir a Ramón que **re-autorice cred Google Calendar** en n8n (`d3uDK7X9ZflAoumq` da `Forbidden`). Sin esto, agente WhatsApp/voz no consulta calendario y agente asignado no crea evento
  2. **Crear cred SMTP Gmail** en n8n con App Password de `simarroproperties@gmail.com`. Sin esto, ningún email sale (cred fantasma `oKRmYFhljczyvzV8`). Pasarme el ID y reasigno los 5 nodos
  3. **Confirmar que Borja metió `N8N_WEBHOOK_TOKEN`** en Vercel + mergeó PR #1 de simarro_web
  4. **Test E2E chatbot WhatsApp** escribiendo a `+34 919 93 28 52` — chatbot YA responde en ~2s (arreglado 2026-05-04)
  5. **Test E2E voz Retell** llamando a `+34 919 93 28 52`. Antes publicar agente Retell (`is_published: true`). Smoke test específico: pedir "*busco un piso en Las Rozas de 3 habitaciones por 600 mil*" → verificar que Ana ejecuta `Buscar_viviendas`, lee 1-2 opciones breves (zona + precio), y si pides detalles los saca sin re-llamar la tool. También verificar caso 0 resultados ("*busco un castillo en Marte*") → fallback hablable
- **Clínica Zen — hero_overlay.jpg pendiente** — imagen con overlay 45% bakeado lista en `/tmp/hero_overlay.jpg`. Falta subir a `AgentesIAMadrid/email-assets/clinica-zen/` (PAT actual sin `Contents:write`). Cuando esté: `python3 /tmp/update_emails_v2.py`
- **FacturaIA — smoke tests pendientes tras deploy 2026-05-02** — ejecutar y verificar manualmente: (1) Webhook delete híbrido: crear webhook prueba → eliminar sin entregas (debe desaparecer), crear otro → emitir factura → eliminar (debe quedar revocado, oculto por defecto, visible con toggle). (2) Editar URL webhook desde UI con icono lápiz, secret se conserva. (3) `GET /v1/clientes?q=...&limit=10` con Bearer real, verificar paginación cursor + sanitización `q` con caracteres `,()`. (4) `GET /v1/clientes/{id}` con UUID válido (200) e inválido (422) y de otra org (404). (5) Webhook E2E: emitir factura, esperar ≤1min, verificar `webhook_deliveries.status='delivered'` + sombra en portal. (6) Cron dispatcher Dokploy logs cada minuto exit 0. Bloquea cierre de la integración como "estable"

## Prioridades esta semana

- **FacturaIA — Presupuestos/Proformas/Abonos** — ~~backend voz proforma/abono~~ HECHO. Pendiente Bloque 1 form manual `generar-view.tsx`: SERIE_POR_TIPO mal (proforma=T, abono=A → debe ser F y B), no setea `tipo_documento` ni `factura_origen_id`, falta selector factura origen abono manual, GET `/api/render-pdf?tipo=&id=`, rama `presupuesto_id` en `/api/email/send`. Bloque 2 vistas separadas presupuesto/proforma + abonos en emitidas + estado `pagada`. Bloque 4 `/api/agent/query/*` queries naturales — ver spec `[[facturaia-bloque-4-agent-query-spec]]`. Bloque 5 métricas tiempo medio + manuales con: (a) proforma como entidad (serie F, conversión a factura, "pagada" intermedia), (b) abono fiscal (serie B, total negativo, `factura_origen_id`, fundamento rectificativas), (c) modal series con builder de bloques (formato custom, plantillas rápidas, validación tokens), (d) flujo invitación equipo (estado invitado→activo, primer login). Tocar al cerrar Bloque 1+2.
- **FacturaIA — rotar secrets que circularon en chat (2026-05-02)** — `fia_live_ZyuhX…` (API key) y `whsec_fia_q2x…` (webhook secret). Camino simple: crear nuevos en paralelo, sesión portal actualiza Dokploy, eliminar viejos. Ver [[webhook-delete-hibrido-hard-si-no-disparo-soft-si-tiene-historial]]
- **agency-portal PR #50 esperando review Borja** — fix detalle standalone para sombras `facturaia_direct` (`/agency/facturaia/[id]` Server Component + cliente lectura). En main todavía clickear factura fiscal lleva al listado, no al detalle individual. Cuando merge: redeploy portal, queda bug-free. https://github.com/AgentesIA-MAdrid/agency-portal/pull/50
- **agency-portal PR #55 audit actor passthrough** (2026-05-05) — pasa `actor: { email, name }` desde sesión del portal a `/v1/facturas` y `/v1/presupuestos`. FacturaIA `main` `57888f8` ya expone `actor` en `openapi.json` y prod desplegado. Esperando review Borja. https://github.com/AgentesIA-MAdrid/agency-portal/pull/55
- **agency-portal PR consolidado post-merge #54** — abrir cuando #54 mergee: (1) regen `types.gen.ts` contra prod (trae `actor`), (2) quitar 3 `as never` (`auto-emit.ts`, `quotes/service.ts`, `agency-invoices/service.ts`), (3) migration `quotes.converted_facturaia_factura_id` nullable + populate en `convertQuoteToInvoiceAction` con el `id` que devuelve `POST /v1/facturas` (botón "Ver factura" del detalle queda muerto sin esto). Razón de consolidar: regen + #54 colisionan en `types.gen.ts`
- **FacturaIA — smoke tests audit creación tras deploy 2026-05-05**: (1) Crear factura desde dashboard `/generar` → modal detalle muestra tu nombre+email · "Aplicación web". (2) Crear presupuesto vía WhatsApp → muestra tu nombre (si tu phone está en `profiles.phone`) · "Agente WhatsApp / voz". Si tu teléfono no resuelve, debe mostrarlo crudo. (3) Crear desde `/agency/quotes/new` o factura del portal → tras merge PR #55, debe mostrar email del usuario logueado del portal · "API v1" + tooltip "Integración: Agency-panel". (4) Convertir presupuesto a factura desde el portal → factura nueva debe heredar el autor del presupuesto + "Convertida desde presupuesto P2026-XXXX"
- **FacturaIA cleanup mockup AgentesiaLab — pospuesto** — plan SQL ya elaborado (transaccional, conserva 1 factura + 2 presupuestos del portal + 3 clientes referenciados, reset series A→6 P→4 resto→0, borrar PDFs Storage). Org_id `ea201784-4813-4eae-ac3f-9cffdb9cc24a`. Retomar cuando quieras
- **agency-portal main local — 4 commits sin pushear** — `feat(clients) primary_contact_name`, `fix(onboarding) personalización`, `polish(onboarding) impeccable`, `feat(onboarding) WhatsApp`. NO hacer reset hard, hablar con Borja para saber si son PRs pendientes que falta abrir o residuo de sesiones viejas
- **FacturaIA — Voz WhatsApp pendientes producción**: (1) Verificar e2e para TODAS las orgs (lookup, `template_config`, bucket `{org_id}/...`, `documento_url`). (2) Probar OCR recibidas con workflow receptor v2 (rama imagen/documento NO testeada con el nuevo). (3) Probar rama presupuestos (`tipo:'presupuesto'`). (4) Mejorar textos WA (resumen, confirmación con total+link, errores específicos, caption PDF con num+total). (5) Test 6 mensajes en 403 toggles ("admin desactivó este canal", no genérico). (6) Probar invitación con novia tras deploy `98250b9`. (7) Probar modal series. (8) Limpiar duplicados de testing en BD. (9) Quitar `pdf_error` y `detail` del response cuando estable. (10) Archivar sub-workflows antiguos (Voice Process/Confirm/Correct).
- **FacturaIA — Asistente IA multi-canal** — conectar AI assistant al canal WhatsApp para consultas (vencidas, resúmenes, pendientes). Extensiones: cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal. Spec preliminar Bloque 4: `[[facturaia-bloque-4-agent-query-spec]]`
- **Agentesia chatbot ticketing — test con cliente real pendiente** — tool "Crear Ticket" desplegado en `89B9QN23hOHDq6oP`, llega al portal pero el test con número de Manuel devolvió 404 (no tiene `primary_contact_phone`). Pedir que pongan teléfono al cliente "Soporte técnico" y repetir. Verificar también respuestas AI Agent a `TICKET_CREATED` / `TICKET_APPENDED` / `ERROR_NO_CLIENTE`, no romper captación/agendamiento/handoff. Limpiar workflow temporal `a96XVFKX4WujMCKW`.
- **Daily Briefing alternativa al curl bloqueado** — trigger `trig_01THsqqvV3pg3WNnbgvkkdzk` ejecuta y lee vault, pero curl a Slack bloqueado en sandbox. Camino más viable: trigger guarda briefing en `00-home/daily-briefing.md` (push automático), n8n webhook lee y manda a Slack. Alternativas descartadas: PushNotification (200 chars), MCP Slack (no soportado), GitHub Action (overkill).
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API. Token storage per org, template editor con variables
- **FacturaIA — Canales Ingesta + Plan/Facturación (spec 2026-04-24)** — canales rediseño sin toggles, config expandible. Plan: página con planes reales, método pago, historial
- **FacturaIA — Conciliación bancaria IA (spec 2026-04-21)** — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes. Pendiente: plan de implementación
- **Tecnocloud — WhatsApp en FacturaIA** — obtener phone_number_id de Meta, guardar en org, webhook override
- **Simarro — preguntar a Ramón (pendiente)** — (1) ¿Cómo funcionan las citas? ¿Bot reserva directo o primero fecha provisional? (2) ¿Pipeline Kommo actual vale o ajustes? (alquiler ya descartado, bot/voz limpios)
- **Simarro — verificar salesbot 88183** — comprobar que tiene acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo
- **Simarro — IDs TODO en n8n** — `TASK_TYPE_ID_TODO`, `RESPONSIBLE_USER_ID_TODO`, `SHEET_ID_LEADS_WEB_TODO`, calendar de Ramón (ahora `primary`), Supabase pending. ~~salesbots Recordatorios~~ ya OK (87861=4h, 87871=24h, code arreglado para iterar Kommo tasks 2026-05-04)
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

- Clínica Zen — emails rediseñados (4 variantes), hero stripe, datos dinámicos vía Code node "Build Emails HTML" — 2026-05-04
- VeriFACTU integración completa (QR en PDFs todas las plantillas, toggle sincroniza BD, cron cada hora, migración aplicada, deploy prod) — 2026-04-27
- FacturaIA Sprint #6/#7 + workflow voz abono + invitaciones equipo + validación formato series + modal series con builder arrastrable — 2026-04-28
