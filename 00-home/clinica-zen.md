---
title: clinica-zen
date: 2026-07-29
updated: 2026-09-03
tags: [cliente, clinica-zen]
---

# Clínica Zen

Clínica dental + estética facial en Las Rozas. Chatbot WhatsApp (Kommo) + agente de voz Retell + recordatorios + emails. Contactos: Gonzalo (legacy), Dani.

## Estado 3-sep-2026: v70 en producción, huecos y guard en código

Tres llamadas reales de prueba destaparon que la **v67 calculaba la disponibilidad en el LLM** desde los eventos crudos del calendario (decía «miércoles completo» con la mañana libre, no dejaba elegir otra hora) y que aceptaba horas fuera de la lista (13:00 ocupada → reservada encima). Hecho en producción (LLM `llm_271c…`, **v70 publicada**, número en `latest_published`):

- `Mirar_disponibilidad` recibe `dia`/`franja`/`hora` y **n8n devuelve los huecos ya calculados** (`Code in JavaScript2` de `RN0wl8RaRmwLpnfQ`: L-V 10-14/15:30-20:30, sáb 10-14, festivos, margen 48 h, ventana 21 días, solapes; salida `opcion1/2_*`, `huecos_disponibles`, `dia_coincide`). El prompt solo elige.
- **Guard en `Reservar_crm`** (4 nodos antes de `Get list of contacts1`): relee el calendario ±1 h y si el hueco está ocupado responde `error: hueco_ocupado` sin tocar Kommo; el prompt (§9b) vuelve a mirar disponibilidad. Probado (exec 13067). La lista cerrada protege el ofrecer; el guard, el reservar → [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].
- Teléfono: ofrece el número del llamante con `{{user_number}}` (**no** `{{from_number}}`, que llegaba vacía) y solo pide otro si dice que no → [[retell-from_number-no-auto-sustituye-en-tool-args]].
- `Append row in sheet1` (log en Sheets, último nodo) con retry 3×5 s tras el 503 del 3-sep; no afecta al paciente.
- Pruebas limpiadas: 4 leads a status 143 renombrados `[TEST agentesia 3-sep] …`, 5 eventos borrados. **Quedan los contactos `39968918` y `41819782`** (la API no borra contactos): quitar en la UI de Kommo.
- Backups pre-cambio (LLM v67, workflow) en el scratchpad de la sesión; el de la v54 sigue en `knowledge/projects/agentesia/n8n-backups/clinica-zen/`.

**Agente Flow** `agent_d3c52ef4ee0f2eeb6904212c05` («Clínica Zen (Flow)»): borrador con intake de una pregunta por turno, tono («vale/perfecto» + «¿me puedes decir tu nombre?»), audio (`interruption_sensitivity 0.5`, `denoising noise-cancellation`, `begin_message_delay 1000`) y sin «Európolis». **Sin número asignado**: 2 h corrigiéndolo mientras la llamada real entraba en el single-prompt — antes de editar, `list-phone-numbers` → `agent_id` ([[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]]). Decidir si sustituye al single-prompt; si sí, portarle huecos + guard + caller-ID.

**Visto y no tocado**: cada reserva crea DOS eventos (30 min «Odontología - Valoración - X» y 60 min «Valoración - General - X», probablemente `Especilista Asignado`) · las pruebas de playground fallan en `Get a call3` de `Leads entrantes` (no hay call real) y no mandan el email · `transfer_call` no funciona desde test web.

## El número servía la v54 (20-ago) — condensado

`+34919934582` fijado a `agent_version: 54` con la v67 publicada: 28 llamadas reales con el prompt de mayo, y de ahí el «fix del nombre inventado no funciona» que este hub arrastró del 3 al 20-ago. Arreglado a `latest_published` (inbound y outbound). Detalle en [[clinica-zen-historico]] · [[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]].

## Estado (verificado 2026-07-28)

**Infra**: servidor `185.47.13.168` · n8n `n8nclinicazen.agentesia.madrid` · Kommo `citasclinicazenes.kommo.com` (account 36308863, pipeline 13495347) · Supabase self-hosted (solo red Docker, sin dominio público).

**14 workflows, 10 activos**:

| ID | Nombre | Notas |
|---|---|---|
| `u0AQPe9pxN79dbFa` | Chatbot clinica zen | 20 nodos salesbot, 4 amojo con token dinámico |
| `RN0wl8RaRmwLpnfQ` | Leads entrantes | reserva chat + voz. Tocado 3-sep: huecos en código + guard + retry Sheets |
| `DkueIeGFWLKh8nTj` | Leads cambio de fecha o anulacion | cancelación voz + chat |
| `PJBMjLLE0vNJjZH8` | Recordatorios | 24h/4h, cada 30 min, desde Google Calendar. Tocado 28-jul |
| `bfc4dWuztZsWfb4Q` | Reenganche Conversaciones Abandonadas | cron 30 min |
| `qBUnBCRxKJEOJGFv` | Especilista Asignado | webhook Kommo `status_lead` 104115983 |
| `13Roz21TOBwy8gp8` | Formulario Pagina web | lead + email |
| `15bh3GWag2IgwLe8` | Derivacion Humano | |
| `s3q2LceTDBvohSIx` | Buscar_base_de_datos | RAG Supabase |
| `FMotimghgUBzEgdm` | Error Handler | `errorWorkflow` de los demás |

