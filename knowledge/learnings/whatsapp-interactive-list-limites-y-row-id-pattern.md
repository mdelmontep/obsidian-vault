---
title: WhatsApp Interactive List — límites Meta y patrón row.id "tipo:UUID"
date: 2026-05-21
source: claude-code-session
tags: [whatsapp, meta-cloud-api, n8n, interactive]
---

Límites Meta Cloud API para `interactive.type='list'`:

- `body.text` ≤ 1024 chars
- `action.button` ≤ 20 chars (texto del CTA inferior)
- `action.sections[].title` ≤ 24 chars
- `action.sections[].rows[].title` ≤ 24 chars (visible en lista)
- `action.sections[].rows[].description` ≤ 72 chars (opcional, segunda línea)
- `action.sections[].rows[].id` ≤ 200 chars (callback ID, no visible)
- Máximo 10 rows totales (10 secciones × 1 row, o 1 sección × 10 rows).
- `footer.text` ≤ 60 chars.

Patrón para `row.id` cuando el router downstream debe diferenciar tipo de selección: usar prefijo `tipo:datos`, ej. `org_select:b5f86e8f-4c44-4a44-89d0-acccd8d4530e`. El switch n8n filtra con regex `^org_select:` y extrae el UUID con `.replace("org_select:", "")`.

Defense in depth: el backend revalida que el UUID extraído sea legítimo para ese user antes de actuar (no fiar de `list_reply.id` — un cliente WhatsApp manipulado puede enviar cualquier valor). Caso real TuFacturaIA 2026-05-21: select-org endpoint revalida `org_members.estado='activo'`.

Truncado de title: nombres >24 chars cortar con `.slice(0,24)`. Si colisionan tras truncado (ej. "Grupo Agentesia Madrid" y "Grupo Agentesia Barcelona"), añadir descripción.
