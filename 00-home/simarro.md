---
title: simarro
date: 2026-06-10
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria (Las Rozas, Madrid). Chatbot WhatsApp + agente de voz Retell "Ana" + Kommo CRM + catálogo Idealista (Supabase) + scraping. Contacto: Ramón.

> Source of truth técnico: `/Users/manueldelmonte/simarro/CLAUDE.md`. Snapshot detallado: [[estado-actual]]. Routing/buffer citas: [[routing-citas-por-agente]].

## Estado (2026-06-11)

- **Outbound reactivación (Opción C) IMPLEMENTADO 2026-06-11** — llamadas IA a leads fríos cada ≥10 días (L-V 10:30, finde → lunes), cap 3 intentos, gate = CF consentimiento `1376604` marcado a mano. Agente Retell `agent_042b9fbc990838ae4117315440` + flow `conversation_flow_29839e6fd152`; lanzador `2LqwDgLecHwjgIQl` (INACTIVO hasta test real) + handler `flhsvOskRZiHrcKu` (activo). **Falta**: aplicar `sql/017` (sin exec_sql — necesita psql en contenedor) + test de llamada real + marcar consentimientos. Lista Robinson documentada, no se usa aún. Detalle: [[llamadas-outbound-reactivacion]].
- **Audit 2026-06-10**: BD sana — 12 viviendas activas (8 con `agente:`, 4 sin → fallback Ramón), tabla `agents` completa (8 agentes, emails reales), `match_pairs` verificado con los 2 leads activos (case-insensitive OK). **Fix aplicado**: la anulación de citas (`om8iBm8ovENIgaxv`) no miraba los calendarios de Elisa, Javier, Mónica ni Ramón Simarro — añadidos los 4 pares Buscar/Eliminar (backup `om8iBm8ovENIgaxv-cambio-pre-calendarios-faltantes-20260610.json`).
- **Notificaciones P1-P5 HECHAS** (2026-06-02→09): confirmación cliente formulario, confirmación visita, aviso interno visita a Ramón+agente (emails reales en BD), seguimiento post-visita 48h (salesbot 87873 + etapa Post-visita), alertas inactividad (`Xh2miozB7LvwQKia`, diario 08:30).
- **Recordatorios** solo reaccionan a tareas Meeting (type 2) creadas por la reserva; matching usa Follow-up (1). ~~Especialista Asignado~~ desactivado 2026-06-08 (el agente va por `agente:` de Idealista).
- **Subsistema contratos Docuseal** activo: 4 workflows `contratos-*` (generar borrador, enviar firma, firmado, spawn). OJO: `contratos-enviar-firma` lleva un `TODO producción: cambiar a la cuenta real` en Build Recipients.
- **SMTP RESUELTO** (2026-06-02): `SMTP LEADS Simarro` (leads/visitas) + `SMTP Simarro` (contratos), ambas funcionales. Emails HTML rediseñados Gmail-safe.

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
6. **Plantilla `Día de visita`**: verificar que el CF `1330871` se inyecta con fecha legible en la plantilla WA (test real).
7. **Reconcile `Build rows`**: probar con lead real con tipos/extras rellenos — los diccionarios usan etiquetas con acentos (`'Ático'`, `'Jardín'`); si Kommo envía otro encoding, la preferencia se descarta en silencio (no rompe matching, pero la ignora).

## Otros pendientes

