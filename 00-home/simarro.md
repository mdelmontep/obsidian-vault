---
title: simarro
date: 2026-06-10
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria (Las Rozas, Madrid). Chatbot WhatsApp + agente de voz Retell "Ana" + Kommo CRM + catálogo Idealista (Supabase) + scraping. Contacto: Ramón.

> Source of truth técnico: `~/Projects/simarro/CLAUDE.md`. Snapshot detallado: [[estado-actual]]. Routing/buffer citas: [[routing-citas-por-agente]].
>
> La web (solo landing/marketing) vive aparte en `~/Projects/simarro_web/` — no mezclar con este proyecto de automatización.

## Estado (2026-08-17)

**Seguimiento a los fixes del 13-ago, arrancado por una llamada real del cliente con 3 quejas — las 3 confirmadas y corregidas.** Detalle técnico completo: [[simarro-voz-fixes-claro-clusters-17-ago]].

- **Guard de teléfono endurecido** (`Edit Fields3`, `iMoTKZWxYLymGuHF`): el guard de mayo solo descartaba el placeholder viejo — hoy el modelo confundió teléfono con nombre y llegó basura hasta Kommo. Ahora valida que parezca un teléfono real, no solo que no sea el patrón conocido. Confirmado E2E con lead de prueba real.
- **"Claro." + transición en el mismo turno — causa raíz oficial encontrada**: los edges de Retell solo evalúan tras un turno NUEVO del usuario, nunca justo tras la propia frase del agente (confirmado por soporte oficial de Retell, ver [[Stack/retell/conversation-flow-outbound-gotchas]]). Fix en los 2 flujos de voz (entrada v24, salida v1) — confirmado con llamada real sin ninguna pausa.
- **Ruido de fondo**: `denoising_mode` ausente en el agente de salida (sí lo tenía el de entrada) — igualado.
- **Clústeres de proximidad geográfica (feature nueva)**: primera versión con 2 clústeres (núcleo/sierra), luego ampliada el mismo día a **toda la Comunidad de Madrid** (petición del cliente vía Manu: "que funcione en toda España" → acotado a Madrid, resto de España solo coincidencia exacta) — 179 municipios reconocidos, 12 clústeres reales basados en las 9 comarcas oficiales (Wikipedia, verificado 179/179), partiendo la comarca "Área Metropolitana" en 4 subzonas (mezclaba puntas opuestas de Madrid bajo una sola etiqueta). De rebote, encontrado y corregido un bug preexistente que descartaba SIEMPRE el mensaje con la sugerencia antes de llegar a la llamada (`Format For Voice`, ver [[Stack/n8n]]) — y una 2ª vuelta del mismo bug al añadir el caso "fuera de zona" (el primer fix condicionaba el mensaje a `zones.length`, que ese caso nuevo no tiene). Corregida también una clasificación errónea: Villaviciosa de Odón estaba en "sierra", pertenece oficialmente al área metropolitana junto a Boadilla. Verificado con 9 casos reales contra el catálogo real (incluye Alcorcón, Alcalá de Henares: reconocidos como Madrid real, "fuera de zona" honesto por falta de cartera). Detalle: [[simarro-voz-fixes-claro-clusters-17-ago]].
- **Zona rechazada no se guarda como interés**: efecto colateral de la función nueva — si Ana propone una zona y el cliente la rechaza, ya no se captura como si fuera lo que pide. Sin validar aún con caso real.
- **Precio antes/después visual (petición Dani)**: investigado, no implementado. La tabla `properties_price_history` existe en Supabase pero `Sync_catalogo_idealista` nunca escribe en ella; el badge "rebajado" en `simarro_web` es decorativo (sin comparación real). Implementarlo toca schema de BD en producción + el repo `simarro_web` (Astro, GitHub aparte) — **aplazado explícitamente por el usuario**, no construir sin que lo pida de nuevo.

**Pendiente**: confirmar regla de zona rechazada en llamada real. Corregido en este hub: el lanzador outbound (`2LqwDgLecHwjgIQl`) está ACTIVO (verificado hoy), no inactivo como decía la entrada de junio — el bloqueante real sigue siendo que 0 leads tienen el consentimiento marcado.

## Estado (2026-08-13)

