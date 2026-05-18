---
title: ADR-001 — Agenda Elphis vía Google Calendar (no API Doctoralia)
date: 2026-05-18
source: investigación agente + integrations.docplanner.com
tags: [adr, elphis, doctoralia, gcal, agenda]
---

# ADR-001 — Agenda de Centro Elphis vía Google Calendar

## Contexto

Centro Elphis usa Doctoralia para captación y agenda. Queremos que un agente de voz Retell y un chatbot WhatsApp puedan **consultar disponibilidad, crear, mover y cancelar citas** en tiempo real durante la conversación.

## Opciones evaluadas

1. **Integrations API oficial de DocPlanner** (`integrations.docplanner.com`). Cubre todo el caso (slots, bookings, webhooks PUSH/PULL, OAuth2). **Pero está restringida a "medical software providers"** (PMS comerciales): proceso de aprobación con kickoff, QA conjunto, implementación obligatoria de todos los métodos, monitorización con pings cada 5 min. No la dan a clínicas individuales ni a integradores ad-hoc.

2. **PMS intermediario ya integrado** (Clinic Cloud u otro de `pro.doctoralia.es/integraciones`). El PMS habla con Doctoralia, nosotros hablamos con el PMS. Robusto y legal — pero requiere que Elphis adopte un PMS (coste, formación, migración).

3. **Google Calendar como bus intermedio**. Doctoralia PRO permite sync nativa con Google Calendar para el profesional. Nosotros leemos/escribimos en GCal vía API; Doctoralia refleja los cambios. Limitaciones: lógica de servicios/duraciones por tipo se mantiene en n8n, no en Doctoralia.

4. **Email/SMS parsing** de las notificaciones de Doctoralia. Solo lectura. No permite crear/cancelar.

5. **Scraping con Playwright** del panel `pro.doctoralia.es`. Viola ToS DocPlanner. RGPD sanitario sin base contractual. Frágil ante cambios UI. Descartado.

## Decisión

**Opción 3: Google Calendar como agenda-service.**

Detrás de un sub-workflow n8n `agenda-service` con contrato estable: `check_availability`, `book_slot`, `cancel_slot`, `reschedule_slot`, `list_upcoming`. Toda la lógica de servicios/duraciones vive en n8n + Postgres `agenda_cache`. Doctoralia espeja vía su integración nativa con GCal.

## Razones

- Único camino legal sin obligar a Elphis a contratar PMS.
- API estable y documentada (Google).
- Si mañana DocPlanner abre acceso o Elphis adopta Clinic Cloud, **se sustituye solo el backend** del `agenda-service` sin tocar consumidores (Retell tools, chatbot WhatsApp, crons).
- Compatible con que el paciente reserve directo en doctoralia.es: la cita aparece en GCal y un cron de n8n la sincroniza a Clientify.

## Riesgos asumidos

- **No hay webhook GCal nativo** para algunos eventos → cron cada 10 min con delta `updatedMin`. Tolerancia de ~10 min en notificaciones inversas (aceptable para clínica).
- **OAuth refresh token caduca** si no se usa → workflow `keepalive` semanal.
- **Si Doctoralia rompe su integración con GCal**, perdemos la sync inversa de citas creadas por paciente en su web. Fallback: parsing IMAP del email de notificación a la clínica como segundo canal.

## Implementación

Ver [[workflows-n8n-elphis]] sub-workflow `agenda-service` y trigger `doctoralia-incoming-sync`.

## Revisar si

- DocPlanner abre la Integrations API a integradores.
- Elphis decide adoptar un PMS listado en `pro.doctoralia.es/integraciones`.
- El volumen supera ~100 citas/día (entonces el cron de 10min se queda corto).

## Relacionado

- [[arquitectura-elphis]]
- [[workflows-n8n-elphis]]