- **Outbound go-live** (orden): aplicar `sql/017` (psql en contenedor — falta vía de acceso o autorización SSH) → test llamada real al móvil de Manu → marcar consentimiento `1376604` en leads autorizados por Ramón → activar `2LqwDgLecHwjgIQl`.
- **4 viviendas activas sin `agente:`** (Ramón debe añadirlo en Idealista): `111460118` (Chalet La Chopera), `111607600` (Pareado Los Satélites), `111668433` (Piso Coto Blanco), `111708032` (Local Primo de Rivera). Mientras, fallback = calendario general `consultingsimarroproperties@gmail.com`: la visita se agenda ahí, el aviso interno va solo a `rss@` (sin agente en copia) y el buffer de 60 min se calcula contra esa agenda. La cita no se pierde, pero sin routing por agente. Se autocorrige con el sync de las 8:00 al añadir `agente: <nombre>` en la descripción de Idealista.
- Verificar que el bot `88575` (formularios no-contacto) tiene plantilla WA aprobada (`Solicitud_recibida` 72645) — solo comprobable en Kommo UI.
- Borrar embudo vacío `13862727` ("Compradores en búsqueda") en Kommo UI.
- Rotar key Supabase (cred `Wm7JL1tsxiWyElqt` usa la demo de self-hosted) a producción.
- `contratos-enviar-firma`: cambiar cuenta Documenso de prueba a la real (TODO en Build Recipients).
- Meter leads al pool "Buscando vivienda" desde chatbot/voz tras opt-in (hoy lo mueve el agente a mano en Kommo).
- Crear salesbot para plantilla `72645` Solicitud_recibida (resto de formTypes del formulario web; relacionado con la verificación del bot `88575` de arriba).
- Latencia voz opcional: quitar embedding de `Buscar_viviendas` + `begin_message_delay_ms` 1000→400.
- Consolidar creds (opcional, no urgente): 2 creds `kommoLongLivedApi` con el mismo token → una; 2 SMTP → reasignar los 7 nodos de contratos a `SMTP LEADS Simarro`.
- **LATER**: `meter info rag` cerrado (no se usa, sin documentos); monitor inmuebles tipo StateFox.

✓ Resueltos: SMTP (2026-06-02) · leads test limpiados (2026-05-31) · `desiredResults` Apify ya en 50 · sin restos de `Próxima cita` en Code JS (verificado 2026-06-10) · calendarios faltantes en anulación (2026-06-10).

## Links rápidos

- n8n: `n8nsimarro.agentesia.madrid` · workflows clave: `iMoTKZWxYLymGuHF` (reserva/disponibilidad), `om8iBm8ovENIgaxv` (cambio/cancelación), `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), `5NRXALN9lBVE9fTs` (búsqueda + red anclaje), `aUENlbhCLPhPAVvV` (disponibilidad tool), `QLfRT9AWmV1HLMZs` (chatbot)
- Voz: Flow `conversation_flow_19ca70e19b3f` · Kommo: `simarro.kommo.com` · Retell: `+34 919 93 28 52` · transfer humano `+34 629 12 78 16`

## Histórico de hitos

- 2026-06-10: audit completo (BD + 34 workflows) · fix anulación: añadidos calendarios Elisa/Javier/Mónica/Ramón Simarro (antes una visita en esos calendarios no se podía anular) · cobertura `agente:` 8/12 · hub actualizado
- 2026-06-08/09: P3 aviso interno visita (emails reales agentes, sql/015-016) · P4 post-visita 48h · P5 alertas inactividad · Especialista Asignado desactivado
- 2026-06-02: matching en 3 embudos (multi-pool) · recordatorios de visita anclados a tarea Meeting (mata el falso positivo del matching + habilita recordatorios reales) · matching task → Follow-up · emails HTML rediseñados Gmail-safe · SMTP verificado
- 2026-06-01: visitas a 30 min + buffer 0/60 (todos los workflows) · bug voz "no reservaba" (nodo silencioso `n_confirmar_tel`) corregido · cambio de cita alineado con reserva (30min + calendario del agente) · WhatsApp `Mirar_disponibilidad`→toolWorkflow · red backend anclaje `idealista_id` · **reserva WhatsApp: validar ANTES de confirmar** (antes confirmaba en Kommo aunque el slot estuviera ocupado; voz PENDIENTE) · ajustes latencia voz · descubierto que el agente productivo es el Flow (no el retell-llm)
- 2026-05-31: Ana voz publicada + disponibilidad con buffer (slots) + recheck + E2E · plantillas Meta aprobadas · leads limpios
- 2026-05-28: routing por agente + WA confirmación voz + bugs Retell
- 2026-05-04: chatbot lentitud arreglada · salesbots recordatorios
