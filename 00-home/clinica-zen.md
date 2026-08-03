---
title: clinica-zen
date: 2026-07-29
tags: [cliente, clinica-zen]
---

# Clínica Zen

Clínica dental + estética facial en Las Rozas. Chatbot WhatsApp (Kommo) + agente de voz Retell + recordatorios + emails. Contactos: Gonzalo (legacy), Dani.

Auditado end-to-end el 2026-07-28/29 vía API (n8n, Retell, Kommo, Google Calendar, IMAP) y GUI de Kommo. Los tres hitos que arrastraba este hub desde mayo estaban ya resueltos en producción.

**Estado 29-jul: nada bloqueante y nada roto conocido.** Lo corregido está verificado por partes ejecutándose (Switch, Code de ambas ramas de reserva, generador de email, deploy); lo que falta es verlo funcionar de punta a punta con un paciente real — llega solo con el uso: cuando los contadores de los bots `63810`/`63808` dejen de estar a 0 en Kommo, los recordatorios funcionan.

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

### Trabajo cerrado (28/29-jul) — detalle en [[clinica-zen-historico]]

Auditoría end-to-end contra las APIs reales (Kommo, Retell, Calendar, IMAP), los tres hitos que el hub
arrastraba desde mayo ya estaban resueltos en producción, y los cuatro bugs de `Recordatorios`
corregidos: Switch sin `options` que mandaba los de 4 h por la rama de 24 h · envíos de madrugada
(ventana 08:00–21:30) · marcado previo al envío que impedía todo reintento · y la causa raíz del 400,
`entity_type` como string en vez de entero — por la que **los recordatorios de WhatsApp no habían
funcionado nunca**. Más el email interno de la reserva por voz, que no salía.

## Verificación por API del 2026-08-03 (read-only, sin tocar nada)

Medido el **efecto**, no el estado de las ejecuciones. Método y contexto en [[agentes-cliente-tres-capas]].

- **Recordatorios: el fix del `entity_type` SIGUE SIN VERIFICAR en producción.** Inspeccionadas una a
  una las **268 ejecuciones retenidas** de `PJBMjLLE0vNJjZH8` (29-jul 02:30 → 3-ago 16:00), todas en
  `success`: **ninguna pasó de `Filtrar y evitar duplicados`**. Ni el Switch ni los dos nodos
  `WhatsApp Recordatorio 24h/4h` se ejecutaron una sola vez. No es un bug — es que no ha habido
  ninguna cita cruzando la ventana: los únicos dos eventos del calendario están a más de 24 h.
  **Las 268 ejecuciones en verde no prueban absolutamente nada**, que es justo el punto.
  - **Primera oportunidad real de verificarlo: el 4-ago sobre las 11:30** (recordatorio de 24 h del
    evento del 5-ago 11:30, lead 33137378). El de 4 h de esa cita caería a las 07:30 → **se suprime
    por la ventana 08:00–21:30**, por diseño. Segunda y tercera: 5-ago ~17:30 (24 h) y 6-ago ~13:30
    (4 h, esta sí dentro de ventana) para el evento del 6-ago 17:30.
- 🔴 **El fix del nombre inventado NO funcionó — reincidió el 2-ago con la v64 ya publicada.** En la
  llamada `call_f730941298c987b1fbbf9f0a913` (2-ago 12:38, desde `+34609779229`) el agente **nunca
  preguntó el nombre** — el transcript va servicio → primera vez → día → hora → teléfono →
  consentimiento → reservar — y llamó a `Reservar` con `"name":"Paciente nuevo"`. Antes inventaba
  `"No proporcionado"`; ahora inventa `"Paciente nuevo"`. La cita del 6-ago 17:30 figura en la agenda
  de la clínica como *"Odontología - Valoración - Paciente nuevo"* (lead `37513628`), con el teléfono
  identificado en Kommo.
  - El fallback de `Preparar Datos Voz`/`Voz2` **no puede entrar**: solo actúa si `name` viene vacío o
    ausente, y el LLM manda siempre un string plausible.
  - Es exactamente [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]]: un invariante de
    dominio no se defiende con una regla del prompt. **Arreglo correcto**: validar en el Code node —
    si `name` falta **o casa una lista de genéricos** (`No proporcionado`, `Paciente nuevo`, `Paciente`,
    `Cliente`, `Sin nombre`…), resolver contra el contacto de Kommo por teléfono y, en último término,
    `Paciente <9 dígitos>`. Y en general no fiarse del `name` del LLM cuando el teléfono ya identifica
    al contacto ([[dos-campos-confundibles-pide-los-dos-y-cruzalos-en-codigo]]).
