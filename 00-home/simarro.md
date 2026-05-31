---
title: simarro
date: 2026-05-31
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria (Las Rozas, Madrid). Chatbot WhatsApp + agente de voz Retell "Ana" + Kommo CRM + catálogo Idealista (Supabase) + scraping. Contacto: Ramón.

> Source of truth técnico: `/Users/manueldelmonte/simarro/CLAUDE.md`. Snapshot detallado: [[estado-actual]]. Routing/buffer citas: [[routing-citas-por-agente]].

## Estado (2026-05-31)

- **Voz Ana (Retell)** — `agent_7b02aa7680b8798ea033fab2c2`, **PUBLICADA v29**. Llama a `+34 919 93 28 52`. Busca viviendas, mira disponibilidad (con buffer), reserva (pide nombre), cancela, deriva.
- **Disponibilidad con buffer real** — visitas 1h; misma vivienda pega (0 min), distinta vivienda del mismo agente +30 min. `Mirar_disponibilidad` devuelve `slots` ya filtrados; recheck anti-doble-booking en la reserva. E2E verificado (lead Kommo + evento calendar).
- **Chatbot WhatsApp** activo (`QLfRT9AWmV1HLMZs`), mismo motor de disponibilidad.
- **Kommo** integrado (pipeline `13546071` + 4 pipelines de forms web), salesbots recordatorio.
- **Catálogo Idealista** en Supabase (`properties`), sync diario vía Apify.

## Pendiente go-live por-agente (bloqueante)

1. **Ramón añade `agente: <nombre>`** a las descripciones de Idealista → hoy `properties.agent=NULL` en todas → todas las citas caen en el calendario general `consultingsimarroproperties@gmail.com`.
2. Correr sync (`Lanzar scrape Simarro (manual)`, workflow `3zBDpPwBYLZgMink`) para poblar `properties.agent`.
3. E2E con vivienda de agente real → cita en su calendario.

## Otros pendientes

- **Limpiar leads test Kommo** sesión 2026-05-31 (ver [[estado-actual]] §pendientes).
- **Cred SMTP Gmail** en n8n (`oKRmYFhljczyvzV8` es fantasma → 0 emails). App Password de `simarroproperties@gmail.com`.
- **Preguntar a Ramón**: ¿citas bot-directo o fecha provisional? ¿pipeline Kommo actual vale?
- **LATER**: monitor inmuebles tipo StateFox · desplegar Supabase RAG (workflow `meter info rag` inactivo).

## Links rápidos

- n8n: `n8nsimarro.agentesia.madrid` · workflows clave: `iMoTKZWxYLymGuHF` (citas/disponibilidad), `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), `QLfRT9AWmV1HLMZs` (chatbot)
- Kommo: `simarro.kommo.com` · Retell: `+34 919 93 28 52` · transfer humano `+34 629 12 78 16`

## Histórico de hitos

- 2026-05-31: Ana voz publicada (v29) + disponibilidad con buffer real (slots) + recheck + E2E verificado
- 2026-05-28: routing por agente + WA confirmación voz + bugs Retell
- 2026-05-04: chatbot lentitud arreglada · salesbots recordatorios
