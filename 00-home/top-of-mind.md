---
title: top of mind
date: 2026-04-26
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

- **Clinica Zen — Corregir email confirmación (2026-04-25)** — imágenes base64, verificar en Gmail/Apple Mail. Workflow `13Roz21TOBwy8gp8` nodo `Send Confirmation Email`

## Prioridades esta semana

- **FacturaIA — Presupuestos/Proformas/Abonos** — ~~Fase 1: presupuestos~~ HECHO (vista completa: filtros, agrupación mes, menú 3 puntos, detalle modal, edición modal con líneas, lazy expiration, funnel dashboard, KPIs, serie P en Generar, número readonly). Fase 2: proformas (tabla/campo, serie T). Fase 3: abonos (rectificativas, serie B, importes negativos). Fase 4: vistas pipeline y métricas
- **FacturaIA — Voz WhatsApp pendientes** — ~~comprobar OCR~~ HECHO (OCR inline en receptor v2, workflow separado desactivado), probar presupuestos, handler texto libre (conectar AI assistant), ~~PDF deformado~~ HECHO (Puppeteer), probar corrección/cancelación, ~~actualizar manuales~~ HECHO
- **FacturaIA — Asistente IA multi-canal** — conectar AI assistant al canal WhatsApp para consultas (vencidas, resúmenes, pendientes). Extensiones: cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal
- **FacturaIA — Google OAuth email por org** — cada org envía desde su email via Gmail API. Token storage per org, template editor con variables
- **FacturaIA — Canales Ingesta + Plan/Facturación (spec 2026-04-24)** — canales rediseño sin toggles, config expandible. Plan: página con planes reales, método pago, historial
- **FacturaIA — Conciliación bancaria IA (spec 2026-04-21)** — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes. Pendiente: plan de implementación
- **Tecnocloud — WhatsApp en FacturaIA** — obtener phone_number_id de Meta, guardar en org, webhook override
- **Simarro — workflow Recordatorios** — nueva API key n8n → actualizar `Oa1lSQuDgEZvZCNS` con salesbot IDs (87861/87863/87865/87871)
- **Clínica Zen — cancelar cita borra Calendar** — workflow `DkueIeGFWLKh8nTj` no borra evento. Añadir nodo
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
