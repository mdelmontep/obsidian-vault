---
title: kommo salesbot jsons del drive tienen datos hardcodeados de cz — adaptar antes de importar
date: 2026-04-28
source: claude-code-session
tags: [kommo, salesbot, migración]
---

Los JSONs de `salesbot kommo/` en Google Drive son de Clínica Zen / Grupo Médico Capilar.
Antes de importar en un cliente nuevo, reemplazar:

- `lead.cf.3084042` (fecha cita CZ) → ID del campo "Próxima cita" del cliente (`GET /api/v4/leads/custom_fields`)
- `lead.cf.3126552` (especialista CZ) → ID equivalente si existe; si no, eliminar referencia del texto
- `template_id` (18148, 18166, 18192…) → **eliminar** (son IDs de plantillas HSM de la cuenta CZ, inválidos en otras cuentas)
- Texto: reemplazar nombre negocio, dirección, URL de Maps
- "Confirmacion Cita" tiene un paso `set_custom_fields` para el especialista — eliminar si el cliente no tiene ese campo
