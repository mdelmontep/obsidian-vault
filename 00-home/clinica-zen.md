---
title: clinica-zen
date: 2026-07-28
tags: [cliente, clinica-zen]
---

# Clínica Zen

Clínica dental + estética facial en Las Rozas. Chatbot WhatsApp (Kommo) + agente de voz Retell + recordatorios + emails. Contactos: Gonzalo (legacy), Dani.

Auditado end-to-end el 2026-07-28 vía API (n8n + Retell). Los tres hitos que arrastraba este hub desde mayo estaban ya resueltos en producción; se sustituyen por lo que hay abierto de verdad.

## Estado (verificado 2026-07-28)

**Infra**: servidor `185.47.13.168` · n8n `n8nclinicazen.agentesia.madrid` · Kommo `citasclinicazenes.kommo.com` (account 36308863, pipeline 13495347) · Supabase self-hosted (solo red Docker, sin dominio público).

**14 workflows, 10 activos**:

| ID | Nombre | Notas |
|---|---|---|
| `u0AQPe9pxN79dbFa` | Chatbot clinica zen | 20 nodos salesbot, 4 amojo con token dinámico |
| `RN0wl8RaRmwLpnfQ` | Leads entrantes | reserva chat + voz. Tocado 28-jul |
| `DkueIeGFWLKh8nTj` | Leads cambio de fecha o anulacion | cancelación voz + chat |
| `PJBMjLLE0vNJjZH8` | Recordatorios | 24h/4h, cada 30 min, desde Google Calendar. Tocado 28-jul |
| `bfc4dWuztZsWfb4Q` | Reenganche Conversaciones Abandonadas | cron 30 min |
| `qBUnBCRxKJEOJGFv` | Especilista Asignado | webhook Kommo `status_lead` 104115983 |
| `13Roz21TOBwy8gp8` | Formulario Pagina web | lead + email |
| `15bh3GWag2IgwLe8` | Derivacion Humano | |
| `s3q2LceTDBvohSIx` | Buscar_base_de_datos | RAG Supabase |
| `FMotimghgUBzEgdm` | Error Handler | `errorWorkflow` de los demás |

Apagados: `wt5vmFCoSEEcYF3O` tmp_test_email_cz · `jp6lfAANQYvi2MbS` TEMP_test_leads_entrantes_v2 · `sIjznBan8THkEbcx` meter info rag · `5ecU1EI4DSs0SPWT` Chabot Laserys (ajeno, borrable).

**Retell** — agente `agent_350620f6b3044226efaeba9111`, LLM `llm_271c1594207dffae30974c56b5e6`, **v63 publicada** (28-jul). Voz `custom_voice_c3e5212df87e5341a06ad66e66` (eleven_flash_v2_5, es-ES), `ambient_sound: call-center`, `voice_speed 1.05`, `volume 0.84`. Entra por `+34919934582`. Tools: `Mirar_disponibilidad`, `Reservar`, `Cancelar_cita`, `end_call`, `transfer_call`.

**Salud**: 1 sola ejecución con error en todo el histórico retenido — la de recordatorios de hoy (ver hitos). El resto en verde.

**Observabilidad**: los 9 workflows activos (todos menos el propio handler) tienen `errorWorkflow: FMotimghgUBzEgdm`, y ese handler **sí notifica**: `Error Trigger` → `Preparar contexto` → POST a `https://n8n-borja.tecnocloud.es/webhook/incidencia` con cliente/workflow/nodo/error. El fallo del 28-jul a las 06:30 disparó la incidencia correctamente (ejec 9408 en success). O sea, el hueco no es de instrumentación sino de **que nadie mira ese colector** — el error llevaba 7 horas reportado cuando lo encontré a mano. Pendiente: saber quién vigila las incidencias que llegan ahí (¿Borja? [[tecnocloud]]).

### Resuelto sin registrar (se creía abierto)

