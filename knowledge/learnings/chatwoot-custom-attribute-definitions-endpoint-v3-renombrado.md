---
title: chatwoot v3+ renombra custom_attributes a custom_attribute_definitions
date: 2026-05-22
source: claude-code-session
tags: [chatwoot, api, breaking-change]
---

Endpoint clásico v2 `/api/v1/accounts/{id}/custom_attributes` devuelve **404 HTML** en Chatwoot v3+ (cuando intentas crear o listar custom attributes).

Nombre actual: `/api/v1/accounts/{id}/custom_attribute_definitions`.

Payload sigue igual:
```json
{
  "attribute_display_name": "Matrícula",
  "attribute_display_type": 0,
  "attribute_key": "ecobox_matricula",
  "attribute_model": 0,
  "attribute_values": ["chapa","pintura"]
}
```

`attribute_model`: 0=conversation, 1=contact.
`attribute_display_type`: 0=text, 1=number, 2=currency, 3=percent, 4=link, 5=date, 6=list, 7=checkbox.

Para list: incluir `attribute_values` array.

Caso real: EcoBox 2026-05 — 15 attrs fallaron en bloque con `custom_attributes`, todos OK con `custom_attribute_definitions`.
