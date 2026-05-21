---
title: ADR-014 — EcoBox log universal de leads en Google Sheet, no en Chatwoot conversation
date: 2026-05-22
status: accepted
tags: [adr, ecobox, n8n, log, sheet]
---

## Contexto
EcoBox recibe leads por dos canales: voz Retell (workflow `Reservar_cita`) y chat WhatsApp (mismo workflow via tool). Chat crea conversation Chatwoot con `custom_attribute_definitions` rellenos. Voz solo crea evento Calendar + 2 emails. Asimetría: leads de voz no aparecen en Chatwoot, Cristian no tiene listado consolidado.

## Opciones consideradas
- **A — Voz también crea Chatwoot conversation** — workflow añade 3 nodos (POST contact, POST conversation, PATCH attrs+label) en un inbox "API channel" voz_retell. Master list unificada en Chatwoot. Coste: complejidad +3 nodos, "conversation de voz" tiene 1 msg sintético.
- **B — Google Sheet append como log universal** — añadir 1 nodo Sheets append paralelo a emails en `Reservar_cita`. Cristian abre Sheet (o Looker Studio embed) y ve todo.
- **C — Status quo** — solo Calendar + emails. Sin master list.

## Decisión
**B (Sheet append)**, porque (a) menor complejidad (1 nodo vs 3), (b) Cristian ya consume info via email cuando llega lead — Sheet es el "histórico" no el realtime, (c) Looker Studio dashboard sale gratis encima del Sheet, (d) abre vía migración futura a NocoDB cuando crezca sin reescribir Chatwoot voice channel.

## Consecuencias
- `Reservar_cita` workflow tiene fan-out a 4 destinos tras GCal create: Email cliente · Email Cristian · Respond OK · Sheet append. Cada uno con `onError: continueRegularOutput` para que log opcional no rompa flow primario.
- Detección `fuente` por `call_id.startsWith('call_')` → `voz_retell` else `whatsapp`. Convención Retell que no cambia.
- 17 columnas (ver `Ecobox/ecobox_leads_template.csv`). Migración futura a NocoDB conserva headers.
- Cancelar_cita NO actualiza Sheet por ahora (no pedido). Si crece dolor, añadir update por matrícula+gcal_event_id.
- Si OAuth Google falla → Sheet append falla silencioso, emails + Calendar siguen funcionando. Log irrecuperable de ese lead (no crítico, dato en Calendar).