- **status_id Kommo 'Cita cancelada'** — `Update leads1` usa `status_id: 143` + `pipeline_id: 13495347`. El 104115987 heredado de Gonzalo ya no está. Arreglado el 2026-05-10. **El bloqueo "pedir el ID a quien gestiona Kommo" era obsoleto.**
- **Retell en leads entrantes** — en producción y verificado con llamada real (`call_a398cee3465ea4472f9a9464ba3`, 28-jul): tool `Reservar` OK, ejecuciones n8n 9422/9423 en success, cita creada.
- **Bug recordatorios por task_type** — **no aplica a CZ**. El blueprint de Simarro dispara desde tareas de Kommo; CZ dispara desde eventos de Google Calendar que llevan `Lead ID:` en la descripción. Cerrado el cabo cruzado de [[simarro]]. Ver [[recordatorios-visita-por-task-type]].
- **amojo_token manual que expiraba cada 24h** — resuelto. El chatbot obtiene el token dinámicamente (`GET /api/v4/account?with=amojo_id` con OAuth2) y 20 de sus nodos ya van por salesbot.

### Hecho el 2026-07-28 (feedback de llamada de Gonzalo)

- **Dirección**: el prompt decía "Polígono Européolis" en 4 sitios. Los 3 que se hablan pasan a *"calle Castillo de Atienza, uno bis, frente al edificio de correos de la dehesa de Navalcarbón"*; el bloque de datos conserva `Pol. Europolis` con la grafía correcta. La KB de Retell ya estaba limpia y ningún workflow lo mencionaba.
- **`voice_speed` 1.12 → 1.05**. `ambient_sound` y `volume` se quedan por decisión de Manuel.
- **La reserva por voz no enviaba NINGÚN email** — la rama de voz nunca tocaba `Build Emails HTML`. Ahora `Pendiente de Asignar A/B` entran en él y el aviso interno sale a `citas@clinicazen.es`. `Build Emails HTML` elige origen con `isExecuted` (chat / voz A / voz B).
- **IF `¿Hay email de paciente?`** antes del correo al paciente: por voz no se pide dirección, así que sin ella no se intenta el envío. Los dos emailSend con `onError: continueRegularOutput`.
- **`WA Confirmación Cita A/B` estaban huérfanos** (0 conexiones) — el agente prometía WhatsApp y no salía nada. Conectados a `Create an event Voz`/`Voz2`. Ver [[canal-nuevo-en-workflow-no-hereda-los-side-effects-de-la-rama-original]].

Backup pre-cambio: `cz-pre-email-voz-20260728-1227.json` (scratchpad de sesión, mover a repo).

### Auditoría de funcionamiento (28-jul) — verificado contra las APIs reales

Todo cruzado contra Kommo, Retell, Google Calendar e IMAP, no leyendo el JSON:

- **Kommo — todo existe y cuadra.** Pipeline `13495347` y los 6 status usados ✓. Los 7 campos personalizados usados existen con el nombre esperado (`1828338` Nombre, `1828340` Fuente de entrada, `1828342` motivo, `1828350` Apagar IA?, `1864817` Día de preferencia, `1864879` Email, `1903454` Respuesta_bot) ✓. Los 4 bots referenciados existen y están **activos** (`63808` recordatorios 4h, `63810` Recordatorio 24h, `63814` Confirmacion cita, `68822` Enviar Respuesta Bot) ✓. Los 2 webhooks de Kommo apuntan a n8n y están activos ✓.
- **Retell — las 4 tools apuntan a webhooks que existen** (`/Reservar_crm`, `/mirar_disponibilidad`, `/cancelar_cita`, `/derivar_humano`) y los 4 workflows leen los argumentos en `body.args.*`, que es como Retell los envía (`args_at_root: false`) ✓. `Derivar_agente` y `Cancelar_cita` no declaran `method`, pero POST es el default documentado ✓. `transfer_call` ya apunta al definitivo `+34629494209` (el hub viejo lo daba por provisional) ✓.
- **El número `+34919934582` no tiene `inbound_agent_id`** y aun así entran llamadas: es `phone_number_type: custom` (SIP trunk de Netelip + LiveKit, visible en las dynamic vars `lk-*`). No es un fallo, pero en el panel se ve "sin agente".
- **Segundo agente no documentado**: `agent_c4cbf4ce04538c867996bfc18a` "Sara Queja" (existe, v5), que `Derivacion Humano` usa para llamar a la clínica vía `create-phone-call` cuando hay queja en horario.
- **Google Calendar responde** ✓, un único calendario `99e8af26…@group.calendar.google.com` compartido por 5 workflows, con la credencial **"Cuenta Gonzalo"** (dependencia de una cuenta personal del contacto legacy; se mantiene por decisión de Manuel).
- **Corregido el mismo día**: `Especilista Asignado / Create new tasks` creaba la cita como `task_type_id: 1` (Follow-up) con `duration: 3600`. Pasa a `2` (Meeting, que existe en la cuenta) y `1800`, que es lo que dura el evento en Calendar.
- **El agente reservaba sin nombre**: en la llamada real llamó a `Reservar` con `"name":"No proporcionado"` — literal que no está ni en n8n ni en el prompt, se lo inventó al saltarse el paso 3 del guion. El lead `33137378` quedó llamado así, y eso es lo que ve la clínica en su agenda, **teniendo el contacto identificado en Kommo como `Gonzalo Riera / +34 609 779 229`**. Doble fix: regla dura en el prompt (v64 publicada) que prohíbe rellenar `name` con texto inventado y exige nombre antes de reservar; y fallback en `Preparar Datos Voz`/`Voz2` que usa el nombre del contacto de Kommo y, en último término, `Paciente <9 dígitos>`. Regex probada contra 10 casos con `node`.

