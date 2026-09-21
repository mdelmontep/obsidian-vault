---
title: una plantilla waba de kommo queda atada a la fuente donde se aprobó; al cambiar de línea falla
date: 2026-09-21
source: simarro
tags: [kommo, whatsapp, plantillas, salesbot]
---
Síntoma: el salesbot manda la plantilla y en el chat sale "Error", mientras otras plantillas del mismo
bot/cuenta llegan bien. Kommo la sigue mostrando como `approved`.

Causa: la aprobación es por fuente (número/WABA). Si la cuenta cambió de línea, las plantillas creadas
antes siguen aprobadas en la fuente vieja y el envío por la nueva falla.

Diagnóstico por API (sin UI): `GET /api/v4/chats/templates?with=reviews` → `_embedded.reviews[].source_id`
por plantilla; `GET /chats/templates/{id}` → `waba_selected_waba_ids`. Las que difieren del resto son las rotas.
Caso Simarro: "Valoración" y "Plantilla 4 horas" (11-may) en source 23064219; las demás (≥28-may) en 23065722.

Fix: recrear la plantilla en la UI con la línea actual y repuntar el salesbot (una aprobada no se edita:
[[plantilla-waba-en-kommo-se-crea-y-edita-solo-desde-la-ui]]). `GET /api/v4/bots` lista los salesbots con nombre e id.
