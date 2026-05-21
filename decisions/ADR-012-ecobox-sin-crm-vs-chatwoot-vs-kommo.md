---
title: ADR-012 — Stack EcoBox sin CRM tradicional, Chatwoot como inbox unificado
date: 2026-05-22
status: accepted
tags: [adr, ecobox, crm, chatwoot]
---

## Contexto
Taller de chapa y pintura EcoBox 360 (Las Rozas, ~30-50 leads/mes esperados, 1 admin Cristian + 2 compañeros taller futuros). Necesita captar leads por voz (Retell) + WhatsApp y gestionarlos. Plan inicial era Kommo como CRM (paquete 4 de skill pollo-costco). Cristian descartó Kommo por curva de aprendizaje.

## Opciones consideradas
- **A — Kommo Avanzado** — pipeline visual + salesbots HSM + custom fields. €15/user/mes. Curva alta para Cristian. Descartado por cliente.
- **B — Chatwoot self-hosted compartido AgentesIA** — inbox WhatsApp + labels=pipeline + custom_attribute_definitions=campos. Multi-cliente con prefijo `ecobox_*`. Cero infra extra (ya desplegado). Notificaciones push nativas móvil + asignación a agentes.
- **C — Solo Google Sheet** — 22 columnas, vistas filtradas, sin chat UI unificada. Más barato pero peor UX y sin histórico mensajes.
- **D — NocoDB self-hosted en Dokploy EcoBox** — base de datos visual con API y relaciones, alternativa futura a Chatwoot+Sheet si escala.

## Decisión
**B (Chatwoot compartido AgentesIA)**, porque (a) ya está desplegado y Cristian puede instalar la app móvil gratis con push, (b) labels + custom_attribute_definitions cubren pipeline + datos estructurados sin custom code, (c) handoff bot→humano nativo via assign + label, (d) coste marginal cero. Reevaluar a D NocoDB cuando supere 60 leads/mes sostenidos o entre segundo asesor.

## Consecuencias
- Sin pipeline visual tipo Kommo: estado se gestiona con labels (`ecobox-nuevo`, `ecobox-cita-agendada`, …) filtradas en UI Chatwoot.
- Multi-tenancy débil en Chatwoot compartido: todos los labels y custom attrs son de toda la cuenta. Mitigación: prefijo `ecobox_*` consistente para que filtros UI funcionen por cliente.
- Reporting via Looker Studio conectado a export Chatwoot (pendiente). 
- Migración futura a NocoDB queda como opción si dolor real aparece.