## Próximos hitos

1. **Smoke de la reserva por voz (NEXT, bloquea el resto)** — `POST /Reservar_crm` crea contacto+lead reales en Kommo, evento en Calendar y manda correo. Requiere OK y limpieza posterior. Verifica: email interno llega a `citas@clinicazen.es`, WhatsApp del salesbot llega al paciente, cita correcta.
2. **Recordatorios (`PJBMjLLE0vNJjZH8`) — tres bugs CORREGIDOS el 28-jul, falta el 400 de Kommo**. Salieron de la única ejecución con error del histórico (9407, 28-jul 06:30, lead 32984916, "Julián" `+34617314938`, evento `ejidsbhd41q51j2mqdtu2f7gp8`):
   - ✅ **El de 4h salía por la salida de 24h.** Probado en el `runData`: el item `tipoRecordatorio: "4h"` fue por la rama 0 y la rama 1 quedó a 0 items — las conditions del Switch no llevaban `options`/`combinator`, así que la primera regla se lo tragaba todo. Los avisos de 4 horas llevaban meses saliendo con `bot_id 63810` (plantilla de "mañana tienes cita") en vez de 63808. **Fix**: bloque `options` (`typeValidation: strict`, `version: 2`) + `combinator` + `typeVersion 3.2`. **Verificado en ejecución** con banco de pruebas: `24h`→salida 0, `4h`→salida 1. Ver [[n8n-switch-conditions-sin-options-enruta-todo-por-la-primera-salida]].
   - ✅ **Se escribía al paciente de madrugada.** Las 06:30 no eran un fallo: es el aviso de 4h de una cita de 10:30, con el scanner corriendo 24/7 y la clínica abriendo a las 10:00. **Fix**: ventana de emisión 09:00–21:30 (Europe/Madrid) en el Code de filtrado; fuera de ella no se envía. **Decisión tomada**: se suprime, no se pospone — el de 24h ya avisó y un "faltan 4 horas" enviado a las 09:00 para una cita de las 10:30 sería falso. Si prefieres posponer en vez de suprimir, hay que rehacer la lógica de ventanas. Ver [[recordatorio-relativo-sin-ventana-horaria-escribe-de-madrugada]].
   - ✅ **Un fallo de envío no se reintentaba jamás.** `Filtrar y evitar duplicados` marcaba `staticData.enviados[clave]` antes de enviar. **Fix**: el marcado sale del filtro y pasa a dos nodos `Marcar enviado 24h`/`4h` (modo `runOnceForEachItem`) colgados de cada emisor, que solo escriben si el item no trae `error`; los HTTP llevan `onError: continueRegularOutput`. Además `MARGEN` 15→30 min, para que la ventana (60 min) supere al intervalo del scanner (30 min) y cada evento caiga en DOS pasadas: un envío fallido tiene segunda oportunidad. Ver [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]].
   - ✅ **CAUSA RAÍZ del 400 encontrada (no era el chat de WhatsApp).** `entity_type` iba como **string** `"2"` en los dos nodos de Recordatorios; la API lo exige **entero**. Probado contra Kommo con IDs inexistentes (sin enviar nada a nadie): `entity_type: 2` → `403 Entity not found` (pasa validación); `entity_type: "2"` → `400 Invalid field: entity_type` (idéntico al de producción). **Consecuencia: los recordatorios de WhatsApp NUNCA han funcionado**, ni los de 24h ni los de 4h, y el marcado previo al envío lo ocultó desde el primer día. Los otros 13 nodos `salesbot/run` del sistema (chatbot, reenganche, confirmación de cita) ya usaban entero y sí funcionan. **Fix**: `"2"` → `2`. Ver [[kommo-salesbot-run-entity-type-debe-ser-entero-no-string]].
   - ⚠️ **Corrección de la hora**: el intento fallido fue a las **08:30 de Madrid**, no a las 06:30 (eso era UTC). La cita era a las 12:30. El caso malo real es una cita a las 10:00 (apertura), cuyo aviso de 4h cae a las **06:00**. Por eso `HORA_MIN` quedó en **08:00**, no en 09:00: con 09:00 se habría suprimido un aviso legítimo de las 08:30. Simulado: cita 12:30→envía, 10:00→suprime, 16:00→envía.
   Backup pre-fix: `cz-recordatorios-pre-fix-20260728-1339.json`.
