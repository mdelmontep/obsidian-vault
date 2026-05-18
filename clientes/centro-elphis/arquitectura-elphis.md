---
title: Centro Elphis — Arquitectura
date: 2026-05-18
source: diseño técnico tras discovery Clientify + onboarding firmado
tags: [elphis, arquitectura, retell, chatwoot, clientify, doctoralia, n8n, supabase, dokploy]
---

# Arquitectura · Centro Elphis

## Stack final propuesto

| Capa | Servicio | Notas |
|---|---|---|
| **CRM** | Clientify | Single source of truth del paciente. Pipeline propio del cliente ya operativo (ID 56886). Ver [[clientify-discovery-elphis]]. |
| **Inbox WhatsApp + handoff humano** | Chatwoot self-hosted en Dokploy | Cuenta dedicada Elphis. Decide el arranque (bloqueante de [[bloqueantes-elphis]]). |
| **WhatsApp** | Meta Cloud API directo | Arrancamos con número de pruebas Agentesia; migración al 659 877 708 al validar E2E. |
| **Voz** | Retell + ElevenLabs castellano femenino | Desvío del 659 877 708 al agente si no contesta nadie en 3 tonos. Nombre del bot: Laura. |
| **Orquestador** | n8n dedicado en Dokploy actual | Stack `n8n-elphis` + Postgres interno propio. Aislamiento de credenciales sanitarias. |
| **Base de datos auxiliar** | Supabase self-hosted en Dokploy | Stack `supabase-elphis`. Postgres + pgvector + Storage + REST. Deja la puerta abierta a RAG y guardado de audios. |
| **Agenda** | Google Calendar de Enrique Sanz como puente | Doctoralia sincroniza nativa con GCal del profesional. Su API está cerrada a clínicas individuales. Ver [[ADR-001-doctoralia-google-calendar]]. |

## Diagrama lógico

```
                ┌──────────────────────────┐
                │   PSTN · 659 877 708     │  ← desvío si no contesta 3 tonos
                └────────────┬─────────────┘
                             │ voz
                      ┌──────▼──────┐
                      │   Retell    │  Laura · ElevenLabs castellano
                      │   (LLM)     │  Transfer 112 sólo crisis = 717 003 717
                      └──────┬──────┘
                             │ custom tools + post-call webhook
   ┌──────────────┐    ┌─────▼─────┐    REST   ┌──────────────┐
   │  WhatsApp    │───►│    n8n    │◄─────────►│  Clientify   │
   │ (Chatwoot)   │◄───│           │           │ (SoT lead)   │
   └──────────────┘    └─┬──┬──┬───┘           └──────────────┘
                         │  │  │
                  GCal   │  │  │   tablas aux + RAG (futuro)
                  ┌──────┘  │  └─────────┐
                  ▼         ▼            ▼
            ┌─────────┐ ┌──────┐    ┌──────────┐
            │ Google  │ │ Cron │    │ Supabase │
            │ Calendar│ │ jobs │    │ pgvector │
            └────┬────┘ └──────┘    └──────────┘
                 │ link nativo
                 ▼
            ┌──────────┐
            │Doctoralia│  refleja citas, NO es destino API
            └──────────┘
```

## Single source of truth por entidad

| Entidad | Owner | Notas |
|---|---|---|
| Paciente / lead | **Clientify** | Match por teléfono E.164. URL-encode el `+`. |
| Cita (estado real) | **Google Calendar de Enrique** | Doctoralia espeja, no es destino API. |
| Espejo de cita | Clientify (custom field `gcal_event_id`) | Para reporting y recordatorios. |
| Conversación WhatsApp | **Chatwoot** | Historial + handoff humano nativo. |
| Transcript llamada | **Retell** + copia textual como nota Clientify | Audio queda en Retell, retención 30 d. |
| Memoria conversacional bot | Postgres del n8n (`chat_memory`) | TTL 30 d. |
| Tablas auxiliares bot | **Supabase Elphis** | `paciente_cache`, `conversation_state`, `agenda_cache`, `call_log`. |
| KB FAQs adicciones | KB Retell + Supabase pgvector si crece | Datos verificados solo. |

## Tablas auxiliares (Supabase)

- **paciente_cache** — espejo ligero del contacto Clientify indexado por teléfono E.164. Evita pegarle a la API de Clientify en cada turno.
- **conversation_state** — bot_paused_until, último intent, contador handoffs por conversación.
- **agenda_cache** — citas materializadas desde GCal para alimentar recordatorios sin pegarle a Google cada vez.
- **call_log** — metadatos de cada llamada Retell: call_id, duración, intent_final, transcript_url, sentiment.

## Handoff humano (resumen)

Tres caminos según el caso:

1. **Petición humano en llamada · dentro de horario** → Laura transfiere la llamada a recepción. Frase: «Te paso con una compañera, un momento.»
2. **Resto de casos (notificación interna)** → WhatsApp interno al equipo. Sin transferencia:
   - Interés en ingreso → al 659 877 708.
   - Resto → al número directo de la recepcionista (pendiente Alba).
3. **Crisis vital** → transferencia inmediata al Teléfono de la Esperanza (717 003 717). Ver [[protocolo-crisis-elphis]].

## Riesgos top 5 y mitigaciones

1. **GCal/Doctoralia desincronizan** (cambio UI Doctoralia, OAuth caduca) → tests E2E diarios + alerta Slack + fallback «tomo datos y te llaman».
2. **Doble booking** (voz vs chat vs paciente vía web) → lock distribuido Redis por `slot_id` + re-check antes de confirmar.
3. **RGPD art. 9** (datos de salud) → DPA con Retell + OpenAI + Meta. Audio 30 d. Consentimiento explícito al inicio. Ver [[dpas-rgpd]].
4. **Clientify rate limit no documentado** → backoff exponencial, caché Postgres, batch nocturno.
5. **Latencia tool Retell** (objetivo n8n < 1.5 s, timeout 10 s) → pre-warm disponibilidad GCal en Redis, filler phrases en el agente.

## Stacks Dokploy a crear

- `n8n-elphis` · n8n dedicado con Postgres interno propio.
- `supabase-elphis` · Supabase self-hosted (pgvector + Storage).
- Cuenta `elphis` en Chatwoot compartido del Dokploy actual (no stack nuevo).

## Relacionado

- [[index|Centro Elphis HUB]]
- [[clientify-discovery-elphis]]
- [[protocolo-crisis-elphis]]
- [[bloqueantes-elphis]]
- [[propuesta-pdf-elphis]]
- [[ADR-001-doctoralia-google-calendar]]
- [[dpas-rgpd]]
