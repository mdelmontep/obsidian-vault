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