- **La dirección vieja se sigue diciendo.** En esa misma llamada: *"Estamos en la calle Castillo de
  Atienza, uno bis, **en el Polígono Européolis** de Las Rozas"*. El fix del 28-jul dejó `Pol. Europolis`
  en el bloque de datos por considerarlo no hablado — se habla. Es literalmente lo que pidió corregir
  Gonzalo.
- **Volumen real, para calibrar**: el agente de voz lleva **50 llamadas en total desde mayo**, y las de
  julio/agosto son casi todas desde el móvil de Gonzalo (`+34609779229`) o el de Manu (`+34617314938`).
  Sin tráfico de pacientes no hay forma de que un fallo aflore solo: por eso hace falta el check de
  efecto, no esperar a que salte algo.

## Próximos hitos

1. **Smoke de la reserva por voz (NEXT, bloquea el resto)** — `POST /Reservar_crm` crea contacto+lead reales en Kommo, evento en Calendar y manda correo. Requiere OK y limpieza posterior. Verifica: email interno llega a `citas@clinicazen.es`, WhatsApp del salesbot llega al paciente, cita correcta.
2. **Recordatorios (`PJBMjLLE0vNJjZH8`) — los 4 bugs corregidos el 28-jul, pendiente de verse en vivo.** Detalle en [[clinica-zen-historico]]. El fix de la causa raíz (`entity_type` string→entero, [[kommo-salesbot-run-entity-type-debe-ser-entero-no-string]]) **sigue sin ejecutarse ni una vez**: ver la verificación del 3-ago arriba. Learnings: [[n8n-switch-conditions-sin-options-enruta-todo-por-la-primera-salida]] · [[recordatorio-relativo-sin-ventana-horaria-escribe-de-madrugada]] · [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]]. Backup pre-fix: `cz-recordatorios-pre-fix-20260728-1339.json`.
3. **Verificar el RAG de Supabase (NEXT)** — es el único corpus que no he podido revisar (self-hosted sin dominio público). Puede seguir teniendo "Europolis" o la dirección vieja. Se comprueba preguntando "¿dónde estáis?" al bot por WhatsApp.
4. **`emiafd@agentesia.madrid` hardcodeado (LATER)** — en `Especilista Asignado`, `toEmail` = `{{ email }}, emiafd@agentesia.madrid`. Buzón de la agencia recibiendo datos de pacientes en producción. Quitar.
5. **Tres teléfonos distintos (LATER)** — prompt dice llamadas `629 494 209` y WhatsApp `919 934 582`; la KB dice `91 993 35 69`; las llamadas entran por `919 934 582`. Decidir cuál es cuál y unificar prompt + KB.
6. **Nitidez de audio (LATER, si Gonzalo insiste)** — medido sobre la grabación: agente −19,8 dBFS, 0 muestras saturadas; el que se oye 5 dB más bajo es el llamante. Candidata real = `ambient_sound: call-center`, que se mezcla después de la grabación y por eso no se oye al escuchar el WAV. Latencia e2e p50 2,35 s / p90 3,35 s también pesa. Prueba: quitar el ambient y llamar. Ver [[retell-ambient-sound-no-esta-en-la-grabacion-auditar-por-config]].
7. **Sin repo local (LATER)** — `~/Projects/clinica-zen` está vacío. Mitigado el 28-jul: los 10 workflows activos + el backup pre-cambio están en `knowledge/projects/agentesia/n8n-backups/clinica-zen/` (trackeado por git, excluido de búsqueda vía `.ignore`). Falta decidir si CZ merece repo propio con `ops/`.
8. ~~**n8n solo retiene las ejecuciones del día**~~ **RESUELTO 29-jul**: la causa era `EXECUTIONS_DATA_MAX_AGE=7` **dentro del `composeFile`** del stack (no en el Environment, donde no había ninguna `EXECUTIONS_*`). La variable va en **horas**, no en días: quien la puso quiso decir 7 días y dejó 7 horas. Corregido a `336` (14 días, el default oficial) + `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`, aplicado por la API de Dokploy y desplegado (corte real de 13 s, 10:06:05→10:06:18 UTC; los 10 workflows activos volvieron íntegros). Backup: `cz-compose-n8n-pre-retencion-20260729-1203.yml`. Ver [[n8n-executions-data-max-age-va-en-horas-no-en-dias]].
   *Detalle previo (obsoleto)*: **n8n solo retenía las ejecuciones del día (NEXT)** — las 44 retenidas son todas del 28-jul, ni una de días anteriores, cuando los defaults oficiales de n8n son `EXECUTIONS_DATA_MAX_AGE=336` (14 días) y `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`: alguien los bajó. Sin histórico no se detecta un fallo recurrente — el 400 de los recordatorios se cazó por horas, el mismo día en que se produjo. **Bloqueado**: la clave SSH de Manu no está autorizada en `185.47.13.168:5251`; hace falta `ssh-copy-id` y luego editar el env en *panel Dokploy → Environment* (nunca en disco, Dokploy lo regenera).
