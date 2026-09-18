---
title: clinica-zen
date: 2026-07-29
updated: 2026-09-18
tags: [cliente, clinica-zen]
---

# Clínica Zen

Clínica dental + estética facial en Las Rozas. Chatbot WhatsApp (Kommo) + agente de voz Retell + recordatorios + emails. Contactos: Gonzalo (legacy), Dani.

## Estado 15/18-sep-2026: valoración post-cita en WhatsApp

Al mover el lead a **111224991** o **111225743** sale la plantilla «Valorar Servicio» **2 h después**,
solo entre 10:00 y 21:00 (si no, a las 10:00 del día siguiente): `sa3W3r6WfVoV9sd9` + webhook Kommo
`47478027` → salesbot **64322**. `?inmediato=1` salta espera y candado (solo pruebas).

- **Una sola vez por paciente**: etiqueta `Valoración solicitada` en el CONTACTO (no en el lead) +
  `INCR` en Redis con TTL 26 h; re-lee lead y contacto tras la espera. Quitar la etiqueta = reenviar.
  → [[envio-unico-por-paciente-se-marca-en-el-contacto-no-en-el-lead]]
- **Botones** (chatbot `u0AQPe9pxN79dbFa`): «Muy buena» → gracias personalizado con el nombre de pila +
  enlace de reseña `https://g.page/r/CXrEhc4g7n4MEBM/review`; «No muy buena» → pregunta el motivo y lo
  captura (Redis `pendiente`→`capturado`). Nota + etiqueta en Kommo en los tres casos.
- **El enlace sale como `kommo.cc`** y Manuel lo da por bueno (18-sep): Kommo reescribe los enlaces de
  los textos del bot, no los de una plantilla. Se descartó la plantilla con botón «Dejar reseña».
  → [[kommo-acorta-enlaces-del-salesbot-pero-no-los-de-plantilla]]
- **Reenganche**: tras una valoración ya no salta el «¿Sigues por ahí?» — etapa 111224991 añadida al
  gate y la sesión se marca `skipped` desde el chatbot.
  → [[una-etapa-nueva-del-embudo-no-entra-sola-en-los-gates-que-listan-etapas]]
- **Plantillas**: «Recordatorio Cita» (92996) sustituye a «Envia Recordatorio» en el bot de 24 h — con
  los teléfonos y el enlace largo de Maps. Probado E2E contra el 617314938 (lead 38631418).
  → [[plantilla-waba-en-kommo-se-crea-y-edita-solo-desde-la-ui]]

## Estado 8/9-sep-2026 — condensado, ya estrenado

Un solo escritor de la etapa del lead (los 10 `salesbot*` de `u0AQPe9pxN79dbFa` y `Update leads` de
`RN0wl8RaRmwLpnfQ` ya no la escriben; los 4 `Marcar Pendiente si Reserva*` sí) · **regla de negocio**:
contestamos → Contestados, hay cita → Pendiente de asignar · `NO_PISAR` con `143`/`111224991`, así que
quien cancela no resucita · reenganche con gate de ESTADO y descarte persistido (`status='skipped'`) ·
DST por número de mes (citas 1 h antes ~34 días/año), `ccEmail` fuera de `options` y confirmación
escrita al que reserva por voz, los tres arreglados. Todo verificado en vivo desde entonces.
Kommo devuelve **400**, no 404, para un lead que ya no existe.

**Abierto**: capturar email y teléfono en la llamada (es del agente Retell) · el que anula y escribe
*sin* volver a reservar se queda en Perdido y fuera del radar — si la clínica lo quiere ver, etapa o
tarea propia, no sacar `143` de la lista.

Detalle → [[clinica-zen-historico]] · [[el-nodo-que-envia-el-mensaje-no-debe-escribir-la-etapa-del-lead]] ·
[[un-descarte-que-no-se-persiste-recircula-y-con-limit-desplaza-a-los-reales]] ·
[[al-centralizar-quien-escribe-el-estado-quedan-dos-huecos-tipicos]] ·
[[offset-de-zona-horaria-por-numero-de-mes-desfasa-una-hora-las-citas]] ·
[[ccemail-en-la-raiz-del-nodo-email-se-descarta-sin-dar-error]]

## v70 en producción (3-sep) — condensado

