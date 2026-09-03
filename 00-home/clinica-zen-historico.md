---
title: clinica-zen — histórico detallado
date: 2026-08-03
tags: [cliente, clinica-zen, historico]
---

# Clínica Zen — histórico

Detalle de hitos ya cerrados, sacados del hub el 2026-08-03 para que el arranque de sesión no los
pague en contexto. El estado vivo está en [[clinica-zen]].

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
- ~~**`WA Confirmación Cita A/B` estaban huérfanos**~~ **REVERTIDO 29-jul**: los conecté a `Create an event Voz`/`Voz2` creyendo que el agente prometía un WhatsApp que nadie enviaba. **Falso**: el salesbot `63814` "Confirmacion cita" ya se dispara solo con el trigger *"lead movido o creado en la etapa pENDIENTE DE ASIGNAR"* — justo lo que hace la rama de voz — y llevaba **104 lanzamientos** en Kommo. Mi conexión habría mandado la confirmación **dos veces** al paciente. Los nodos vuelven a estar desconectados, como estaban. El contador de lanzamientos del bot solo se ve en la GUI, no por API. Ver [[nodo-huerfano-puede-estar-desconectado-porque-otro-mecanismo-ya-lo-cubre]].

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


### Retención de ejecuciones n8n (29-jul) — RESUELTO

Causa: `EXECUTIONS_DATA_MAX_AGE=7` dentro del `composeFile` del stack (no en el Environment del
panel, donde no había ninguna `EXECUTIONS_*`). La variable va en **horas**, no en días: quien la
puso quiso decir 7 días y dejó 7 horas — solo se retenía lo del propio día. Corregido a `336`
(14 días, default oficial) + `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`, aplicado por la API de
Dokploy y desplegado (corte real de 13 s, 10:06:05→10:06:18 UTC, los 10 workflows activos
volvieron íntegros). Backup: `cz-compose-n8n-pre-retencion-20260729-1203.yml`. Ver
[[n8n-executions-data-max-age-va-en-horas-no-en-dias]].

### Bots del Digital Pipeline de Kommo (29-jul) — VERIFICADO en la GUI

Los 8 bots, con sus lanzamientos históricos: `Enviar Respuesta Bot` 350 · `Confirmacion cita` 104
(trigger etapa pENDIENTE DE ASIGNAR, plantilla *Confirmación Cita*) · `especilista asignado` 17
(trigger etapa) · `Formulario web` 10 (trigger etapa) · `vALORACION SERVICIO` 3 ·
**`Recordatorio 24 horas antes` 0** · **`recordatorios 4 horas antes` 0** · `NPS Bot` 0. Los dos
de recordatorio nunca se habían ejecutado: confirmación en el propio Kommo del bug del
`entity_type`. Ambos bien montados (sin disparador propio, los lanza n8n; plantilla correcta;
rama de error) — nada que tocar en los bots. Las 6 plantillas WABA están Aprobadas (WABA ID
`2697891833940384`); 5 en Marketing y `Doctor Asignado` en Utility.

**Decisión (Manuel, 29-jul): NO recategorizar a Utility.** `Confirmacion cita` entrega con 94%
sobre 104 envíos y es Meta quien fija la categoría (recategoriza sola si cree que está mal). El
ahorro a este volumen es de céntimos y en contra pesa más: editar una plantilla WABA la manda de
vuelta a revisión de Meta, y a esta cuenta ya le rechazaron plantillas el 21-jul. No tocar lo que
entrega.

### Pase de tono chat+voz + fix link Google Maps (04-ago)

