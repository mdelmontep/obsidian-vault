---
title: Centro Elphis — HUB
date: 2026-05-18
source: investigación + onboarding firmado + discovery Clientify + propuesta enviada
tags: [cliente, agentesia, elphis, voz, whatsapp, retell, clientify, doctoralia, n8n, dokploy]
---

# Centro Elphis · HUB

Centro privado de tratamiento de adicciones en Madrid. Cliente Agentesia: paquete avanzado (voz Retell + chatbot WhatsApp + Clientify).

## Estado actual · 2026-08-12

- **Auditoría completa del bot. Todo lo encontrado, cerrado salvo el canal de voz.**
  - ✅ **`chatwoot-event` ya no falla** (era el 🔴 desde el 3-ago, 55 errores en 14 días): `queryReplacement` mandaba el TEXTO `"null"` y `$3::bigint` cascaba antes del `COALESCE`. Fix `NULLIF(NULLIF($N,'null'),'')`, probado con `BEGIN/ROLLBACK` contra la BD (rojo con la vieja, verde con la nueva). **Impacto real mucho menor del que decía la ficha**: 54 de 55 respondieron al paciente y liberaron el lock — reventaba en el último nodo, solo perdía persistir ids. Limpiadas 5 filas con `'null'` literal en `conversation_state`. Ver [[una-expresion-que-evalua-a-null-viaja-como-el-texto-null]].
  - ✅ **Avisos de error a `#01-incidencias`** (bot `n8n_aia_bot`, dedup 60 min por workflow+nodo) y handler asociado a **28 de 28** workflows — antes estaba en 2. El montaje pasó nueve checks y **no avisaba**; se detectó leyendo el canal. Ver [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] · [[n8n-error-handler-global-via-errorworkflow]].
  - ✅ **Desactivados 4 webhooks vivos de la fase de pruebas**, uno peligroso: `purge-idem` era un `TRUNCATE` de `idempotency_log`+`slot_lock` **sin autenticación**. También los dos test-runners y `retell-tool-buscar-huecos`. Ver [[el-utillaje-de-pruebas-se-queda-encendido-en-produccion]].
  - ✅ Sanos: certificados hasta el **17-oct** (la nota decía agosto), env de avisos correcto en runtime, suscripción del webhook de Meta activa, disco al 32%.
  - 🔴 **ÚNICO CABO: el canal de voz.** `retell-post-call-webhook`, `retell-tool-reservar-visita` y `retell-tool-crear-lead` llevan 14 días a **cero ejecuciones**. O no ha entrado ninguna llamada, o el webhook de Retell no llega y se están perdiendo los leads de voz. Se cierra con `POST /v2/list-calls` filtrando por los tres `agent_id` de Elphis.
  - Los cuatro `agenda-*` siguen activos y sin uso desde el rediseño de junio: son sub-workflows (no exponen URL), se dejan por si vuelve la reserva desde el bot.

## Histórico

- **10-ago: los avisos internos de lead no llegaban al equipo, por dos causas.** (1) `ELPHIS_NOTIF_INGRESO`/`_RECEPCION` seguían con el móvil del dev porque «el número de la recepcionista» figuraba como pendiente… cuando **el de Alba llevaba en §Datos clave desde mayo**; ahora ambos en `+34687448210` y el email en `info@centroelphis.com`. (2) El `else` de `Decidir etapa` ponía `destino='none'` y ahí caían el default `'info'` y cualquier `tipo_consulta` inventado por el LLM: 65 de 73 ejecuciones sin avisar a nadie, todo en `success`; cambiado a `destino='recepcion'` sin tocar la etapa de Clientify. Verificado E2E (`wamid` de Meta + `250` del SMTP) y con tráfico real el 11-ago. Volumen: **13 personas en 14 días, pico de 4/día** — contar ejecuciones en vez de personas infla ×10. `notify-cita-confirmada-email` desactivado por huérfano. **Limpiar en Clientify**: contacto `170386983` / deal `31693026`. Ver [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]] · [[workflow-activo-no-significa-llamado-grep-su-id-antes-de-editarlo]].

