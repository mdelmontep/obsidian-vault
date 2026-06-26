---
title: clinica-zen
date: 2026-05-07
tags: [cliente, clinica-zen]
---

# Clínica Zen

Clínica fisioterapia/salud. Chatbot Chatwoot + agente voz Retell + emails marketing + Kommo. Contactos: Gonzalo (legacy), Dani.

## Estado

- **Chatbot + voz** completados 2026-04-23
- **Emails rediseñados** (4 variantes, hero stripe, datos dinámicos vía Code node "Build Emails HTML") — 2026-05-04
- **Cancelación Retell** workflow `DkueIeGFWLKh8nTj` con bug status_id

## Próximos hitos

1. **status_id Kommo 'Cita cancelada'** (NEXT) — workflow `DkueIeGFWLKh8nTj` `Update leads1` da 400 NotSupportedChoice (104115987 heredado de Gonzalo). Pedir ID correcto pipeline 13495347
2. **Configurar Retell en leads entrantes** (LATER) — workflow `RN0wl8RaRmwLpnfQ`, verificar webhooks dominio CZ
3. **Bug recordatorios por task_type** — el workflow disparaba recordatorio por cualquier tarea; viene del blueprint compartido con Simarro. Revisar si CZ lo tiene. Ver [[recordatorios-visita-por-task-type]]

## Bloqueos / esperando a terceros

- ID correcto del status "Cita cancelada" en pipeline 13495347 (preguntar a quien gestiona Kommo)

## Links rápidos

- n8n: `DkueIeGFWLKh8nTj` (cancelar Retell), `RN0wl8RaRmwLpnfQ` (leads entrantes)
- Repo email-assets: AgentesIAMadrid/email-assets/clinica-zen/

## Histórico de hitos

- 2026-05-04: emails rediseñados con hero stripe + Code node
- 2026-04-29: fix `$if(isExecuted)` en Update leads1 + error handler con JSON.stringify
- 2026-04-23: chatbot + voz completados