3. **Verificar el RAG de Supabase (NEXT)** — es el único corpus que no he podido revisar (self-hosted sin dominio público). Puede seguir teniendo "Europolis" o la dirección vieja. Se comprueba preguntando "¿dónde estáis?" al bot por WhatsApp.
4. **`emiafd@agentesia.madrid` hardcodeado (LATER)** — en `Especilista Asignado`, `toEmail` = `{{ email }}, emiafd@agentesia.madrid`. Buzón de la agencia recibiendo datos de pacientes en producción. Quitar.
5. **Tres teléfonos distintos (LATER)** — prompt dice llamadas `629 494 209` y WhatsApp `919 934 582`; la KB dice `91 993 35 69`; las llamadas entran por `919 934 582`. Decidir cuál es cuál y unificar prompt + KB.
6. **Nitidez de audio (LATER, si Gonzalo insiste)** — medido sobre la grabación: agente −19,8 dBFS, 0 muestras saturadas; el que se oye 5 dB más bajo es el llamante. Candidata real = `ambient_sound: call-center`, que se mezcla después de la grabación y por eso no se oye al escuchar el WAV. Latencia e2e p50 2,35 s / p90 3,35 s también pesa. Prueba: quitar el ambient y llamar. Ver [[retell-ambient-sound-no-esta-en-la-grabacion-auditar-por-config]].
7. **Sin repo local (LATER)** — `~/Projects/clinica-zen` está vacío. Mitigado el 28-jul: los 10 workflows activos + el backup pre-cambio están en `knowledge/projects/agentesia/n8n-backups/clinica-zen/` (trackeado por git, excluido de búsqueda vía `.ignore`). Falta decidir si CZ merece repo propio con `ops/`.
8. ~~**n8n solo retiene las ejecuciones del día**~~ **RESUELTO 29-jul**: la causa era `EXECUTIONS_DATA_MAX_AGE=7` **dentro del `composeFile`** del stack (no en el Environment, donde no había ninguna `EXECUTIONS_*`). La variable va en **horas**, no en días: quien la puso quiso decir 7 días y dejó 7 horas. Corregido a `336` (14 días, el default oficial) + `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`, aplicado por la API de Dokploy y desplegado (corte real de 13 s, 10:06:05→10:06:18 UTC; los 10 workflows activos volvieron íntegros). Backup: `cz-compose-n8n-pre-retencion-20260729-1203.yml`. Ver [[n8n-executions-data-max-age-va-en-horas-no-en-dias]].
   *Detalle previo (obsoleto)*: **n8n solo retenía las ejecuciones del día (NEXT)** — las 44 retenidas son todas del 28-jul, ni una de días anteriores, cuando los defaults oficiales de n8n son `EXECUTIONS_DATA_MAX_AGE=336` (14 días) y `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`: alguien los bajó. Sin histórico no se detecta un fallo recurrente — el 400 de los recordatorios se cazó por horas, el mismo día en que se produjo. **Bloqueado**: la clave SSH de Manu no está autorizada en `185.47.13.168:5251`; hace falta `ssh-copy-id` y luego editar el env en *panel Dokploy → Environment* (nunca en disco, Dokploy lo regenera).
