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
