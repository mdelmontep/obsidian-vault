---
title: Centro Elphis — Arquitectura
date: 2026-05-18
source: agente Plan + decisiones Manu
tags: [elphis, arquitectura, retell, chatwoot, clientify, doctoralia, n8n, dokploy]
---

# Arquitectura Centro Elphis

## Diagrama lógico

```
                          ┌─────────────────────────────┐
                          │       PSTN / número ES      │
                          └──────────────┬──────────────┘
                                         │ voz
                                  ┌──────▼──────┐
                                  │  Retell AI  │  (LLM + voz ElevenLabs ES + transcript)
                                  └──────┬──────┘
                                         │ custom tools (HTTP)
                                         │ + post-call webhook (call_analyzed)
   ┌──────────────┐   inbound   ┌────────▼────────┐   REST   ┌──────────────┐
   │  WhatsApp    │────────────►│      n8n        │◄────────►│  Clientify   │
   │ (Chatwoot)   │◄────────────│  (orquestador)  │          │ (SoT lead)   │
   └──────────────┘  outbound   └─┬─────┬─────┬───┘          └──────────────┘
                                  │     │     │
                                  │     │     │
                                  ▼     ▼     ▼
                         ┌──────────┐ ┌────────┐ ┌──────────────────┐
                         │  Google  │ │Postgres│ │ Cron: GCal sync  │
                         │ Calendar │ │ (cache)│ │ + recordatorios  │
                         └────┬─────┘ └────────┘ └──────────────────┘
                              │ link a perfil
                              ▼
                         ┌──────────┐
                         │Doctoralia│  ← refleja citas, no es API destino
                         └──────────┘
```

## Single source of truth

| Entidad | Owner | Notas |
|---|---|---|
| Paciente/lead | **Clientify** | Match por teléfono E.164. |
| Cita (estado real) | **Google Calendar** del profesional | Doctoralia espeja, no es destino API. |
| Espejo de cita | Clientify (custom field `gcal_event_id`) | Para reporting/recordatorios. |
| Conversación WhatsApp | **Chatwoot** | Historial + handoff humano. |
| Transcript llamada | **Retell** + copia textual como nota en Clientify | Audio queda en Retell (retención 30d). |
| Memoria conversacional bot | Postgres n8n (`chat_memory` por `wa_id`) | TTL 30d. |
| RAG (FAQs, info clínica) | Embeddings en Postgres o Supabase compartido | Datos verificados por Elphis solo. |

## Stack

| Capa | Servicio | Justificación |
|---|---|---|
| Voz | Retell + ElevenLabs castellano | Conversation Flow para evitar alucinaciones de horarios. |
| Telefonía | Twilio número ES | Soporte fácil import SIP a Retell, $1/mes + $0.015/min. |
| Chat | WhatsApp Cloud vía 360dialog (BSP UE) | DPA UE, sin markup, RGPD sanitario ok. |
| Bandeja | Chatwoot self-hosted | Patrón Agentesia, handoff vía `bot_paused`. |
| CRM | Clientify único | No meter Kommo: duplicaría source of truth. |
| Agenda | Google Calendar | API Doctoralia cerrada → GCal con sync nativo al perfil del profesional. Ver [[ADR-001-doctoralia-google-calendar]]. |
| Orquestación | n8n dedicado | Aislamiento credenciales sanitarias. |
| Estado | Postgres dedicado del stack | `paciente_cache`, `conversation_state`, `agenda_cache`, `call_log`. |

## Riesgos top 5

1. **GCal/Doctoralia desincronizan** (cambio UI Doctoralia, OAuth caduca) → tests E2E diarios + alerta Slack + fallback "tomo datos y te llaman".
2. **Doble booking** (voz vs chat vs paciente web) → lock distribuido Redis por `slot_id` + re-check antes de confirmar.
3. **RGPD art. 9** (datos salud) → DPA con Retell + OpenAI + 360dialog. Audio 30d. Consentimiento explícito al inicio.
4. **Clientify rate-limit no documentado** → backoff exponencial, caché Postgres, batch nocturno.
5. **Latencia tool Retell** (objetivo n8n <1.5s, timeout 10s) → pre-warm disponibilidad GCal en Redis, filler phrases en el agente.

## Relacionado

- [[index|Centro Elphis HUB]]
- [[ADR-001-doctoralia-google-calendar]]
- [[workflows-n8n-elphis]]
- [[dokploy-deploy-elphis]]