Apagados: `wt5vmFCoSEEcYF3O` tmp_test_email_cz · `jp6lfAANQYvi2MbS` TEMP_test_leads_entrantes_v2 · `sIjznBan8THkEbcx` meter info rag · `5ecU1EI4DSs0SPWT` Chabot Laserys (ajeno, borrable).

**Retell** — agente `agent_350620f6b3044226efaeba9111`, LLM `llm_271c1594207dffae30974c56b5e6`, **v70 publicada** (3-sep: huecos calculados en n8n, guard de hueco ocupado, caller-ID; la v67 del 05-ago ya quitaba "Europolis" y la estética proactiva). Voz `custom_voice_c3e5212df87e5341a06ad66e66` (eleven_flash_v2_5, es-ES), `ambient_sound: call-center`, `voice_speed 1.05`, `volume 0.84`. Entra por `+34919934582`. Tools: `Mirar_disponibilidad` (`dia`/`franja`/`hora`), `Reservar`, `Cancelar_cita`, `end_call`, `transfer_call`.

**Salud**: 1 sola ejecución con error en todo el histórico retenido — la de recordatorios de hoy (ver hitos). El resto en verde.

**Observabilidad**: los 9 workflows activos (todos menos el propio handler) tienen `errorWorkflow: FMotimghgUBzEgdm`, y ese handler **sí notifica**: `Error Trigger` → `Preparar contexto` → POST a `https://n8n-borja.tecnocloud.es/webhook/incidencia` con cliente/workflow/nodo/error. El fallo del 28-jul a las 06:30 disparó la incidencia correctamente (ejec 9408 en success). O sea, el hueco no es de instrumentación sino de **que nadie mira ese colector** — el error llevaba 7 horas reportado cuando lo encontré a mano. Pendiente: saber quién vigila las incidencias que llegan ahí (¿Borja? [[tecnocloud]]).

### Trabajo cerrado (04/05-ago) — detalle en [[clinica-zen-historico]]

Pase de tono en chat+voz (saludo, nombre, cierre, teléfono) · fix link roto de Google Maps en 3
workflows (pendiente el mismo link en un Salesbot de Kommo, fuera de n8n) · fix de
`bfc4dWuztZsWfb4Q` (reenganche disparaba sobre conversaciones ya cerradas bien) · "Europolis"
seguía sonando en voz porque el dato crudo del bloque de contexto se lee igual al improvisar, no
solo lo guionado (ver [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]])
· estética facial deja de ofrecerse proactivamente. Voz: v66→v67 publicada. Chat: en vivo.

### Trabajo cerrado (28/29-jul) — detalle en [[clinica-zen-historico]]

Auditoría end-to-end contra las APIs reales (Kommo, Retell, Calendar, IMAP), los tres hitos que el hub
arrastraba desde mayo ya estaban resueltos en producción, y los cuatro bugs de `Recordatorios`
corregidos: Switch sin `options` que mandaba los de 4 h por la rama de 24 h · envíos de madrugada
(ventana 08:00–21:30) · marcado previo al envío que impedía todo reintento · y la causa raíz del 400,
`entity_type` como string en vez de entero — por la que **los recordatorios de WhatsApp no habían
funcionado nunca**. Más el email interno de la reserva por voz, que no salía.

## Próximos hitos

1. **Doble evento por reserva (NEXT)** — cada `Reservar` deja dos eventos en el calendario (30 min y 60 min con distinto título); localizar cuál sobra (`Especilista Asignado` es el sospechoso) y que el guard y los recordatorios miren solo uno.
2. **Recordatorios (`PJBMjLLE0vNJjZH8`) — los 4 bugs corregidos el 28-jul, pendiente de verse en vivo.** Detalle en [[clinica-zen-historico]]. El fix de la causa raíz (`entity_type` string→entero, [[kommo-salesbot-run-entity-type-debe-ser-entero-no-string]]) **sigue sin ejecutarse ni una vez**: 268 ejecuciones en verde hasta el 3-ago sin pasar de `Filtrar y evitar duplicados` porque ninguna cita cruzó la ventana (histórico). Comprobar con las citas del 3-sep. Learnings: [[n8n-switch-conditions-sin-options-enruta-todo-por-la-primera-salida]] · [[recordatorio-relativo-sin-ventana-horaria-escribe-de-madrugada]] · [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]]. Backup pre-fix: `cz-recordatorios-pre-fix-20260728-1339.json`.
3. **Verificar el RAG de Supabase (NEXT)** — es el único corpus que no he podido revisar (self-hosted sin dominio público). Puede seguir teniendo "Europolis" o la dirección vieja. Se comprueba preguntando "¿dónde estáis?" al bot por WhatsApp.
4. **`emiafd@agentesia.madrid` hardcodeado (LATER)** — en `Especilista Asignado`, `toEmail` = `{{ email }}, emiafd@agentesia.madrid`. Buzón de la agencia recibiendo datos de pacientes en producción. Quitar.
5. **Tres teléfonos distintos (LATER)** — prompt dice llamadas `629 494 209` y WhatsApp `919 934 582`; la KB dice `91 993 35 69`; las llamadas entran por `919 934 582`. Decidir cuál es cuál y unificar prompt + KB.
6. **Nitidez de audio (LATER, si Gonzalo insiste)** — medido sobre la grabación: agente −19,8 dBFS, 0 muestras saturadas; el que se oye 5 dB más bajo es el llamante. Candidata real = `ambient_sound: call-center`, que se mezcla después de la grabación y por eso no se oye al escuchar el WAV. Latencia e2e p50 2,35 s / p90 3,35 s también pesa. Prueba: quitar el ambient y llamar. Ver [[retell-ambient-sound-no-esta-en-la-grabacion-auditar-por-config]].
7. **Sin repo local (LATER)** — `~/Projects/clinica-zen` está vacío. Mitigado el 28-jul: los 10 workflows activos + el backup pre-cambio están en `knowledge/projects/agentesia/n8n-backups/clinica-zen/` (trackeado por git, excluido de búsqueda vía `.ignore`). Falta decidir si CZ merece repo propio con `ops/`.