9. ~~**Bots del Digital Pipeline sin verificar en la GUI**~~ **VERIFICADO 29-jul en la GUI**. Los 8 bots, con sus lanzamientos históricos: `Enviar Respuesta Bot` 350 · `Confirmacion cita` 104 (trigger etapa pENDIENTE DE ASIGNAR, plantilla *Confirmación Cita*) · `especilista asignado` 17 (trigger etapa) · `Formulario web` 10 (trigger etapa) · `vALORACION SERVICIO` 3 · **`Recordatorio 24 horas antes` 0** · **`recordatorios 4 horas antes` 0** · `NPS Bot` 0. Los dos de recordatorio **nunca se habían ejecutado**: confirmación en el propio Kommo del bug del `entity_type`. Ambos están bien montados — sin disparador propio (los lanza n8n), plantilla correcta cada uno (`Envia Recordatorio` el de 24h, *"Te esperamos hoy"* / 79254 el de 4h) y rama de error. No hay nada que tocar en los bots. Las **6 plantillas WABA están Aprobadas** (WABA ID `2697891833940384`); 5 en Marketing y `Doctor Asignado` en Utility.
   **DECISIÓN (Manuel, 29-jul): NO recategorizar a Utility.** Lo propuse por regla general, pero la evidencia lo desmiente: `Confirmacion cita` entrega con 94% sobre 104 envíos, y es Meta quien fija la categoría (recategoriza sola si cree que está mal). El ahorro de coste a este volumen es de céntimos y los límites de marketing por usuario no muerden. En contra pesa más: **editar una plantilla WABA la manda de vuelta a revisión de Meta**, y a esta cuenta ya le rechazaron plantillas el 21-jul (avisos de `support@kommo.com` en el buzón de `citas@`; las actuales son del 23 por eso). No tocar lo que entrega.
   *Entrada previa (obsoleta)*: **Bots del Digital Pipeline sin verificar en la GUI (LATER)** — 4 de los 8 bots de Kommo no los lanza n8n sino el Digital Pipeline por cambio de estado: `63804` NPS Bot, `63812` especilista asignado, `64322` vALORACION SERVICIO, `69536` Formulario web. Todos activos, y el reparto tiene sentido (el bot manda WhatsApp, n8n manda email). El único a confirmar es `63812`, que se dispara con el mismo estado `104115983` que el workflow `qBUnBCRxKJEOJGFv`: comprobar en la GUI que no mandan lo mismo dos veces. El enganche bot↔estado no es consultable por API.

*Descartado tras revisión de Manuel (28-jul)*: que el calendario tenga 2 eventos en 21 días es **normal** para el volumen actual, no hay riesgo de doble reserva. La credencial de Calendar "Cuenta Gonzalo" se mantiene por ahora.

## Bloqueos / esperando a terceros

- ~~**Paginalia no entrega el correo saliente**~~ **DIAGNÓSTICO ERRÓNEO, corregido 29-jul**. El rebote de la sonda SÍ llegó — a la carpeta **Spam** del buzón, 7 min después del envío; yo lo busqué a los 2 min y solo en INBOX. Gmail respondió `550-5.1.1 ... does not exist`, o sea **la salida externa funciona**. No hay nada que reclamar a Paginalia.
  **Causa real: reputación.** Cabeceras de un envío propio: `dmarc=pass (p=QUARANTINE)`, `dkim=pass header.d=clinicazen.es` (firma con selector `default`), `spf=pass`. Autenticación impecable — Google los aparca en Spam porque `clinicazen.es` casi no envía correo, sale por IP compartida de un hosting pequeño y escribe a buzones sin historial previo. Las 3 pruebas seguidas con asunto `[TEST]` y sin texto plano tampoco ayudaron.
  **Mitigaciones**: (1) remitente permitido en Workspace (Admin → Apps → Gmail → Spam) para el correo interno de AgentesIA; (2) para emails a PACIENTES (Gmail/Hotmail), proveedor transaccional con reputación propia (Resend/Brevo/SES) autenticando `clinicazen.es` — es lo estándar y no depende del VPS compartido.
  **Impacto real ACOTADO**: el aviso interno de la reserva por voz va a `citas@clinicazen.es`, que es **entrega local en el mismo servidor** (probado: 4 s) — no pasa por Google ni por filtro de spam. La clínica sí recibe sus avisos.

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