**Petición del cliente (Dani, 11-ago) — 8 puntos pendientes de verificar/responder, borrador de respuesta entregado en sesión (sin enviar todavía)**. De los que se pudieron verificar hoy con datos reales:
- **Recordatorios 24h**: mecanismo sano (`Recordatorios`/`Oa1lSQuDgEZvZCNS`) — confirmado con la rama de 4h disparando 2 veces con envío real por WhatsApp; misma lógica/código para 24h, sin bug estructural.
- **Llamadas outbound con vivienda actualizada/alternativa**: `Llamadas_outbound (reactivacion)` + `Retell_outbound_eventos` SÍ registran/actualizan Kommo+Supabase al llamar — pero 0 llamadas reales han salido porque ningún lead tiene el consentimiento (CF `1376604`) marcado. Sigue siendo el pendiente de siempre: Ramón tiene que marcarlo.

**Gap real encontrado y corregido: WhatsApp nunca guardaba las preferencias de búsqueda (zona/precio/habitaciones) del cliente, voz solo 3 de 9 campos y con gate de status.** Detalle: [[simarro-fix-preferencias-busqueda-y-bugs-dedup-whatsapp-13-ago]]. Resumen:
- `Reconcile lead_preferences`: pool ampliado a 4 fases (+ "Lead Caliente" `105137095`) — antes un lead nuevo detectado por voz nunca entraba en `lead_preferences` hasta que alguien lo movía a mano.
- `Buscar_viviendas_catalogo`: nuevo tramo que persiste zona/precio/habitaciones desde cada búsqueda de WhatsApp (voz no manda `Lead_id`, no le afecta). 2 regresiones propias en el camino (ambigüedad de nodo terminal en `Execute Workflow`, luego un `return []` que cortaba el flujo) — revertidas y corregidas antes de quedar en producción; **0 impacto real** (verificado en `executions`, solo mis pruebas en la ventana rota).
- **Bug real PRE-EXISTENTE encontrado de rebote**: el fix de deduplicado de mensajes del 12-ago (`Chatbot Simarro`) llevaba desde entonces sin poder procesar NINGÚN mensaje real — 3 nodos (`Redis - Marcar mensaje`, `Edit Fields`, `If2`) leían `$json.body[...]` cuando ya no existía tras el Redis GET de dedup. Nunca se había probado con un mensaje real hasta hoy. Corregido y confirmado end-to-end (el bot respondió correctamente a una búsqueda real). Ver [[n8n-json-narrowed-rompe-nodos-lejanos-sin-error]].
- Slack SÍ avisó del primer fallo (excepción real) pero no del segundo (fallo silencioso, sin excepción) — no es un bug del aviso, es el límite de lo que un error-workflow puede detectar.

✅ **Confirmado el mismo 13-ago**: PATCH de preferencias validado con mensaje real (Guadarrama, 320.000€, 2 habitaciones) — los 3 campos quedaron bien en Kommo tras el fix del campo "Habitaciones" (`select`, no numérico — ver [[kommo]]).

**Barrido cross-cliente cerrado (13-ago)**: el mismo patrón de dedup roto NO se repite en Laserys Las Rozas ni Clínica Zen (mismo nodo reductor, pero referencian bien el nodo webhook) ni en Elphis/EcoBox (arquitectura Chatwoot, sin ese tipo de nodo). AGH Ibérica no usa n8n. Era específico de Simarro. Detalle en [[simarro-fix-preferencias-busqueda-y-bugs-dedup-whatsapp-13-ago]].

## Estado (2026-08-12, tarde — voz v23)

**Conversation Flow v23 publicado** tras auditar una llamada real (contacto "Manuel del Monte", `call_140936c164a6284a21def1a09ca`) y validar el fix con una segunda llamada de prueba (`call_bdf8f0951546391a72b73669f93`). 3 fixes en `conversation_flow_19ca70e19b3f`:
- `n_proponer_hora`: prohibición local de decir "un agente te contactará"/"queda apuntada" antes de ejecutar `Reservar` — el LLM lo decía tras proponer la hora, ANTES de pedir nombre/consentimiento. Confirmado corregido en la llamada de validación.
- `n_consentimiento`: ante audio ininteligible ya no repite la frase idéntica, dice "perdona, no te he oído bien" primero. Sin validar aún (la llamada de prueba no disparó esa rama).
- `global_prompt`: regla anti-eco (turno de usuario = repetición literal de lo que Ana acaba de decir → no tratarlo como respuesta real, no decir "¿sigues ahí?"). El "eco" original resultó ser la propia llamada de prueba hecha en altavoz, no un defecto de la línea Netelip — ver [[probar-agente-voz-en-altavoz-genera-eco-que-parece-bug-de-flow]]. Regla se deja igual como defensa en profundidad (clientes reales también llaman en manos libres).

