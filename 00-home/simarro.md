---
title: simarro
date: 2026-06-01
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria (Las Rozas, Madrid). Chatbot WhatsApp + agente de voz Retell "Ana" + Kommo CRM + catálogo Idealista (Supabase) + scraping. Contacto: Ramón.

> Source of truth técnico: `/Users/manueldelmonte/simarro/CLAUDE.md`. Snapshot detallado: [[estado-actual]]. Routing/buffer citas: [[routing-citas-por-agente]].

## Estado (2026-06-02)

- **Voz Ana — el agente PRODUCTIVO es el Conversation Flow** `agent_0df7f123e7e3c24d99c9152358` (`conversation_flow_19ca70e19b3f`, gpt-4.1 cascading). ⚠️ El `agent_7b02aa...` (retell-llm) está **EN DESUSO**. Llama a `+34 919 93 28 52`. Busca, mira disponibilidad, reserva (pide nombre + consentimiento), cancela/cambia, deriva.
- **Visitas de 30 min** (solicitud Simarro 2026-06-01; antes 1h). Buffer mismo agente: **0 min misma vivienda, 60 min (1h margen) distinta**. Slots :00 y :30 → **10:00–13:30 y 17:00–19:30**. SSOT: `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), compartida voz+WhatsApp.
- **Chatbot WhatsApp** activo (`QLfRT9AWmV1HLMZs`): `Mirar_disponibilidad` convertido a `toolWorkflow` (el HTTP tool no exponía args al LLM) → sub `Disponibilidad (tool)` (`aUENlbhCLPhPAVvV`). Red backend que ancla el `idealista_id` en el lead cuando la búsqueda da 1 vivienda.
- **Kommo** integrado (pipeline `13546071` + 4 pipelines forms web), salesbots recordatorio.
- **Catálogo Idealista** en Supabase (`properties`), sync diario vía Apify. Ramón YA empezó a poner `agente:` (el dúplex de Pozuelo resuelve a Carlos).
- **Matching multi-pool (2026-06-02)** — el pool ya son **3 etapas en 3 embudos** (Ventas `106971083` + Capacidad de compra `105358051` + Personal Shopper `105358071`), editado en `Reconcile lead_preferences`. Verificado E2E (llegó el WhatsApp del piso de Pozuelo).
- **Recordatorios de visita (2026-06-02)** — anclados a una **tarea Meeting (type 2)** que la reserva crea con `complete_till`=hora de visita; el matching pasó su tarea a Follow-up (1) y Recordatorios filtra solo type 2 → mata el recordatorio falso del matching y habilita los recordatorios reales (antes no existían). Ver [[recordatorios-visita-por-task-type]].

## ⚠ PENDIENTE BLOQUEANTE — reorden recheck en VOZ (no tocar a ciegas)

**Bug del orden (confirma antes de validar)**: el flujo de reserva confirmaba la cita (salesbot Kommo + respuesta al cliente) ANTES del recheck de disponibilidad → con buffer 60 confirma slots ocupados y NO crea el evento. **WhatsApp YA arreglado** (2026-06-01: recheck antes de `Update leads`/crear evento; solo confirma si libre). **VOZ PENDIENTE**: el respond-fast (`Respond FAST`, atado al timeout 6s de Retell) confirma de inmediato, y `Create new leads3/2` crea el lead en **Lead Caliente (105137095)** → salesbot dispara al crear, antes del recheck. Arreglarlo = (1) crear lead en status neutro y mover a Lead Caliente solo en rama libre, (2) recheck antes del respond-fast. NO hacer PUT a ciegas: toca automations de Kommo no inspeccionables + timeout Retell; **requiere test de llamada real tras el cambio**.

## Pendiente — tests E2E reales

Cambios aplicados sin probar en vivo:
1. **WhatsApp reserva**: cae en calendario del agente (red backend anclaje idealista) y, tras el reorden, NO confirma si el slot está ocupado.
2. **Cambio de cita**: nuevo evento en calendario del agente, 30 min, borra el viejo.
3. **Buffer**: misma casa pegadas (10:00–10:30 / 10:30–11:00); casa distinta → 60 min margen (no antes de 11:30).
4. **Voz**: latencia (voz `turbo_v2_5`, `responsiveness 0.85` que no corte) — independiente del reorden pendiente de arriba.
5. **Subir tier OpenAI** (chatbot WA gpt-4o, hoy 30k TPM → rate limits).

## Otros pendientes

- Confirmar cobertura de `properties.agent` poblado en TODAS las viviendas (Ramón).
- **Cred SMTP Gmail** en n8n (`oKRmYFhljczyvzV8` fantasma → 0 emails). App Password de `simarroproperties@gmail.com`.
- Limpiar leads test Kommo.
- **LATER**: `meter info rag` cerrado (no se usa, sin documentos); monitor inmuebles tipo StateFox.

## Links rápidos

- n8n: `n8nsimarro.agentesia.madrid` · workflows clave: `iMoTKZWxYLymGuHF` (reserva/disponibilidad), `om8iBm8ovENIgaxv` (cambio/cancelación), `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), `5NRXALN9lBVE9fTs` (búsqueda + red anclaje), `aUENlbhCLPhPAVvV` (disponibilidad tool), `QLfRT9AWmV1HLMZs` (chatbot)
- Voz: Flow `conversation_flow_19ca70e19b3f` · Kommo: `simarro.kommo.com` · Retell: `+34 919 93 28 52` · transfer humano `+34 629 12 78 16`

## Histórico de hitos

- 2026-06-02: matching en 3 embudos (multi-pool) · recordatorios de visita anclados a tarea Meeting (mata el falso positivo del matching + habilita recordatorios reales) · matching task → Follow-up
- 2026-06-01: visitas a 30 min + buffer 0/60 (todos los workflows) · bug voz "no reservaba" (nodo silencioso `n_confirmar_tel`) corregido · cambio de cita alineado con reserva (30min + calendario del agente) · WhatsApp `Mirar_disponibilidad`→toolWorkflow · red backend anclaje `idealista_id` · **reserva WhatsApp: validar ANTES de confirmar** (antes confirmaba en Kommo aunque el slot estuviera ocupado; voz PENDIENTE) · ajustes latencia voz · descubierto que el agente productivo es el Flow (no el retell-llm)
- 2026-05-31: Ana voz publicada + disponibilidad con buffer (slots) + recheck + E2E · plantillas Meta aprobadas · leads limpios
- 2026-05-28: routing por agente + WA confirmación voz + bugs Retell
- 2026-05-04: chatbot lentitud arreglada · salesbots recordatorios