- **04-ago: bot de chat contestando composición/efectos de sustancias (Alba: «el tussi lleva heroína») y sin avisar cuando alguien decía «ya tuve visita» — ambos corregidos en `router-ia`.** Sustancias: regla dura en el prompt, 4/4 en vivo contra la API real (prompt-only vale aquí porque no hay acción externa). «Contacto previo»: prompt-only NO garantizaba el aviso (0/3 y 1/2 llamando a `pause_bot`), así que se añadió nodo determinista `Contacto previo pre-check` (regex, patrón de `Crisis pre-check`) + rama a `registrar-lead`, 9/9 casos. Voz corregida igual (agente `Laura ... Flow v4` `agent_e21120298343bc2ef8b4a535c9`, flow `conversation_flow_a42bf76dcfa0`, número **`+34910054950`**), con el caveat de que Conversation Flow no admite capa determinista (transiciones `type: prompt`). Regex de «contacto previo» es primera pasada, revisar con volumen. Ver [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]].
- ⚠️ **La API key de Retell (compartida por TODA la agencia) se pegó en texto plano en un chat (04-ago)** porque el vault `Elphis` no tiene credencial de Retell, solo el login del dashboard. Otros clientes sí tienen item `Retell API` propio. Pendiente: decidir si rotar (afecta a todos los agentes de la agencia) y en cualquier caso guardar copia limpia en `Agentesia`/`Compartida Agentesia`.

- ~~🔴 `chatwoot-event` falla 1 de cada 5 ejecuciones (3-ago)~~ ✅ **CERRADO 12-ago** (ver Estado actual). Lo destapó el check de efecto ([[agentes-cliente-tres-capas]]), no el error handler — que existía, activo, y estaba asociado a 2 workflows de 25, así que sus 55 errores no llegaron a nadie durante 13 días.
- **23-jul: agente de chat "Laura" dado de alta en el portal AgentesIA (`clientes.agentesia.madrid`), visible para Alba** — WhatsApp, 659 877 708, workflow `chatwoot-event`, modelo `gpt-4o-mini`. Verificado vía Graph API (no memoria) que el 659 está ya en producción real para chat: `subscribed_apps` + `callback_url` de la app "Centro Elphis" apuntan al mismo endpoint n8n (`/webhook/wa-inbound`) que procesa el chat — corrige un supuesto viejo de que seguía sobre el número de pruebas Agentesia (`+34 910 05 49 50`, ahora legacy/solo pruebas internas).
- **HMAC del webhook `wa-inbound-bridge` CONFIRMADO activo** (no solo presente en el código): nodo `Validate HMAC Meta` valida `x-hub-signature-256` contra HMAC-SHA256(rawBody, `META_APP_SECRET`), y `META_APP_SECRET` está seteado en el compose real de Dokploy → el pass-through de "secret no seteado" nunca se activa. Sigue pendiente solo **rotar** ese secret (expuesto en captura 2026-07-21), no volver a habilitarlo. Ver [[webhook-hmac-pass-through-verificar-env-real-no-solo-codigo]].
- **22-jul: notificaciones internas (WA+email) arregladas en `registrar-lead` + `router-ia`, desplegado y verificado con ejecuciones reales.** Alba reportó un lead pidiendo callback sin aviso. Causa real: el guard anti-doble-deal (`idempotency_log`, 30 días) cortaba TODA la notificación, no solo el deal duplicado; y `should_notify` dependía de que el deal fuera nuevo (`was_created`), así que la rama "deal ya existe" tampoco avisaba nunca. Fix: `should_notify` ya no depende de `was_created`; dedup fino nuevo de 60min (`Check notif dedup`) separado del guard de 30 días del deal. `pause_bot` (handoff a humano en chat) antes no notificaba nada — ahora dispara `registrar-lead` en paralelo. Voz ya quedaba cubierta sin tocar nada (mismo sub-workflow vía `retell-tool-crear-lead` + registro post-call determinista). Ver [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]].
  - **Confirmado**: `ELPHIS_NOTIF_EMAIL=info@centroelphis.com` en el env real de Dokploy (verificado por SSH, `docker exec printenv` acotado a esa var) — las notificaciones por email SÍ llegan al buzón real del cliente.
  - **Pendiente**: probar `pause_bot` con un mensaje real de WhatsApp (solo se verificó el wiring + `registrar-lead` vía webhook directo); **limpiar 3 emails de prueba en `info@centroelphis.com`** (asuntos `[Bot Elphis] RECEPCION: Test Uno/Dos...`, 22-jul) — pendiente decidir con Alba o acceso IMAP; limpiar 2 leads de test en Clientify prod (`deal 31183504`/`31183588`, phones `+34600000001/002` — no se pudo marcar "lost" vía API, schema de status/pipeline_stage no aceptó los valores probados).
