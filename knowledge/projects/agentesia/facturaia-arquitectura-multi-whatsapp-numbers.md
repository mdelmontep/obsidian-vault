---
title: facturaia arquitectura multi whatsapp numbers para orgs premium
date: 2026-04-25
source: claude-code-session
tags: [facturaia, whatsapp, arquitectura, parking]
---

# Multi WhatsApp numbers — feature aparcada

Idea: tabla `whatsapp_numbers` para asignar números dedicados a orgs premium, además del número global compartido.

## Beneficios

- Números dedicados para orgs de alto volumen (anti-rate-limit Meta)
- Balanceo de carga entre varios números si una sola línea satura
- Org Lookup por `phone_number_id` entrante (en vez de solo por remitente) — más rápido y robusto que matching por número del usuario

## Cambios requeridos

- **BD**: nueva tabla `whatsapp_numbers` con `phone_number`, `phone_number_id` (Meta), `token` (Meta), `org_id` (nullable para global). RLS solo admin/superadmin
- **n8n**: el Org Lookup resuelve primero por `phone_number_id` del receptor (`entry[0].changes[0].value.metadata.phone_number_id`), luego por remitente como fallback
- **Meta Business Manager**: cada número nuevo requiere registro + webhook URL + permisos

## Estado actual

Aparcada. Hoy el número global `919932618` cubre todas las orgs y es configurable desde `/admin/config` (tabla `system_config`). Retomar cuando entre la primera org premium que pida número dedicado.

Relacionado: [[agency-portal-n8n]], [[facturaia-integracion-api-v1-portal]]