9. **Bots del Digital Pipeline sin verificar en la GUI (LATER)** — 4 de los 8 bots de Kommo no los lanza n8n sino el Digital Pipeline por cambio de estado: `63804` NPS Bot, `63812` especilista asignado, `64322` vALORACION SERVICIO, `69536` Formulario web. Todos activos, y el reparto tiene sentido (el bot manda WhatsApp, n8n manda email). El único a confirmar es `63812`, que se dispara con el mismo estado `104115983` que el workflow `qBUnBCRxKJEOJGFv`: comprobar en la GUI que no mandan lo mismo dos veces. El enganche bot↔estado no es consultable por API.

*Descartado tras revisión de Manuel (28-jul)*: que el calendario tenga 2 eventos en 21 días es **normal** para el volumen actual, no hay riesgo de doble reserva. La credencial de Calendar "Cuenta Gonzalo" se mantiene por ahora.

## Bloqueos / esperando a terceros

- **Paginalia no entrega el correo saliente a dominios externos (28-jul)** — el SMTP `mail.clinicazen.es:465` acepta y encola (`250 Ok: queued`) pero nada sale. Probado: 3 correos a `@agentesia.madrid` sin llegar; uno al propio `citas@clinicazen.es` **entregado en 4 s**; sonda a una dirección inexistente de Gmail sin rebote a los 7 min (Gmail devolvería `550` en segundos si lo recibiera); 0 rebotes acumulados en el buzón. Descartado todo lo demás: buzón destino existe (`250` al RCPT contra `aspmx.l.google.com`), SPF autoriza la IP de salida por `+mx` y `+a:vps01.paginalia.es`, DKIM `default` publicado, FCrDNS coherente (`185.99.186.74` ↔ `ns1.paginalia.es`), IP limpia en Spamhaus/Spamcop/Barracuda, dominio limpio en DBL.
  **Acción**: ticket a Paginalia con los IDs de cola `C31C3BD1B2`, `DA84BBFC98`, `7E1ACBFC98`, `2114DBDD65` (externos, no entregados) y `A3247BFC98` (interno, entregado — sirve de contraste).
  **Consecuencia**: el aviso interno a `citas@clinicazen.es` que conecté hoy SÍ funciona (entrega local); el correo al paciente **no llegará** aunque se cablee, porque los pacientes están en Gmail/Hotmail. Corrobora la queja: en el buzón solo hay 2 avisos de "Nueva cita", ambos de mayo. Ver [[smtp-acepta-con-250-queued-y-no-entrega-fuera]].

## Links rápidos

- n8n: `https://n8nclinicazen.agentesia.madrid` — credenciales en 1Password vault `Clinica Zen` (`n8n clinica zen`, campo `Api N8N Manu`)
- Retell: item `Retell API` del mismo vault
- Repo email-assets: AgentesIAMadrid/email-assets/clinica-zen/
- Detalle técnico: [[clinica-zen-kommo-workflow]] · [[clinica-zen-supabase]]

## Histórico de hitos

- 2026-07-28: auditoría completa + fixes del feedback de Gonzalo (dirección, voice_speed, email interno de voz, WhatsApp de voz)
- 2026-07-20/21: pasada sobre chatbot, recordatorios, reenganche y derivación humano
- 2026-05-10: cancelación por status 143 + pipeline 13495347
- 2026-05-07: hero_overlay.jpg y emails actualizados
- 2026-05-04: emails rediseñados con hero stripe + Code node
- 2026-04-29: fix `$if(isExecuted)` en Update leads1 + error handler con JSON.stringify
- 2026-04-23: chatbot + voz completados
