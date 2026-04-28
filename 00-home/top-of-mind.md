---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

- **Clinica Zen — Corregir email confirmación (2026-04-25)** — imágenes base64, verificar en Gmail/Apple Mail. Workflow `13Roz21TOBwy8gp8` nodo `Send Confirmation Email`

## Prioridades esta semana

- **FacturaIA — Presupuestos/Proformas/Abonos** — ~~backend voz proforma/abono~~ HECHO. Pendiente Bloque 1 form manual `generar-view.tsx`: SERIE_POR_TIPO mal (proforma=T, abono=A → debe ser F y B), no setea `tipo_documento` ni `factura_origen_id`, falta selector factura origen abono manual, GET `/api/render-pdf?tipo=&id=`, rama `presupuesto_id` en `/api/email/send`. Bloque 2 vistas separadas presupuesto/proforma + abonos en emitidas + estado `pagada`. Bloque 4 `/api/agent/query/*` queries naturales. Bloque 5 métricas tiempo medio + manuales con proforma/abono/modal series visibles
- **FacturaIA — Voz WhatsApp pendientes** — Test 6 mensajes específicos en 403 toggles ("admin desactivó este canal", no error genérico). Probar invitación con novia tras deploy `98250b9`. Probar modal series tras deploy
- **FacturaIA — Asistente IA multi-canal** — conectar AI assistant al canal WhatsApp para consultas (vencidas, resúmenes, pendientes). Extensiones: cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API. Token storage per org, template editor con variables
- **FacturaIA — Canales Ingesta + Plan/Facturación (spec 2026-04-24)** — canales rediseño sin toggles, config expandible. Plan: página con planes reales, método pago, historial
- **FacturaIA — Conciliación bancaria IA (spec 2026-04-21)** — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes. Pendiente: plan de implementación
- **Tecnocloud — WhatsApp en FacturaIA** — obtener phone_number_id de Meta, guardar en org, webhook override
- **Simarro — workflow Recordatorios** — nueva API key n8n → actualizar `Oa1lSQuDgEZvZCNS` con salesbot IDs (87861/87863/87865/87871)
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