8. **Link de Maps roto en el Salesbot de Kommo (NEXT)** — arreglado en los 3 workflows n8n el 04-ago, pero el mensaje de WhatsApp que lo destapó lo manda un Salesbot/plantilla configurado directamente en la UI de Kommo. Cambiar ahí a `https://www.google.com/maps/search/?api=1&query=40.5066687,-3.8926916`.
9. **Verificar el fix de `bfc4dWuztZsWfb4Q` en ejecuciones reales (NEXT)** — patcheado el 04-ago (query no probada contra la base, self-hosted sin dominio público). Confirmar que corre sin error SQL y que no reabre conversaciones ya cerradas.
10. **Identificarse como IA (art. 50, vigente desde 2-ago) (NEXT)** — falta en Clínica Zen; va en el `begin_message` como en Tecnocloud. Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]].
11. **`Get a call3` en `Leads entrantes` (LATER)** — las pruebas de playground no tienen call real y el nodo rompe la rama del email; poner `onError: continue` o saltarlo cuando no hay `call_id`.
12. **Nombre inventado (a vigilar)** — el 2-ago la v64 reservó como «Paciente nuevo»; desde el 20-ago llega el prompt bueno y el 3-sep las 3 reservas llevaron nombre real. Si reincide, el arreglo es el guard en `Preparar Datos Voz` contra genéricos, no el prompt.

*Descartado tras revisión de Manuel (28-jul)*: que el calendario tenga 2 eventos en 21 días es **normal** para el volumen actual, no hay riesgo de doble reserva. La credencial de Calendar "Cuenta Gonzalo" se mantiene por ahora.

## Bloqueos / esperando a terceros

- ~~**Paginalia no entrega el correo saliente**~~ **DIAGNÓSTICO ERRÓNEO, corregido 29-jul**: la salida externa funciona, el rebote llegó a Spam. Causa real: reputación (dominio nuevo enviando poco). Mitigación pendiente si se quiere entregar a bandeja de pacientes: proveedor transaccional (Resend/Brevo/SES). El aviso interno a `citas@clinicazen.es` es entrega local y no le afecta. Detalle → [[clinica-zen-historico]].

## Links rápidos

- n8n: `https://n8nclinicazen.agentesia.madrid` — credenciales en 1Password vault `Clinica Zen` (`n8n clinica zen`, campo `Api N8N Manu`)
- Retell: item `Retell API` del mismo vault
- Repo email-assets: AgentesIAMadrid/email-assets/clinica-zen/
- Detalle técnico: [[clinica-zen-kommo-workflow]] · [[clinica-zen-supabase]]

## Histórico de hitos

- 2026-09-03: v70 (huecos en n8n, guard hueco ocupado, caller-ID `{{user_number}}`), retry Sheets, limpieza de pruebas; Flow agent como borrador
- 2026-08-20: número desfijado de la v54 → `latest_published`
- 2026-08-05: dirección sin "Europolis"/"en la dehesa" + no mencionar estética proactiva (v67 Retell publicada, chat en vivo)
- 2026-08-04: pase de tono en chat+voz (v66 Retell publicada) + fix link roto de Google Maps en 3 workflows + fix reenganche disparando sobre conversaciones ya cerradas
- 2026-07-28: auditoría completa + fixes del feedback de Gonzalo (dirección, voice_speed, email interno de voz, WhatsApp de voz)
- 2026-07-20/21: pasada sobre chatbot, recordatorios, reenganche y derivación humano
- 2026-05-10: cancelación por status 143 + pipeline 13495347
- 2026-05-07: hero_overlay.jpg y emails actualizados
- 2026-05-04: emails rediseñados con hero stripe + Code node
- 2026-04-29: fix `$if(isExecuted)` en Update leads1 + error handler con JSON.stringify
- 2026-04-23: chatbot + voz completados