**Tono menos formal** en chat (`u0AQPe9pxN79dbFa`, en vivo) y voz (Retell, v66 publicada), por
iteraciones sucesivas de Manuel sobre ejemplos concretos:
- Saludo: "¿en qué te ayudo?" → "¿cómo te podemos ayudar?" (voz de equipo, no individual).
- Nombre: "¿Con quién tengo el gusto?" (voz) / "¿Cómo te llamas?" (chat, ya suavizado de "¿A
  nombre de quién?") → unificado en ambos canales a "¿Nos dices tu nombre, por favor?".
- Cierre sin reserva (chat): "Estupendo, que tengas buen día" → "Genial, que vaya bien" →
  "Genial, muchas gracias, nos vemos pronto" (versión final, más cálida).
- Repetición de teléfono (voz): "Pues a ver, es el..." → "Te repito, es el:" → "Te repito el
  número para confirmar:" (versión final, v67 **draft sin publicar**, pendiente OK de Manuel).
- Consentimiento GDPR (voz): "Antes de continuar, ¿me das tu consentimiento..." → "Antes de
  seguir, ¿me dejas guardar tus datos para poder enviarte la confirmación?".

Cada iteración: GET del draft/workflow actual → `assert count==N` sobre el anchor exacto →
replace → PUT/PATCH → re-GET y verificar. Posiciones de nodos n8n verificadas sin drift en cada
PUT. Retell: v65→v66 publicada (2 rondas), v67 patcheada pero sin publicar (última ronda,
esperando confirmación).

**Fix link roto de Google Maps** — `maps.app.goo.gl/XJ9pnc8qG6Tuqpi89` (Firebase Dynamic Links,
apagado ago-2025) rompía la vista previa en WhatsApp aunque resolviera bien en navegador (302→200
comprobado con `curl`). Sustituido por `https://www.google.com/maps/search/?api=1&query=40.5066687,-3.8926916`
en los 3 workflows con la plantilla HTML del link: `qBUnBCRxKJEOJGFv`, `RN0wl8RaRmwLpnfQ`,
`13Roz21TOBwy8gp8`. Detalle transversal → [[maps-app-goo-gl-firebase-dynamic-links-rompe-preview-whatsapp]].
**El mismo link roto vive también en un Salesbot/plantilla de Kommo** (fuera de n8n, no tocable
por API) — el mensaje de WhatsApp que lo destapó viene de ahí, pendiente que Manuel lo cambie en
la UI de Kommo.

Credenciales usadas: vault 1Password `Clinica Zen` → item `n8n clinica zen` (campo `Api N8N
Manu`) y `Retell API`. Gotcha de sesión: el system prompt del `AI Agent` vive en
`parameters.options.systemMessage`, no en `parameters.text` (`text` es una expresión corta de
176 chars que solo compone `[DATOS_PACIENTE]`) — ya documentado en
[[leer-system-prompt-y-tools-actuales-antes-de-modificar-ai-agent]].

### Paginalia y entrega de correo (29-jul) — diagnóstico corregido

*Diagnóstico inicial erróneo*: "Paginalia no entrega el correo saliente". El rebote de la sonda SÍ
llegó — a la carpeta Spam del buzón, 7 min después del envío; se buscó a los 2 min y solo en
INBOX. Gmail respondió `550-5.1.1 ... does not exist`, o sea la salida externa funciona. No hay
nada que reclamar a Paginalia.

**Causa real: reputación.** Cabeceras de un envío propio: `dmarc=pass (p=QUARANTINE)`, `dkim=pass
header.d=clinicazen.es` (firma con selector `default`), `spf=pass`. Autenticación impecable —
Google los aparca en Spam porque `clinicazen.es` casi no envía correo, sale por IP compartida de
un hosting pequeño y escribe a buzones sin historial previo. Las 3 pruebas seguidas con asunto
`[TEST]` y sin texto plano tampoco ayudaron.

**Mitigaciones**: (1) remitente permitido en Workspace (Admin → Apps → Gmail → Spam) para el
correo interno de AgentesIA; (2) para emails a PACIENTES (Gmail/Hotmail), proveedor transaccional
con reputación propia (Resend/Brevo/SES) autenticando `clinicazen.es` — es lo estándar y no
depende del VPS compartido.

**Impacto real acotado**: el aviso interno de la reserva por voz va a `citas@clinicazen.es`, que
es entrega local en el mismo servidor (probado: 4 s) — no pasa por Google ni por filtro de spam.
La clínica sí recibe sus avisos.

### Reenganche disparando sobre conversaciones ya cerradas (04-ago)

Reportado por Manuel vía WhatsApp real: reservó cita, se despidió ("Gracias!" → "A ti. Que
tengas buen día, Manu."), y 70 min después `bfc4dWuztZsWfb4Q` le escribió "¿Sigues por ahí? Si
tienes alguna pregunta o necesitas algo más, aquí estoy." como si hubiera abandonado la conversación.

**Causa**: la query de `Buscar Conversaciones Abandonadas` solo miraba que el último mensaje de la
sesión fuera de tipo `ai` y que hubieran pasado 60min–24h. Esa condición es un falso positivo
estructural — TODA conversación bien cerrada también termina con el bot hablando último (la
despedida) y luego silencio; es indistinguible de un abandono real sin mirar el contenido.

**Fix**: la query ahora arrastra también el último mensaje del paciente (`msg_type = 'human'`) vía
un `DISTINCT ON` y excluye la sesión si ese mensaje es un cierre corto reconocible (regex anclado
`^(gracias|vale gracias|adiós|nada más|...)\W*$`). Si el bot se quedó esperando un dato real
(nombre, hora, confirmación) el reenganche sigue disparando igual — solo se corrige el caso de
"el paciente ya se despidió". No toca el nodo del AI Agent ni añade estado nuevo, solo la
condición SQL. Backup: `reenganche-pre-fix-farewell-20260804-1237.json`. Verificado: posiciones
de nodos sin drift tras el PUT. Pendiente confirmar en la ejecución de después (~11:00 UTC) que
corre sin error de sintaxis SQL — no se pudo probar contra la base directamente (self-hosted, sin
dominio público). Learning transversal →
[[reenganche-por-ultimo-mensaje-del-bot-dispara-tambien-en-conversaciones-bien-cerradas]].

### Segunda ronda de correcciones al prompt de voz (05-ago)

Dos correcciones más sobre el mismo prompt de Retell, pedidas por Manuel tras revisar el draft:

**1. "Europolis" seguía sonando pese al fix del 28-jul.** La causa: el fix de julio cambió las 3
frases YA GUIONADAS (confirmación de cita, "¿Dónde están?", cierre) a "frente al edificio de
correos de la dehesa de Navalcarbón", pero dejó intacto el dato crudo en el bloque de contexto:

```
- **Dirección**: C/ Castillo de Atienza, 1 bis, 28232 Las Rozas de Madrid (Pol. Europolis)
```

Cuando el paciente preguntaba algo que no calzaba exactamente con ninguna de las 3 frases
guionadas, el modelo improvisaba leyendo ese dato tal cual, paréntesis incluido — de ahí que
reincidiera el 2-ago en una llamada real ("Estamos en la calle Castillo de Atienza, uno bis, en
el Polígono Européolis de Las Rozas"). Fix: anclar la instrucción de pronunciación EN LA MISMA
LÍNEA del dato:

```
- **Dirección** (di SIEMPRE "frente al edificio de correos en la dehesa de Navalcarbón"; NUNCA
  menciones "Europolis" ni "polígono"): C/ Castillo de Atienza, 1 bis, 28232 Las Rozas de Madrid
```

De paso se corrigió la preposición en las 4 apariciones de la frase guionada: "de la dehesa" →
"en la dehesa" (petición explícita de Manuel). Learning transversal (aplica a cualquier AI Agent
con bloque de datos separado del guion) →
[[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]].

**2. El agente ofrecía "medicina estética" de forma proactiva.** La pregunta de apertura cuando no
se sabía el servicio era "¿Vienes por odontología, estética facial, o por algo concreto?" — Manuel
pidió que solo se mencione si el paciente la pide explícitamente o pregunta por los servicios en
general. Cambiado en ambos canales:

- Voz (Retell): `"¿Vienes por odontología, estética facial, o por algo concreto?"` →
  `"¿Qué tratamiento tienes en mente?"` + regla explícita de no nombrar "estética facial"/"medicina
  estética" salvo petición directa o pregunta general de servicios. También se quitó la línea
  redundante `Solo pregunta "¿es dental o estética?" cuando realmente no quede claro.` que repetía
  el mismo patrón proactivo.
- Chat (n8n, `u0AQPe9pxN79dbFa`): `"¿Es por tema dental o medicina estética?"` → `"¿Qué tratamiento
  tienes en mente?"` con la misma regla añadida inline.

Ambos canales verificados sin drift de posición tras el PUT/PATCH. Voz: draft v67 (que ya llevaba
la frase de repetición de teléfono de la ronda anterior) → publicado con estos dos fixes añadidos
en la misma versión. Chat: aplicado directo, en vivo.

## Cerrados en julio, sacados del hub el 20-ago

- **n8n solo retenía las ejecuciones del día** — RESUELTO 29-jul: `EXECUTIONS_DATA_MAX_AGE` iba en horas, no en días; a `336` (14 días).
- **Bots del Digital Pipeline sin verificar en la GUI** — VERIFICADO 29-jul: los 8 bien montados, nada que tocar.

### Sacado del hub el 2026-09-03

#### El número servía la v54: 3 meses de fixes que nunca llegaron (20-ago-2026)

`+34919934582` estaba **fijado** a `agent_version: 54` con la v67 publicada, así que publicar no cambiaba
nada: **28 llamadas reales** con el prompt de mayo, la última el 14-ago. Eso explica el pendiente que este
hub arrastraba desde el 3-ago — el fix del nombre inventado y el de «Európolis» **estaban escritos en la
v67** y verificados en el diff; no era el modelo ni el Code node, no llegaba.

Arreglado: inbound y outbound a `latest_published` (diff de las 9 versiones revisado antes; nada
peligroso). Con la v67 entran además: teléfono de clínica **629 494 209** separado del WhatsApp (919 934
582), web `clinicazen.es`, no ofrecer «estética facial» de forma proactiva y guion de *warm transfer*.
Backup de la v54 en `knowledge/projects/agentesia/n8n-backups/clinica-zen/` (Retell solo retiene 10
versiones y ya se había caído de la lista).

**A vigilar**: que la reserva llegue con nombre real a la agenda y que no diga «Európolis».
Ver [[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]]

#### Verificación por API del 2026-08-03 (read-only, sin tocar nada)

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
- ~~**La dirección vieja se sigue diciendo.**~~ **RESUELTO 05-ago**: el fix del 28-jul dejó `Pol.
  Europolis` en el bloque de datos "por considerarlo no hablado" — se hablaba igual al improvisar.
  Ver [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]].
- **Volumen real, para calibrar**: el agente de voz lleva **50 llamadas en total desde mayo**, y las de
  julio/agosto son casi todas desde el móvil de Gonzalo (`+34609779229`) o el de Manu (`+34617314938`).
  Sin tráfico de pacientes no hay forma de que un fallo aflore solo: por eso hace falta el check de
  efecto, no esperar a que salte algo.
