---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

_(ninguno activo)_

## Prioridades esta semana

- **FacturaIA — Presupuestos/Proformas/Abonos** — ~~backend voz proforma/abono~~ HECHO. Pendiente Bloque 1 form manual `generar-view.tsx`: SERIE_POR_TIPO mal (proforma=T, abono=A → debe ser F y B), no setea `tipo_documento` ni `factura_origen_id`, falta selector factura origen abono manual, GET `/api/render-pdf?tipo=&id=`, rama `presupuesto_id` en `/api/email/send`. Bloque 2 vistas separadas presupuesto/proforma + abonos en emitidas + estado `pagada`. Bloque 4 `/api/agent/query/*` queries naturales — ver spec `[[facturaia-bloque-4-agent-query-spec]]`. Bloque 5 métricas tiempo medio + manuales con: (a) proforma como entidad (serie F, conversión a factura, "pagada" intermedia), (b) abono fiscal (serie B, total negativo, `factura_origen_id`, fundamento rectificativas), (c) modal series con builder de bloques (formato custom, plantillas rápidas, validación tokens), (d) flujo invitación equipo (estado invitado→activo, primer login). Tocar al cerrar Bloque 1+2.
- **agency-portal PR #54 + #55 pendientes de pushear** — #55 audit actor passthrough (`actor: { email, name }` a `/v1/facturas` y `/v1/presupuestos`); #54 ya tiene branch base, pendiente push y review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` nullable + populate con id devuelto por POST. Consolidar regen + #54 en un PR (colisionan en types.gen.ts)
- **FacturaIA cleanup mockup AgentesiaLab — pospuesto** — plan SQL ya elaborado (transaccional, conserva 1 factura + 2 presupuestos del portal + 3 clientes referenciados, reset series A→6 P→4 resto→0, borrar PDFs Storage). Org_id `ea201784-4813-4eae-ac3f-9cffdb9cc24a`. Retomar cuando quieras
- **FacturaIA — Voz WhatsApp pendientes producción**: (1) Verificar e2e para TODAS las orgs (lookup, `template_config`, bucket `{org_id}/...`, `documento_url`). (2) Probar OCR recibidas con workflow receptor v2 (rama imagen/documento NO testeada con el nuevo). (3) Probar rama presupuestos (`tipo:'presupuesto'`). (4) Mejorar textos WA (resumen, confirmación con total+link, errores específicos, caption PDF con num+total). (5) Test 6 mensajes en 403 toggles ("admin desactivó este canal", no genérico). (6) Probar invitación con novia tras deploy `98250b9`. (7) Probar modal series. (8) Limpiar duplicados de testing en BD. (9) Quitar `pdf_error` y `detail` del response cuando estable. (10) Archivar sub-workflows antiguos (Voice Process/Confirm/Correct).
- **FacturaIA — Asistente IA multi-canal** — conectar AI assistant al canal WhatsApp para consultas (vencidas, resúmenes, pendientes). Extensiones: cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal. Spec preliminar Bloque 4: `[[facturaia-bloque-4-agent-query-spec]]`
- **Agentesia chatbot ticketing — test con cliente real pendiente** — tool "Crear Ticket" desplegado en `89B9QN23hOHDq6oP`, llega al portal pero el test con número de Manuel devolvió 404 (no tiene `primary_contact_phone`). Pedir que pongan teléfono al cliente "Soporte técnico" y repetir. Verificar también respuestas AI Agent a `TICKET_CREATED` / `TICKET_APPENDED` / `ERROR_NO_CLIENTE`, no romper captación/agendamiento/handoff. Limpiar workflow temporal `a96XVFKX4WujMCKW`.
- **Daily Briefing alternativa al curl bloqueado** — trigger `trig_01THsqqvV3pg3WNnbgvkkdzk` ejecuta y lee vault, pero curl a Slack bloqueado en sandbox. Camino más viable: trigger guarda briefing en `00-home/daily-briefing.md` (push automático), n8n webhook lee y manda a Slack. Alternativas descartadas: PushNotification (200 chars), MCP Slack (no soportado), GitHub Action (overkill).
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API. Token storage per org, template editor con variables
- **FacturaIA — Canales Ingesta + Plan/Facturación (spec 2026-04-24)** — canales rediseño sin toggles, config expandible. Plan: página con planes reales, método pago, historial
- **FacturaIA — Conciliación bancaria IA (spec 2026-04-21)** — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes. Pendiente: plan de implementación
- **FacturaIA — pestaña notificaciones por org** — inbox unificado: anomalías OCR + sugerencias IA + vencimientos + errores. Campana topbar + drawer feed cronológico. Base ya construida (`module_events`). Spec: `docs/MODULOS-PRODUCTO.md`. ~1-2 días
- **FacturaIA — backends módulos pendientes** — Cobros (recordatorios escalados), Fiscal (modelos AEAT 303/111/115/347), Firma eIDAS, Cashflow IA forecast. ~21 opciones config con badge "Próximamente" hasta que se implementen. Cobros y Stripe los primeros (alta conversión)
- **FacturaIA — Stripe en activación add-ons** — hoy CTA "Activar +XX€/mes" redirige a `/settings?tab=plan` sin cobro real. Conectar Stripe checkout para que el toggle = compra. Conciliación 19€/mes y Anti-fraude 9€/mes ya seedeados
- **FacturaIA — conexión bancaria automática (Plaid/GoCardless/BBVA Open Banking)** — desbloquea Conciliación al 100%, hoy requiere import manual de `movimientos_bancarios`. Sin esto el módulo es infrautilizado
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