`Mirar_disponibilidad` recibe `dia`/`franja`/`hora` y n8n devuelve los huecos ya calculados (la v67 los
calculaba en el LLM y aceptaba horas fuera de lista) · guard en `Reservar_crm` que relee el calendario
±1 h · caller-ID con `{{user_number}}`. Agente **Flow** `agent_d3c52ef4ee0f2eeb6904212c05` sigue como
borrador sin número. **Visto y no tocado**: cada reserva crea DOS eventos (30 y 60 min) · las pruebas de
playground fallan en `Get a call3` · `transfer_call` no va desde el test web. Detalle →
[[clinica-zen-historico]] · [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]] ·
[[retell-from_number-no-auto-sustituye-en-tool-args]]

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
| `sa3W3r6WfVoV9sd9` | Valoracion post-cita | webhook Kommo `status_lead` 111224991/111225743 → espera 2 h → salesbot 64322 (18-sep) |
| `13Roz21TOBwy8gp8` | Formulario Pagina web | lead + email |
| `15bh3GWag2IgwLe8` | Derivacion Humano | |
| `s3q2LceTDBvohSIx` | Buscar_base_de_datos | RAG Supabase |
| `FMotimghgUBzEgdm` | Error Handler | `errorWorkflow` de los demás |

Apagados: `wt5vmFCoSEEcYF3O` tmp_test_email_cz · `jp6lfAANQYvi2MbS` TEMP_test_leads_entrantes_v2 · `sIjznBan8THkEbcx` meter info rag · `5ecU1EI4DSs0SPWT` Chabot Laserys (ajeno, borrable).

**Retell** — agente `agent_350620f6b3044226efaeba9111`, LLM `llm_271c1594207dffae30974c56b5e6`, **v70 publicada** (3-sep: huecos calculados en n8n, guard de hueco ocupado, caller-ID; la v67 del 05-ago ya quitaba "Europolis" y la estética proactiva). Voz `custom_voice_c3e5212df87e5341a06ad66e66` (eleven_flash_v2_5, es-ES), `ambient_sound: call-center`, `voice_speed 1.05`, `volume 0.84`. Entra por `+34919934582`. Tools: `Mirar_disponibilidad` (`dia`/`franja`/`hora`), `Reservar`, `Cancelar_cita`, `end_call`, `transfer_call`.

**Observabilidad**: los 9 workflows activos tienen `errorWorkflow: FMotimghgUBzEgdm`, y ese handler sí notifica (POST a `n8n-borja.tecnocloud.es/webhook/incidencia`). El hueco no es de instrumentación sino de **que nadie mira ese colector**: el fallo del 28-jul llevaba 7 h reportado cuando lo encontré a mano. Pendiente saber quién lo vigila (¿Borja? [[tecnocloud]]). Detalle → [[clinica-zen-historico]]

### Trabajo cerrado (jul/ago) — detalle en [[clinica-zen-historico]]

- **04/05-ago**: tono de chat y voz (v66/v67 publicadas), dirección sin «Europolis», link de Maps roto
  en 3 workflows, primer parche del reenganche sobre conversaciones cerradas.
- **28/29-jul**: auditoría completa de los 14 workflows y el feedback de Gonzalo (dirección,
  `voice_speed`, email interno de voz, WhatsApp de voz); el falso diagnóstico de Paginalia, corregido.

## Próximos hitos

1. **Doble evento por reserva (NEXT)** — cada `Reservar` deja dos eventos en el calendario (30 min y 60 min con distinto título); localizar cuál sobra (`Especilista Asignado` es el sospechoso) y que el guard y los recordatorios miren solo uno.
2. **Recordatorios (`PJBMjLLE0vNJjZH8`) — 4 bugs corregidos el 28-jul, sin verse en vivo aún**: 268 ejecuciones en verde sin pasar de `Filtrar y evitar duplicados` porque ninguna cita cruzó la ventana. Comprobar con las citas del 3-sep. Detalle y los 4 learnings → [[clinica-zen-historico]] · [[kommo-salesbot-run-entity-type-debe-ser-entero-no-string]]
3. **Verificar el RAG de Supabase (NEXT)** — es el único corpus que no he podido revisar (self-hosted sin dominio público). Puede seguir teniendo "Europolis" o la dirección vieja. Se comprueba preguntando "¿dónde estáis?" al bot por WhatsApp.
4. **`emiafd@agentesia.madrid` hardcodeado (LATER)** — en `Especilista Asignado`, `toEmail` = `{{ email }}, emiafd@agentesia.madrid`. Buzón de la agencia recibiendo datos de pacientes en producción. Quitar.
5. **Tres teléfonos distintos (LATER)** — prompt dice llamadas `629 494 209` y WhatsApp `919 934 582`; la KB dice `91 993 35 69`; las llamadas entran por `919 934 582`. Decidir cuál es cuál y unificar prompt + KB.
6. **Nitidez de audio (LATER, si Gonzalo insiste)** — el agente no satura (−19,8 dBFS); la candidata es `ambient_sound: call-center`, que no está en la grabación. Prueba: quitarlo y llamar. Ver [[retell-ambient-sound-no-esta-en-la-grabacion-auditar-por-config]]
7. **Sin repo local (LATER)** — `~/Projects/clinica-zen` está vacío; los 10 workflows activos y los backups viven en `knowledge/projects/agentesia/n8n-backups/clinica-zen/` (git, fuera de búsqueda vía `.ignore`). Falta decidir si CZ merece repo propio con `ops/`.