**Teléfono confirmado ya blindado**: el `Reservar` de la llamada de validación mandó `"phone":"+34{{from_number}}"` literal (el LLM copia el placeholder si la instrucción del nodo lo menciona entre paréntesis) — pero `Edit Fields3` en `iMoTKZWxYLymGuHF` ya lo detecta y usa `call.from_number` real. Contacto nuevo (`38943714`) quedó con teléfono correcto. Ver [[retell-from_number-no-auto-sustituye-en-tool-args]].

**Pendiente nuevo**: `Buscar_viviendas` (`5NRXALN9lBVE9fTs`) omite el número de portal en el campo `message` (lo que Ana lee) aunque `direccion` sí lo trae completo desde el primer resultado — inconsistencia menor, sin decisión tomada. Backup pre-fix en `knowledge/projects/agentesia/n8n-backups/simarro/retell-flow-v22-published-pre-fix-audio-eco-nombre-consentimiento-20260812.json`.

**Limpieza pendiente en Kommo**: leads/contactos de la llamada de validación de hoy (`34802708` / `38943714`, "Manuel del Monte") además de los ya conocidos abajo.

**Chatbot WhatsApp (`QLfRT9AWmV1HLMZs`) — 2 fixes más, tras auditar una conversación real** (mismo lead `34802708`):
- Bug que parecía "el bot resetea el contexto" a mitad de conversación: en realidad Kommo/WABA reenvió el mismo `message.id` ~70s después y el workflow no dedupeaba — solo tenía Redis para agrupar mensajes fragmentados por `lead_id`, nada para descartar un evento ya procesado. Fix: 4 nodos nuevos tras `Recibir mensaje` (`Redis - Check duplicado` → `If - Es duplicado` → `NoOp` o `Redis - Marcar mensaje`, TTL 1h). Ver [[webhook-reenviado-sin-dedup-parece-reset-de-contexto-del-bot]].
- El `AI Agent` dijo "en esa zona no operamos" (pregunta por Galicia) sin haber llamado a `Buscar_viviendas`, violando su propia regla escrita — mismo patrón que el bug de voz de arriba (`n_proponer_hora`), mismo día, arquitectura de agente distinta. Reforzado con "PROHIBIDO ABSOLUTO... sin haber invocado la tool en este turno". Nota aparte: aunque hubiera buscado, el filtro de zona no cubre Galicia (no es del diccionario de Madrid) y por defecto excluye "Local" — el único activo real allí (`111708032`, A Coruña) es un local, no residencial; no se tocó esa parte, valor de negocio marginal. Ver [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]] (complemento 12-ago).
- Backups en `n8n-backups/simarro/n8n-QLfRT9AWmV1HLMZs-chatbot-simarro-pre-dedup-20260812.json` y `-post-dedup-pre-prompt-fix-20260812.json`.
- Nota aparte: ejecución `8376` de este mismo workflow tuvo un error real hoy 12:07:57 (disparó el Error Workflow, ejec. `8377`) — no investigado en esta sesión, puede solaparse con el trabajo de dedup de arriba.

**Watchdog de catálogo — alerta falsa cada tarde, corregida**: `Watchdog_catalogo_idealista` (creado anoche con cooldown, ver hito 11/12-ago) llevaba umbral 8h contra una cadencia de sync diaria real (24h) → avisaba en `#01-incidencias` toda tarde sin nada roto. Verificado con el dato real: `last_seen_at` coincidía al segundo con la hora del cron (06:25 Madrid), el sync SÍ corre a tiempo. Subido a 26h en el nodo `Evaluar Frescura`, verificado por relectura independiente tras el PUT (posiciones intactas, resto de nodos sin tocar). 3ª recurrencia del mismo patrón — ver [[watchdog-umbral-debe-tolerar-un-tick-perdido]]. **Pendiente sin confirmar**: `EXECUTIONS_DATA_MAX_AGE` del n8n de Simarro probablemente mal puesto en horas — mismo síntoma que Clínica Zen (71 ejecuciones vía API, ninguna anterior a ~6,5h); no verificado por SSH. Ver [[n8n-executions-data-max-age-va-en-horas-no-en-dias]].

## Estado (2026-08-12)

**Auditoría a fondo de voz+n8n (11/12-ago), 8 puntos de queja del cliente atacados uno a uno.** Resueltos y verificados con datos/llamadas reales: catálogo Idealista (roto ~4h por cambio de plataforma, ver Incidentes), tarea de visita en Kommo (nunca se había creado, ni voz ni WA, desde siempre), reorden recheck-antes-de-confirmar en voz (bloqueante de junio, YA resuelto), disponibilidad de voz con fecha (mismatch de esquema Retell), latencia de cancelación (7,9-9s → 2s, ver Incidentes), derivación a humano sin avisar a nadie, `match_count` de búsqueda ignorado en n8n, boosted_keywords de topónimos, y reintento de las 7 tools sin preguntar al cliente. Detalle técnico completo en [[simarro-auditoria-voz-2026-08]]. Cron zombie de `Matching semanal` y `Reconcile lead_preferences` reactivado (deactivate/activate); `Matching semanal` además tenía un bug real (cortaba con error falso cuando no había coincidencias nuevas, el caso normal).

