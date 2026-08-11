---
title: simarro
date: 2026-06-10
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria (Las Rozas, Madrid). Chatbot WhatsApp + agente de voz Retell "Ana" + Kommo CRM + catálogo Idealista (Supabase) + scraping. Contacto: Ramón.

> Source of truth técnico: `/Users/manueldelmonte/simarro/CLAUDE.md`. Snapshot detallado: [[estado-actual]]. Routing/buffer citas: [[routing-citas-por-agente]].

## Estado (2026-08-12)

**Auditoría a fondo de voz+n8n (11/12-ago), 8 puntos de queja del cliente atacados uno a uno.** Resueltos y verificados con datos/llamadas reales: catálogo Idealista (roto ~4h por cambio de plataforma, ver Incidentes), tarea de visita en Kommo (nunca se había creado, ni voz ni WA, desde siempre), reorden recheck-antes-de-confirmar en voz (bloqueante de junio, YA resuelto), disponibilidad de voz con fecha (mismatch de esquema Retell), latencia de cancelación (7,9-9s → 2s, ver Incidentes), derivación a humano sin avisar a nadie, `match_count` de búsqueda ignorado en n8n, boosted_keywords de topónimos, y reintento de las 7 tools sin preguntar al cliente. Detalle técnico completo en [[simarro-auditoria-voz-2026-08]]. Cron zombie de `Matching semanal` y `Reconcile lead_preferences` reactivado (deactivate/activate); `Matching semanal` además tenía un bug real (cortaba con error falso cuando no había coincidencias nuevas, el caso normal).

## Estado (2026-06-11, histórico)

- **Outbound reactivación (Opción C) VALIDADO E2E 2026-06-11** — llamadas IA a leads fríos cada ≥10 días (L-V 10:30, finde → lunes), cap 3 intentos, gate = CF consentimiento `1376604` marcado a mano. Agente Retell `agent_042b9fbc990838ae4117315440` (voz `eleven_multilingual_v2` temp 1.1) + flow `conversation_flow_29839e6fd152` **v2 (17 nodos, tool Buscar_viviendas + reglas de naturalidad)**; lanzador `2LqwDgLecHwjgIQl` (INACTIVO, **integra `match_pairs`**: pivote vivienda-original→motivo→alternativa del matching) + handler `flhsvOskRZiHrcKu` (activo). `sql/017` aplicada. 4 llamadas test al móvil de Manu; la 4ª completó el camino entero: motivo descarte → alternativa → búsqueda en cartera → visita agendada con `idealista_id` correcto. **Falta**: marcar consentimientos (Ramón) + activar lanzador. Lista Robinson documentada, no se usa aún. Doc presentación: `simarro/docs/entrega-fase2-simarro.html`. Detalle: [[llamadas-outbound-reactivacion]].
- **Audit 2026-06-10**: BD sana — 12 viviendas activas (8 con `agente:`, 4 sin → fallback Ramón), tabla `agents` completa (8 agentes, emails reales), `match_pairs` verificado con los 2 leads activos (case-insensitive OK). **Fix aplicado**: la anulación de citas (`om8iBm8ovENIgaxv`) no miraba los calendarios de Elisa, Javier, Mónica ni Ramón Simarro — añadidos los 4 pares Buscar/Eliminar (backup `om8iBm8ovENIgaxv-cambio-pre-calendarios-faltantes-20260610.json`).
- **Notificaciones P1-P5 HECHAS** (2026-06-02→09): confirmación cliente formulario, confirmación visita, aviso interno visita a Ramón+agente (emails reales en BD), seguimiento post-visita 48h (salesbot 87873 + etapa Post-visita), alertas inactividad (`Xh2miozB7LvwQKia`, diario 08:30).
- **Recordatorios** solo reaccionan a tareas Meeting (type 2) creadas por la reserva; matching usa Follow-up (1). ~~Especialista Asignado~~ desactivado 2026-06-08 (el agente va por `agente:` de Idealista).
- **Subsistema contratos Docuseal** activo: 4 workflows `contratos-*` (generar borrador, enviar firma, firmado, spawn). OJO: `contratos-enviar-firma` lleva un `TODO producción: cambiar a la cuenta real` en Build Recipients.
- **SMTP RESUELTO** (2026-06-02): `SMTP LEADS Simarro` (leads/visitas) + `SMTP Simarro` (contratos), ambas funcionales. Emails HTML rediseñados Gmail-safe.