7b. **Plantillas de WhatsApp pendientes (NEXT)** — «Doctor Asignado» (`79256`) está RECHAZADA por Meta y el bot que la manda no envía nada; «Nueva plantilla de WhatsApp (15.09.2026 14:30)» (`92532`) quedó aprobada pero rota (variable como texto `[Manu]`, botón a `…/review.` → 404) y hay que borrarla; el recordatorio de 4 h (`79254`) sigue sin los teléfonos. Estado de todas: `GET /api/v4/chats/templates?with=reviews`.

8. **Link de Maps roto en el Salesbot de Kommo (NEXT)** — arreglado en los 3 workflows n8n el 04-ago, pero el mensaje de WhatsApp que lo destapó lo manda un Salesbot/plantilla configurado directamente en la UI de Kommo. Cambiar ahí a `https://www.google.com/maps/search/?api=1&query=40.5066687,-3.8926916`.
9. **Identificarse como IA (art. 50, vigente desde 2-ago) (NEXT)** — falta en Clínica Zen; va en el `begin_message` como en Tecnocloud. Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]].
10. **Correo solo-HTML (LATER)** — los tres `emailSend` mandan solo `html`, sin parte text/plain y con imágenes remotas de githubusercontent. Añadir la parte de texto ayuda a la clasificación; el CC externo a `info@zendental.es` es el que sufre.
11. **`Get a call3` en `Leads entrantes` (LATER)** — las pruebas de playground no tienen call real y el nodo rompe la rama del email; poner `onError: continue` o saltarlo cuando no hay `call_id`.
12. **Nombre inventado (a vigilar)** — el 2-ago la v64 reservó como «Paciente nuevo»; desde el 20-ago llega el prompt bueno y el 3-sep las 3 reservas llevaron nombre real. Si reincide, el arreglo es el guard en `Preparar Datos Voz` contra genéricos, no el prompt.

*Descartado tras revisión de Manuel (28-jul)*: que el calendario tenga 2 eventos en 21 días es **normal** para el volumen actual, no hay riesgo de doble reserva. La credencial de Calendar "Cuenta Gonzalo" se mantiene por ahora.

## Bloqueos / esperando a terceros

- ~~**Paginalia no entrega el correo saliente**~~ **DIAGNÓSTICO ERRÓNEO, corregido 29-jul**: la salida externa funciona, el rebote llegó a Spam. Causa real: reputación (dominio nuevo enviando poco). **Reconfirmado 8-sep** con el CC externo a `info@zendental.es`: SPF, DKIM, DMARC, FCrDNS y 4 RBL en verde y aun así Spam en Gmail. Único matiz nuevo: el HELO es `vps01.paginalia.es` y el PTR `ns1.paginalia.es` (FCrDNS pasa igual, ambos resuelven a 185.99.186.74) → señal menor, no la causa. Mitigación pendiente si se quiere entregar a bandeja de pacientes: proveedor transaccional (Resend/Brevo/SES). El aviso interno a `citas@clinicazen.es` es entrega local y no le afecta. Detalle → [[clinica-zen-historico]].

## Links rápidos

- n8n: `https://n8nclinicazen.agentesia.madrid` — credenciales en 1Password vault `Clinica Zen` (`n8n clinica zen`, campo `Api N8N Manu`)
- Retell: item `Retell API` del mismo vault
- Repo email-assets: AgentesIAMadrid/email-assets/clinica-zen/
- Detalle técnico: [[clinica-zen-kommo-workflow]] · [[clinica-zen-supabase]]

## Histórico de hitos

- 2026-09-08: etapa del lead escrita desde un único nodo (chatbot + reenganche); resumen IA de la conversación en el correo interno + CC a info@zendental.es
- 2026-09-08 (noche): reenganche con gate de estado + descarte persistido y `ORDER BY`; `Update leads` escribe Pendiente de asignar al reservar; `NO_PISAR` con «Perdido» (en discusión)
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