- **Bug conocido, sin arreglar (22-jul, decisión explícita de dejarlo así):** `clientify-upsert-contact` matchea contacto **solo por teléfono** y sobreescribe `first_name`/`last_name` sin comprobar si sigue siendo la misma persona (los emails, en cambio, solo se suman, nunca se pisan — por eso el síntoma es nombre nuevo + email viejo conviviendo). Confirmado en 2 contactos reales: uno donde `chatwoot-event` renombró a un contacto tras una conversación posterior desde el mismo teléfono, y otro donde `doctoralia-email-sync` mezcló dos reservas de personas distintas (Sophia Olivella Sánchez → José Miguel Zabala Monsalve) que compartían número de teléfono — encaja con que ~50% de contactos son familiares reservando por el paciente. Causa raíz: teléfono como identity key sin verificación de identidad. Si se retoma, tocar `Build PATCH body` en `arlyptFsEBJD7Owl`. Ver [[telefono-como-identity-key-en-upsert-crm-colisiona-si-se-comparte]] (patrón aplica a otros clientes con upsert-por-teléfono).
- **Idioma del bot de chat corregido (22-jul)**: Alba reportó que el bot dijo que no había terapia en inglés (sí la hay, solo terapia individual, no francés). Prompt de `router-ia` ahora responde en inglés si el usuario escribe en inglés (fallback español para el resto) y sabe que la terapia individual sí se ofrece en inglés.
- **Bot WhatsApp real VIVO** en 659 (Cloud API). 2026-07-21: **corregidos 4 fallos reportados por Alba en `chatwoot-event` + `book-and-notify` (desplegados y verificados E2E)**:
  - **Lock del orquestador liberado tras responder** (antes se retenía 15s por la extracción CRM → el 2º mensaje se descartaba = bot mudo tras dar el nombre + nombre vacío en Clientify + "Timed out" en Chatwoot) + reintento en `locked_busy`. Ver [[lock-conversacion-liberar-tras-responder-no-tras-trabajo-post]].
  - **Enlace primera visita por canal**: chat → texto libre **vía Chatwoot** (visible en bandeja + reenvío a WA por `send_to_meta`); voz → **plantilla `elphis_cita_link`** (fuera de ventana 24h). Ver [[whatsapp-fuera-ventana-24h-requiere-plantilla-hsm]].
  - **Retraso de 90 min (19-jul) diagnosticado: fue de Meta**, no del stack (n8n "Up 3 days", Traefik "Up 2 months"; diagnóstico vía API Dokploy sin SSH → [[dokploy-api-docker-getcontainers-estado-sin-ssh]]).
- **3 plantillas HSM APROBADAS** (WABA `3949824101978503`): `elphis_notif_interna` (`1003760889245568`), `elphis_recordatorio_24h` (`1052157190679924`), `elphis_cita_link` (`2263122474525415`, MARKETING). Token Meta en `op://Elphis/whatsapp elphis token EAA/credential`.
- **Monitor del portal**: servidor Elphis dado de alta en `/agency/infrastructure` ("En línea"). Acceso SSH al host resuelto (puerto 5251; pw root en op "ssh dokploy"; clave `dokploy_portal_monitor` + m.delmonte autorizadas). API Dokploy en `op://Employee/dokploy API Elphis/credential`.
- IDs WABA/credenciales en memory [[elphis-wa-cloud-api-migracion]]. Prompt afinado (17-jul): "nuestro director", paciente/familiar, `**`→`*`, reutiliza contexto. Chatwoot: 2 cuentas recepción admin.
- **Pendientes go-live:** (1) **rotar clave RSA `dokploy` + API key Dokploy** (expuestas en chat 2026-07-21), `META_APP_SECRET` `723c1d…` y `POSTGRES_AUX_PASSWORD` (reexpuesta 10-ago); (2) DPAs Enrique, sesión 30min crisis; ~~número directo recepcionista~~ ✅ **cerrado 10-ago: es el `+34687448210` de Alba, ya en §Datos clave**; (3) migrar GCal de pruebas al de Enrique. Ver [[bloqueantes-elphis]].