- **Voz Ana — el agente PRODUCTIVO es el Conversation Flow** `agent_0df7f123e7e3c24d99c9152358` (`conversation_flow_19ca70e19b3f`, gpt-4.1 cascading). ⚠️ El `agent_7b02aa...` (retell-llm) está **EN DESUSO**. Llama a `+34 910 05 46 75` (verificado en Retell 12-ago, nickname "Simarro Netelip" — el hub tenía `919 93 28 52` desactualizado). Busca, mira disponibilidad, reserva (pide nombre + consentimiento), cancela/cambia, deriva.
- **Visitas de 30 min** (solicitud Simarro 2026-06-01; antes 1h). Buffer mismo agente: **0 min misma vivienda, 60 min (1h margen) distinta**. Slots :00 y :30 → **10:00–13:30 y 17:00–19:30**. SSOT: `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), compartida voz+WhatsApp.
- **Chatbot WhatsApp** activo (`QLfRT9AWmV1HLMZs`): `Mirar_disponibilidad` convertido a `toolWorkflow` (el HTTP tool no exponía args al LLM) → sub `Disponibilidad (tool)` (`aUENlbhCLPhPAVvV`). Red backend que ancla el `idealista_id` en el lead cuando la búsqueda da 1 vivienda.
- **Kommo** integrado (pipeline `13546071` + 4 pipelines forms web), salesbots recordatorio.
- **Catálogo Idealista** en Supabase (`properties`), sync diario vía Apify. Ramón YA empezó a poner `agente:` (el dúplex de Pozuelo resuelve a Carlos).
- **Matching multi-pool (2026-06-02)** — el pool ya son **3 etapas en 3 embudos** (Ventas `106971083` + Capacidad de compra `105358051` + Personal Shopper `105358071`), editado en `Reconcile lead_preferences`. Verificado E2E (llegó el WhatsApp del piso de Pozuelo).
- **Recordatorios de visita (2026-06-02)** — anclados a una **tarea Meeting (type 2)** que la reserva crea con `complete_till`=hora de visita; el matching pasó su tarea a Follow-up (1) y Recordatorios filtra solo type 2 → mata el recordatorio falso del matching y habilita los recordatorios reales (antes no existían). Ver [[recordatorios-visita-por-task-type]].

## ✅ Resuelto 11/12-ago (eran bloqueantes)

- **Cron zombie de 3 workflows** (`Matching semanal`, `Reconcile lead_preferences`, y de paso `Leads cambio de fecha o anulacion` al tocarlo) — el trigger quedaba registrado sin recargar de verdad en el motor; fix = deactivate/activate. `Llamadas_outbound (reactivacion)` sin confirmar todavía (espera consentimientos de Ramón, no urgía).
- **Reorden recheck en VOZ** (bloqueante desde 2026-06-01, "no tocar a ciegas") — la rama de voz confirmaba antes de verificar disponibilidad real; consolidado a 1 solo camino con recheck real antes de responder, igual que ya tenía WhatsApp. Validado con llamada de prueba real.

Ver [[simarro-auditoria-voz-2026-08]] para el detalle completo (8 agentes de auditoría, 10 workflows n8n tocados, 4 versiones de Retell).

## Pendiente — tests E2E reales

1. ✅ **WhatsApp reserva** — validado 11-ago: evento real + tarea Kommo + email, con recheck real antes de confirmar.
2. **Cambio de cita**: nuevo evento en calendario del agente, 30 min, borra el viejo — sin re-test tras el rediseño de latencia de cancelación (comparte el camino rápido, no probado end-to-end el caso "cambio", solo "cancelar puro").
3. **Buffer**: misma casa pegadas (10:00–10:30 / 10:30–11:00); casa distinta → 60 min margen (no antes de 11:30).
4. **Voz — latencia**: bug real confirmado y corregido 12-ago (cancelación 7,9-9s→2s por rediseño; ver Incidentes). Sigue sin medir: latencia de `Buscar_viviendas`/`Mirar_disponibilidad` en llamada real (0 ejecuciones capturadas), y si conviene bajar de gpt-4.1 a una variante mini (dejado igual a propósito, decisión pendiente).
5. **Subir tier OpenAI** (chatbot WA gpt-4o, hoy 30k TPM → rate limits).
6. **Plantilla `Día de visita`**: verificar que el CF `1330871` se inyecta con fecha legible en la plantilla WA (test real).
7. **Reconcile `Build rows`**: probar con lead real con tipos/extras rellenos — los diccionarios usan etiquetas con acentos (`'Ático'`, `'Jardín'`); si Kommo envía otro encoding, la preferencia se descarta en silencio (no rompe matching, pero la ignora).
8. **Pronunciación TTS de topónimos** (12-ago): reforzado el reconocimiento de entrada (`boosted_keywords`), no la pronunciación de salida — sin confirmar el formato que acepta esta plataforma para eso, no tocado por precaución.

## Otros pendientes

- **Limpieza leads de test 12-ago (Kommo UI)**: `34790206` ("TEST BORRAR - validacion tarea") y su contacto `38931342` — usado para validar el fix de latencia de cancelación. Y avisar a `rss@`/`pss@simarroproperties.com`: recibieron 2-3 emails reales de "visita" por las pruebas de reserva de esta sesión (nombre "Test Latencia Claude").
- **Outbound go-live** (solo queda): marcar consentimiento `1376604` en leads autorizados por Ramón → activar `2LqwDgLecHwjgIQl`.
- **Limpieza test outbound 2026-06-11 (Manu, en Kommo UI)**: borrar lead `32662576` + contacto `36417752` (la API no permite delete). El WA de confirmación de ese test le llegó al móvil de Ramón (629127816) — avisarle. Evento Calendar ya borrado, sin tarea Meeting.
- **4 viviendas activas sin `agente:`** (Ramón debe añadirlo en Idealista): `111460118` (Chalet La Chopera), `111607600` (Pareado Los Satélites), `111668433` (Piso Coto Blanco), `111708032` (Local Primo de Rivera). Mientras, fallback = calendario general `consultingsimarroproperties@gmail.com`: la visita se agenda ahí, el aviso interno va solo a `rss@` (sin agente en copia) y el buffer de 60 min se calcula contra esa agenda. La cita no se pierde, pero sin routing por agente. Se autocorrige con el sync de las 8:00 al añadir `agente: <nombre>` en la descripción de Idealista.
- Verificar que el bot `88575` (formularios no-contacto) tiene plantilla WA aprobada (`Solicitud_recibida` 72645) — solo comprobable en Kommo UI.
- Borrar embudo vacío `13862727` ("Compradores en búsqueda") en Kommo UI.
- Rotar key Supabase (cred `Wm7JL1tsxiWyElqt` usa la demo de self-hosted) a producción.
- `contratos-enviar-firma`: cambiar cuenta Documenso de prueba a la real (TODO en Build Recipients).
- **Documenso no sobrevive a los reboots (07-ago)** — su compose no trae `restart:`, así que los dos contenedores nacían con policy `no`. Parcheado en caliente con `docker update --restart unless-stopped`, pero **eso se pierde en el próximo redeploy desde el panel**: hay que añadir `restart: unless-stopped` a los dos servicios del compose en Dokploy. El host no está expuesto a la carrera de la overlay (en su `dokploy-network` solo hay servicios de Swarm). → [[contenedor-que-no-vuelve-tras-reboot-dos-causas-que-se-confunden]]
- Meter leads al pool "Buscando vivienda" desde chatbot/voz tras opt-in (hoy lo mueve el agente a mano en Kommo).
- Crear salesbot para plantilla `72645` Solicitud_recibida (resto de formTypes del formulario web; relacionado con la verificación del bot `88575` de arriba).
- Latencia voz opcional: quitar embedding de `Buscar_viviendas` + `begin_message_delay_ms` 1000→400.
- Consolidar creds (opcional, no urgente): 2 creds `kommoLongLivedApi` con el mismo token → una; 2 SMTP → reasignar los 7 nodos de contratos a `SMTP LEADS Simarro`.
- **Verificación E2E reserva tras recableo (06-25)**: falta corrida real — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email interno. Crash "node hasn't been executed" cerrado; pendiente la corrida. Ver [[n8n-ramas-paralelas-no-garantizan-orden-poner-en-serie]].
- **Outbound — re-test guion**: bug `n_motivo` (callejón sin salida) corregido en vivo (06-25). Pendiente re-test "no, me pareció cara → sigo buscando" + marcar consentimiento `1376604` (Ramón). Lanzador `2LqwDgLecHwjgIQl` activo. Ver [[project-outbound-reactivacion]] · [[conversation-flow-outbound-gotchas]].
- ~~**Simarro/CZ — bug recordatorios por task_type**~~ **CERRADO 2026-07-28**: verificado que Clínica Zen NO lo arrastra — su workflow `PJBMjLLE0vNJjZH8` dispara desde eventos de Google Calendar (`Lead ID:` en la descripción), no desde tareas de Kommo, así que el `task_type` no interviene. Solo aplica a Simarro. Ver [[recordatorios-visita-por-task-type]] · [[clinica-zen]].
- **Preguntar a Ramón**: (1) ¿bot reserva directo o fecha provisional? (2) ¿pipeline Kommo vale o ajustes?
- **Verificar salesbot `88183`**: acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo.
- **Go-live routing por-agente** (datos): Ramón añade `agente:` en Idealista → sync `3zBDpPwBYLZgMink` → E2E con vivienda real. Hoy `properties.agent=NULL`. Voz publicada (v29). Ver [[routing-citas-por-agente]].
- **Limpiar leads ZZ TEST matching (Kommo UI)**: `32287686`/`32288360`/`32293872`/`32295018`/`32302304`/`32314286` + `36016032` + Bad Bunny `32281284`. Pendiente también: chatbot WA que mueva a pool (voz ✅) + mapeo agente→`kommo_user_id` (Ramón) + re-notificar bajada de precio.
- **Limpiar 9 leads test + cred SMTP fantasma**: leads `32260874`/`32260174`/`32260184`/`32260262`/`32260290`/`32260318`/`32260370`/`32257958` + "Ramon Demo". Cred SMTP App Password `simarroproperties@gmail.com` (`oKRmYFhljczyvzV8`) fantasma.
- **IDs TODO en n8n** (LATER): rellenar TASK_TYPE_ID, RESPONSIBLE_USER_ID, SHEET_ID_LEADS_WEB, calendar Ramón, Supabase pending.
- **LATER**: `meter info rag` cerrado (no se usa, sin documentos); monitor inmuebles tipo StateFox.

✓ Resueltos: SMTP (2026-06-02) · leads test limpiados (2026-05-31) · `desiredResults` Apify ya en 50 · sin restos de `Próxima cita` en Code JS (verificado 2026-06-10) · calendarios faltantes en anulación (2026-06-10).

## Links rápidos

- n8n: `n8nsimarro.agentesia.madrid` · workflows clave: `iMoTKZWxYLymGuHF` (reserva/disponibilidad), `om8iBm8ovENIgaxv` (cambio/cancelación), `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`), `5NRXALN9lBVE9fTs` (búsqueda + red anclaje), `aUENlbhCLPhPAVvV` (disponibilidad tool), `QLfRT9AWmV1HLMZs` (chatbot)
- Voz: Flow `conversation_flow_19ca70e19b3f` · Kommo: `simarro.kommo.com` · Retell: `+34 910 05 46 75` · transfer humano `+34 629 12 78 16`

## Histórico de hitos

- 2026-08-11/12: auditoría de los 8 puntos de queja del cliente, con 8 agentes en paralelo + fixes propios verificados con datos/llamadas reales — detalle en [[simarro-auditoria-voz-2026-08]]. Resumen: catálogo Idealista reparado (2 bugs distintos) + watchdog con cooldown, tarea de visita en Kommo (nunca existió, voz+WA), reorden recheck en voz (bloqueante desde junio), disponibilidad de voz (mismatch de esquema Retell), latencia de cancelación (7,9-9s→2s), derivación a humano (webhook mal cableado, sin aviso a nadie), `match_count` (hardcodeado, ignoraba al LLM), reintento de las 7 tools sin preguntar al cliente, boosted_keywords de topónimos, cron zombie de 3 workflows reactivado. Número real de la línea corregido en el hub (`910 05 46 75`, no `919 93 28 52`).
- 2026-06-11: outbound validado E2E (4 llamadas test) · flow v2 (17 nodos: tool búsqueda, pivote con matching, anti-stall, naturalidad sin empatía enlatada) · voz multilingual_v2 · lanzador integra `match_pairs` (alternativa personalizada por lead) · fix `idealista_id` dinámico en n_mirar/n_reservar (antes reservaba siempre contra la vivienda original) · fix phone alucinado en Reservar (regla EXACTAMENTE `{{telefono_lead}}`) · sql/017 aplicada · doc entrega Fase 2 HTML
- 2026-06-10: audit completo (BD + 34 workflows) · fix anulación: añadidos calendarios Elisa/Javier/Mónica/Ramón Simarro (antes una visita en esos calendarios no se podía anular) · cobertura `agente:` 8/12 · hub actualizado
- 2026-06-08/09: P3 aviso interno visita (emails reales agentes, sql/015-016) · P4 post-visita 48h · P5 alertas inactividad · Especialista Asignado desactivado
- 2026-06-02: matching en 3 embudos (multi-pool) · recordatorios de visita anclados a tarea Meeting (mata el falso positivo del matching + habilita recordatorios reales) · matching task → Follow-up · emails HTML rediseñados Gmail-safe · SMTP verificado
- 2026-06-01: visitas a 30 min + buffer 0/60 (todos los workflows) · bug voz "no reservaba" (nodo silencioso `n_confirmar_tel`) corregido · cambio de cita alineado con reserva (30min + calendario del agente) · WhatsApp `Mirar_disponibilidad`→toolWorkflow · red backend anclaje `idealista_id` · **reserva WhatsApp: validar ANTES de confirmar** (antes confirmaba en Kommo aunque el slot estuviera ocupado; voz PENDIENTE) · ajustes latencia voz · descubierto que el agente productivo es el Flow (no el retell-llm)
- 2026-05-31: Ana voz publicada + disponibilidad con buffer (slots) + recheck + E2E · plantillas Meta aprobadas · leads limpios
- 2026-05-28: routing por agente + WA confirmación voz + bugs Retell
- 2026-05-04: chatbot lentitud arreglada · salesbots recordatorios
