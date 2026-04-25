---
title: facturaia multi whatsapp numbers
date: 2026-04-25
source: claude-code-session
tags: [facturaia, whatsapp, arquitectura]
---

Idea discutida: tabla `whatsapp_numbers` para asignar números dedicados a orgs premium.

Permitiría:
- Números dedicados para orgs de alto volumen
- Balanceo de carga entre varios números
- Org Lookup por `phone_number_id` entrante (en vez de solo por remitente)

Requiere cambios en:
- BD: nueva tabla con phone_number, phone_number_id, token Meta, org_id (nullable para global)
- n8n: Org Lookup resuelve primero por phone_number_id del receptor, luego por remitente
- Meta Business Manager: cada número nuevo requiere registro + webhook

Dejado para cuando haya demanda real. Hoy el número global `919932618` es suficiente y es configurable desde `/admin/config` (tabla `system_config`).