**Reorganización de carpetas (12-ago)**: la carpeta de automatización (`~/simarro`, fuera del patrón `~/Projects/`) había desaparecido de disco sin dejar rastro; recreada en `~/Projects/simarro/` con `CLAUDE.md` reconstruido desde este hub + memoria de sesión superviviente. Duplicado vacío `simarro-properties-web` (repo personal `mdelmontep`) borrado localmente — **pendiente decidir si se borra también en GitHub**. Skill `n8n-surgical-edit` actualizada al nuevo nombre de carpeta. Ver [[borrar-la-carpeta-de-un-proyecto-no-borra-su-memoria-de-claude-code]].

**Pendiente en agency-portal**: el tiempo trabajado en Simarro se atribuye por nombre de carpeta (`project_key`), no hay cliente vinculado todavía → vincular `simarro` y `simarro-web` al cliente "Simarro" en `/agency/time`, y decidir si se reatribuyen a mano las sesiones del 11/12-ago que cayeron en el cubo genérico. Ver [[agency-portal-agrupa-tiempo-por-nombre-de-carpeta-no-por-cliente]].

**2 bugs más, encontrados en llamadas/pruebas reales del propio Manuel tras la auditoría (12-ago)**:
- **Teléfono del contacto de WhatsApp se corrompía en cada reserva** — el flujo pisaba el teléfono real (que Kommo ya conocía por el canal) con lo que el LLM creía extraer del texto ("+34" sin dígitos, en un caso real). Parecía un error de facturación de Meta al enviar la confirmación ("phone number is malformed") pero no lo era — descartado con capturas reales: método de pago y plantilla estaban bien. Corregido para priorizar siempre el dato real del contacto. Ver Incidentes.
- **"Claro." y silencio en voz, persistía tras el primer fix** — reforzado con una tercera vía explícita para cuando la transcripción es muy confusa. Ver Incidentes.

## Estado (2026-06-11, histórico)

- **Outbound reactivación (Opción C) VALIDADO E2E 2026-06-11** — llamadas IA a leads fríos cada ≥10 días (L-V 10:30, finde → lunes), cap 3 intentos, gate = CF consentimiento `1376604` marcado a mano. Agente Retell `agent_042b9fbc990838ae4117315440` (voz `eleven_multilingual_v2` temp 1.1) + flow `conversation_flow_29839e6fd152` **v2 (17 nodos, tool Buscar_viviendas + reglas de naturalidad)**; lanzador `2LqwDgLecHwjgIQl` (**ACTIVO** — corregido 17-ago, esta entrada decía INACTIVO desde junio; **integra `match_pairs`**: pivote vivienda-original→motivo→alternativa del matching) + handler `flhsvOskRZiHrcKu` (activo). `sql/017` aplicada. 4 llamadas test al móvil de Manu; la 4ª completó el camino entero: motivo descarte → alternativa → búsqueda en cartera → visita agendada con `idealista_id` correcto. **Falta**: marcar consentimientos (Ramón) + activar lanzador. Lista Robinson documentada, no se usa aún. Doc presentación: `simarro/docs/entrega-fase2-simarro.html`. Detalle: [[llamadas-outbound-reactivacion]].
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

- **Limpieza leads de test 17-ago (Kommo UI)**: `34951382` (TEST E2E Phone Guard), `34951644`/`34951946` (TEST E2E/E2E Outbound) — usados para validar el guard de teléfono y los fixes de voz de hoy.
- **Limpieza leads de test 12-ago (Kommo UI)**: `34790206` ("TEST BORRAR - validacion tarea") y su contacto `38931342` — usado para validar el fix de latencia de cancelación. Y avisar a `rss@`/`pss@simarroproperties.com`: recibieron 2-3 emails reales de "visita" por las pruebas de reserva de esta sesión (nombre "Test Latencia Claude").
- **Contacto `38942304` ("Manuel del Monte") con teléfono roto (`+34` sin dígitos)** — corregirlo a mano con el número real y reenviar el mensaje de confirmación fallido de la conversación A236 para confirmar que el fix del teléfono ya lo resuelve de verdad (sin probar en real todavía).
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