## Datos clave del cliente

- Web: https://centroelphis.com
- Sede: C/ O'Donnell 32, Bajo C, 28009 Madrid
- Teléfono público: **659 877 708** (mismo voz y WhatsApp)
- Doctoralia: https://www.doctoralia.es/clinicas/centro-elphis (52 reseñas, 5.0)
- Instagram: @centroelphis
- Razón social: KISAMU S.L., CIF B88269022, reg. sanitario CS16658
- Director y firmante: **Enrique Sanz** («Kike» en Clientify)
- Contacto operativo: **Alba Orgaz**, +34 687 448 210, alba.orgaz@centroelphis.com
- AgentesIA owner: **Borja Chivite**, bgchivite@agentesia.madrid

## Conversión y audiencia

- Conversión clave: agendar **primera visita informativa gratuita** (30 min, con Enrique Sanz).
- ~50% de quien contacta es un familiar, no el paciente. El bot pregunta pronto: «¿La consulta es para ti, o para un familiar o conocido?».

## Documentos del proyecto

- [[contexto-cliente-elphis]] · perfil, tono, audiencia, datos para personalizar el bot
- [[arquitectura-elphis]] · stack completo, diagrama lógico, SoT por entidad, riesgos
- [[clientify-discovery-elphis]] · auditoría del CRM existente: pipeline IDs, users, limitaciones técnicas
- [[propuesta-pdf-elphis]] · entregable PDF para Borja y Dani, identidad visual, polish aplicado
- [[protocolo-crisis-elphis]] · Teléfono de la Esperanza como derivación principal, triggers, sesgos
- [[bloqueantes-elphis]] · estado completo: resueltos, bloqueante real, pendientes Alba, pendientes Enrique
- [[dpas-rgpd]] · DPAs pendientes con Retell, OpenAI, Meta (parking hasta cerca del go-live)
- [[ADR-001-doctoralia-google-calendar]] · decisión arquitectónica: GCal como puente, no API Doctoralia

## Stack en una línea

Clientify (CRM) · Chatwoot self-hosted (inbox + handoff) · Meta Cloud API (WhatsApp) · Retell + ElevenLabs castellano (voz) · n8n + Supabase dedicados en Dokploy actual · Google Calendar de Enrique como puente con Doctoralia.

## Protocolo de crisis · resumen

Ideación suicida → transferencia directa al **Teléfono de la Esperanza (717 003 717)**. WhatsApp: plantilla `elphis_aviso_crisis` reproduciendo el texto firmado del onboarding (717, 024, 112, urgencias). Ver [[protocolo-crisis-elphis]] para detalle.

## Plan de fases

0. Infra Dokploy (stacks `n8n-elphis`, `supabase-elphis`, cuenta Chatwoot Elphis).
1. agenda-service sobre Google Calendar.
2. clientify-service (upsert por phone E.164).
3. Chatbot WhatsApp MVP con número de pruebas Agentesia.
4. Agente de voz Laura (Retell + tools + post-call webhook + transfer Teléfono de la Esperanza).
5. Sync inverso, recordatorios, formulario web.
6. Hardening, DPAs firmados, validación Enrique, migración al 659 877 708 real.

Estimación: 3-4 semanas entre arranque y go-live.

## Relacionado

- [[clinica-zen]] · patrón replicable previo (Retell + Kommo + n8n). Aquí cambia el CRM y se añade Chatwoot.
- [[agentesia]] · agencia.
