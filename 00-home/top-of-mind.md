---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

_(ninguno activo)_

## Prioridades esta semana

- **FacturaIA — tests proformas + abonos rectificativos** — el flujo de emisión de presupuestos/proformas/abonos ya funciona (form manual + voz). Falta: (1) tests automáticos de proformas (Vitest), (2) tests de abonos rectificativos verificando `factura_origen_id` + total negativo + referencia visible en PDF (cumplimiento fiscal: el abono debe mostrar num+fecha de la factura original que rectifica)
- **agency-portal PR #54 + #55 pendientes de pushear** — #55 audit actor passthrough (`actor: { email, name }` a `/v1/facturas` y `/v1/presupuestos`); #54 ya tiene branch base, pendiente push y review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` nullable + populate con id devuelto por POST. Consolidar regen + #54 en un PR (colisionan en types.gen.ts)
- **FacturaIA cleanup mockup AgentesiaLab — pospuesto** — plan SQL ya elaborado (transaccional, conserva 1 factura + 2 presupuestos del portal + 3 clientes referenciados, reset series A→6 P→4 resto→0, borrar PDFs Storage). Org_id `ea201784-4813-4eae-ac3f-9cffdb9cc24a`. Retomar cuando quieras
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

## Bloqueos

_(ninguno activo)_

## Completado reciente

Ver `00-home/archive-completed.md`
