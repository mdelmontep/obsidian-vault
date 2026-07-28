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
| `PJBMjLLE0vNJjZH8` | Recordatorios | 24h/4h, cada 30 min, desde Google Calendar |
| `bfc4dWuztZsWfb4Q` | Reenganche Conversaciones Abandonadas | cron 30 min |
| `qBUnBCRxKJEOJGFv` | Especilista Asignado | webhook Kommo `status_lead` 104115983 |
| `13Roz21TOBwy8gp8` | Formulario Pagina web | lead + email |
| `15bh3GWag2IgwLe8` | Derivacion Humano | |
| `s3q2LceTDBvohSIx` | Buscar_base_de_datos | RAG Supabase |
| `FMotimghgUBzEgdm` | Error Handler | `errorWorkflow` de los demás |

Apagados: `wt5vmFCoSEEcYF3O` tmp_test_email_cz · `jp6lfAANQYvi2MbS` TEMP_test_leads_entrantes_v2 · `sIjznBan8THkEbcx` meter info rag · `5ecU1EI4DSs0SPWT` Chabot Laserys (ajeno, borrable).

**Retell** — agente `agent_350620f6b3044226efaeba9111`, LLM `llm_271c1594207dffae30974c56b5e6`, **v63 publicada** (28-jul). Voz `custom_voice_c3e5212df87e5341a06ad66e66` (eleven_flash_v2_5, es-ES), `ambient_sound: call-center`, `voice_speed 1.05`, `volume 0.84`. Entra por `+34919934582`. Tools: `Mirar_disponibilidad`, `Reservar`, `Cancelar_cita`, `end_call`, `transfer_call`.

**Salud**: 1 sola ejecución con error en todo el histórico retenido — la de recordatorios de hoy (ver hitos). El resto en verde.

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
- **`WA Confirmación Cita A/B` estaban huérfanos** (0 conexiones) — el agente prometía WhatsApp y no salía nada. Conectados a `Create an event Voz`/`Voz2`.

Backup pre-cambio: `cz-pre-email-voz-20260728-1227.json` (scratchpad de sesión, mover a repo).

## Próximos hitos

1. **Smoke de la reserva por voz (NEXT, bloquea el resto)** — `POST /Reservar_crm` crea contacto+lead reales en Kommo, evento en Calendar y manda correo. Requiere OK y limpieza posterior. Verifica: email interno llega a `citas@clinicazen.es`, WhatsApp del salesbot llega al paciente, cita correcta.
2. **`salesbot/run` devuelve 400 y se pierde el recordatorio (NEXT)** — hoy 06:30, lead 32984916, `bot_id 63810`, `Some parameters incorrect`. Dos cosas distintas que arreglar:
   - *Por qué falla*: sospecha = el lead no tiene chat de WhatsApp vinculado (paciente que entró por teléfono). Afecta igual al `bot_id 63814` recién conectado en la reserva por voz.
   - *Por qué no se reintenta*: `Filtrar y evitar duplicados` marca `staticData.enviados[clave]` **antes** de enviar. Si el envío falla, queda como enviado para siempre y el paciente se queda sin recordatorio en silencio. Marcar después del envío OK.
3. **Verificar el RAG de Supabase (NEXT)** — es el único corpus que no he podido revisar (self-hosted sin dominio público). Puede seguir teniendo "Europolis" o la dirección vieja. Se comprueba preguntando "¿dónde estáis?" al bot por WhatsApp.
4. **`emiafd@agentesia.madrid` hardcodeado (LATER)** — en `Especilista Asignado`, `toEmail` = `{{ email }}, emiafd@agentesia.madrid`. Buzón de la agencia recibiendo datos de pacientes en producción. Quitar.
5. **Tres teléfonos distintos (LATER)** — prompt dice llamadas `629 494 209` y WhatsApp `919 934 582`; la KB dice `91 993 35 69`; las llamadas entran por `919 934 582`. Decidir cuál es cuál y unificar prompt + KB.
6. **Nitidez de audio (LATER, si Gonzalo insiste)** — medido sobre la grabación: agente −19,8 dBFS, 0 muestras saturadas; el que se oye 5 dB más bajo es el llamante. Candidata real = `ambient_sound: call-center`, que se mezcla después de la grabación y por eso no se oye al escuchar el WAV. Latencia e2e p50 2,35 s / p90 3,35 s también pesa. Prueba: quitar el ambient y llamar.
7. **Sin repo local (LATER)** — `~/Projects/clinica-zen` está vacío. Cero backup de los 14 workflows. Exportarlos y versionarlos.

## Bloqueos / esperando a terceros

Ninguno. El de mayo (ID del status "Cita cancelada") era obsoleto.

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
