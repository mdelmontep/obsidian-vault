---
title: EcoBox HUB
date: 2026-05-26
updated: 2026-09-17
tags: [cliente, ecobox, hub]
---

# EcoBox 360 — HUB

Cliente AgentesIA · Taller de chapa y pintura + mecánica rápida · Las Rozas (Madrid). Onboarding 2026-05-20, despliegue 21-22, voz E2E funcional 2026-05-25, **chat WhatsApp E2E real funcional 2026-06-01**.

**Estimación de horas** (2026-08-04, retroactiva, sin time-tracking — método en [[estimar-horas-retroactivas-sin-time-tracking-cruzar-git-y-hub-cliente]]): web ~5-6h (autor `notcapi`, vía git log del repo `ecobox`) · automatización n8n/Retell/WhatsApp/Chatwoot/GCal ~24-32h (Manuel, estimado por densidad del hub + 3 ADRs del 22-may). Total proyecto ~29-38h, 20-may a 2-jun.

## ▶︎ EMPEZAR AQUÍ (17-sep-2026)

Estado tras la sesión del 17-sep (detalle abajo). Voz **v25** publicada y el número sirve
`latest_published`; **ninguna llamada real la ha estrenado todavía**.

0. **Limpiar Calendar:** las pruebas del 16/17-sep dejaron 4 citas REALES el 17-sep —
   «Peritaje — Reservar_cita — 3254JBC» (12:00 Rozas, la del bug), «Agentesia Proba» (11:30 Rozas),
   «Manuel del mundo» (11:00 Rozas) y «Manu 🥦» (11:00 Majadahonda).
1. **Pruebas reales pendientes (humano):**
   - Llamar al +34910054813 desde un móvil que NO sea el 617314938, **con ruido de fondo a
     propósito**, y pedir "hablar con una persona" → debe sonar el 617314938 mostrando el
     910054813, y Alex no debe cortarse con el ruido (v24: `noise-cancellation`, interrupción 0.3).
     Si aún corta, el siguiente paso es `ambient_sound: null`, NO bajar más la sensibilidad.
     **En esa misma llamada, Alex debe pedirte nombre y apellido justo después del taller** (v25).
   - WhatsApp: reserva completa de punta a punta para confirmar que ahora pide nombre real y email
     y que el correo de confirmación llega. **Ya no hay modo test: toda prueba crea cita real.**
2. **Handoff:** Cristian ya tiene cuenta en Chatwoot (ver sesión tarde). Hasta hoy ninguna de las 16
   conversaciones reales tenía un mensaje de un humano. Falta el email de recepción para su cuenta, y
   cambiar el `assignee_id: 1` fijo del nodo "Assign a Ecobox" por reparto real. Horario del inbox
   definido L-V 9-17 pero `working_hours_enabled:false`.
3. **Que Cristian cierre lo suyo:** antelación mínima para cancelar (guard escrito y sin aplicar),
   Bloque 0 (operadora, destino real de la transferencia, si Alex cierra valoraciones), y datos de
   negocio contradictorios: Mutua (KB compatible, flow deriva siempre), Aval fuera de la lista de
   aseguradoras, eléctricos (web sí, KB no), recogida «sin coste en el noroeste», sustitución gratis
   para seguros/renting, mecánica sin cita.
4. **Dudas abiertas:** el nodo "Email a Cristian" de `Reservar_cita` escribe a m.delmonte.p@, no a
   Cristian. Mensajes `[PRUEBA - borrar]` en el Slack de incidencias (C0ASNEXM2N4) sin borrar.
   Simulaciones: con todos los datos de golpe se salta deletreo y resumen; «el jueves que viene» dio
   dos fechas distintas en dos pruebas.
5. **agency-portal** descarta `custom_analysis_data` de Retell (los 12 campos de EcoBox) en
   `src/lib/fleet/channels/retell/adapter.ts` y no avisa de transferencias fallidas.

## Sesión 2026-09-17 — el nombre: dos notas correctas del vault que se componen en un bug

- **La cita de las 12:00 del 17-sep se tituló «Peritaje — Reservar_cita — 3254JBC — choque».** No fue
  el fallback `'Cliente'`: el cuerpo de Retell tiene tres claves —`args`, `call` y `name`— y ese
  `name` de primer nivel **es el nombre de la tool**. Con `args.name` vacío,
  `args?.name || body?.name || 'Cliente'` se quedó con `"Reservar_cita"` y nunca llegó al default.
  Evidencia: llamada `call_2d5689afe3f5b582bf0ae8afe17` (v24, `user_name: ""`, dos invocaciones con
  `"name": ""`) y ejecución 5960.
- **Por qué Alex no lo preguntaba:** el prompt decía «1. Nombre completo (si no lo tienes ya en
  `user_name`)», y `user_name` solo lo rellena `n-extract-1` si el cliente lo suelta por su cuenta;
  encima la cláusula ORDEN lo mandaba explícitamente detrás de seguro, grúa y taller.
- **La puerta de validación era código muerto.** `Validate input` exige `name notEmpty`, pero
  `Edit Fields` rellenaba el campo antes, así que esa condición no podía disparar desde que existe.
  Mismo anti-patrón que [[normalizar-en-un-nodo-intermedio-no-protege-a-quien-relee-el-de-entrada]]
  visto del otro lado: no es quién relee la entrada, es que la entrada pone un default.
- **El arreglo NO podía ser quitar `|| body.name`**: el chat postea el cuerpo PLANO (la tool
  `reservar_cita` del bot usa `specifyBody: keypair`) y esa rama es la que ha creado todas las citas
  buenas de WhatsApp. Se discrimina por forma:
  `(($json.body?.args ? $json.body.args.name : $json.body?.name) || '').toString().trim()`.
- **Voz v25 publicada:** nombre y apellido obligatorios y explícitos, colocados en la cláusula ORDEN
  justo tras el taller; prohibido llamar `Reservar_cita` con `name` vacío; manejo del motivo
  `missing_data`; y la descripción del argumento `name` de la tool deja de ser «Nombre completo del
  cliente». Número verificado sirviendo `latest_published`.
- **Lo que enseña del vault:** las dos piezas llevaban meses escritas —
  [[n8n-edit-fields-optional-chaining-body-args-plano-vs-wrapped]] (1-jun) prescribe justo la cadena
  `args?.X || body?.X`, y [[retell-custom-tools-comparten-webhook-y-se-rutar-por-body-name]] (18-abr)
  dice que Retell enruta por `body.name`. Cada una es correcta; juntas producen el bug. La del 1-jun
  ya lleva escrita la excepción.
- **Sigue pendiente de seguridad:** el `X-Ecobox-Token` volvió a aparecer en consola (vive en claro
  en la definición de la tool del flow). Rotarlo junto al HMAC de Chatwoot.

## Sesión 2026-09-16 — el bug del debounce, email del cliente, fuera modo test, voz v24

- **El fallo que hacía repreguntar datos ya dados no era la memoria, era el consumidor.** El AI Agent
  leía `$('Edit Fields').item.json.message`, que es el mensaje del ÚLTIMO webhook, no el buffer del
  debounce ya unido. Evidencia: ejecución 5899, `Redis Get buffer drain` = `["Choque trasero, seat
  leon", "Zzz0000"]`, `Join buffer into message` los unió bien, y al modelo le llegó solo `Zzz0000`
  (así quedó también en Postgres). Causa raíz: `Get labels` es un HTTP Request y reemplaza `$json`
  ([[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]]), así que el agente tiraba del
  nodo pre-buffer. Arreglado con `$if($('Join buffer into message').isExecuted, …, $('Edit
  Fields')…)` para no romper el camino `Fail-open sin debounce`. Siguiendo
  [[n8n-json-narrowed-rompe-nodos-lejanos-sin-error]] se auditaron TODOS los consumidores: el otro
  era `Build handoff email`, que mandaba a Cristian el texto recortado. Verificado en la ejecución
  5916: el modelo recibió `'Hola, quiero pedir cita\nChoque trasero, Seat León'`.
- **Prompt del chat:** prohibidas listas numeradas y viñetas (gpt-4.1 copiaba la estructura del
  checklist y soltaba parrafadas), un dato por turno, no repreguntar lo ya dicho. Nuevo paso 8b:
  prohibido llamar a `reservar_cita` en el mismo turno que `mirar_disponibilidad` — antes reservaba
  y DESPUÉS preguntaba "¿te confirmo?" (5903 + 5907, doble llamada; no duplicó evento solo porque
  la idempotencia `idem:reservar:tel:sede:fecha:matrícula` tiene TTL 900s). Verificado en 5930/5933.
- **Memoria limpiada:** 176 filas de `+34617314938` en `ecobox_chat_memory`, con 12 confirmaciones
  afirmadas por el modelo ANTES de existir la guardia ("te he reservado… 16:00 Las Rozas", cita que
  nunca existió). El agente lee 20 turnos, así que las arrastraba como contexto real. Backup en el
  scratchpad de la sesión. El resto de sesiones intactas.
- **`Email al cliente` no había funcionado NUNCA**, ni en chat ni en voz: enviaba a
  `{{ $json.email_cliente }}`, campo que no existía en ningún sitio → "No recipients defined" en
  todas las reservas, mudo por `onError: continueRegularOutput`. Ahora `Reservar_cita` recoge
  `email_cliente`, el chat lo pide una vez (opcional, la cita sale igual sin él) y una puerta
  `IF tiene email` evita el error cuando no hay correo.
- **Modo test eliminado** de `Reservar_cita` (único workflow que lo tenía, comprobado en los 12):
  la condición era `matricula == ZZZ0000`, que incumple el formato que el propio prompt exige
  (4 números + 3 consonantes), así que Alex la rechazaba y la "prueba" acababa creando una cita
  real — pasó el 16-sep con `0000ZZZ` (evento `ec2s2ht1d0tbkit710e9fni1k2krcc1r`, 17-sep 11:00
  Majadahonda, que el cliente decidió mantener).
- **El nombre ya no sale del perfil de WhatsApp.** El tag `[ctx]` trae el nombre de WhatsApp, que
  suele ser un apodo con emojis: el evento del 17-sep quedó como "Peritaje — Manu 🥦 — 0000ZZZ".
  El prompt ahora pregunta y confirma nombre y apellido reales antes de reservar.
- **Voz v24 publicada** (número sirve `latest_published`, verificado): saludo sin el aviso de
  grabación, `denoising_mode: no-denoise → noise-cancellation` y `interruption_sensitivity`
  0.4 → 0.3. La causa de que Alex se cortara con cualquier ruido era el `no-denoise`, no la
  sensibilidad. Sin tocar, pero fuera de la config canónica: `voice_temperature` 0.96 (canónico
  0.5) y `ambient_sound: call-center` (canónico null).
- **Decisión de grabación (Manuel, 16-sep):** se sigue grabando y el saludo ya no lo menciona. El
  matiz que la sostiene: la política de privacidad de la web YA declara que Retell guarda la
  grabación o la transcripción (`web/src/lib/legal.ts:612-615`), así que la divulgación existe por
  escrito; lo que se quitó es el aviso hablado.
- **Pendiente de seguridad:** en la sesión quedaron impresos en consola el secreto HMAC de Chatwoot
  y el `X-Ecobox-Token`. Rotar ambos y actualizar 1Password.
- El PUT a la API pública de n8n rechaza `settings.binaryMode` (`must NOT have additional
  properties`), pero al mandar solo la allowlist **n8n conserva el valor existente**: no se pierde.

## Sesión 2026-09-15 (tarde) — auth de webhooks, alertas solo Slack, voz v21, Chatwoot

- **Webhooks cerrados, token rotado.** `reservar_cita`, `buscar_reserva`, `cancelar_cita`,
  `mirar_disponibilidad`, `aviso_estado` → `headerAuth` con credencial n8n "Webhook EcoBox
  X-Ecobox-Token (rotado 2026-09-15)"; la vieja borrada. Token en 1Password EcoBox, ítem "Webhook n8n
  EcoBox — X-Ecobox-Token (rotado 2026-09-15)". Probado: sin cabecera 403, token viejo 403, nuevo 200.
  `chatwoot-bot-ecobox`: Code node "Auth Chatwoot" verifica `X-Chatwoot-Signature` (HMAC-SHA256 de
  `<timestamp>.<body>`, ventana 10 min, HMAC en JS puro porque el sandbox prohíbe `crypto`) con respaldo
  por `?t=`. `ecobox-logo` sigue público a propósito (PNG de los emails). Las versiones 12-19 del flow
  conservan el token viejo, ya revocado. Ver [[cerrar-un-webhook-exige-censar-todos-sus-emisores-no-solo-el-obvio]].
- **Segundo bug de cabeceras en los tools del bot:** sin `valueProvider` el default es `modelRequired`
  y el LLM rellenaba el token ("your_token"). Va `valueProvider:"fieldValue"` además de `parametersHeaders`.
- **Alertas técnicas solo a Agentesia y solo por Slack** (C0ASNEXM2N4, credencial "Slack EcoBox
  incidencias"). Error Handler sin email y con dedup Redis 30 min; `Meta token health check` (antes
  mandaba EMAIL A CRISTIAN) y `Calendario festivos` pasados a Slack con dedup 6 h / 24 h. Gotcha: el
  nodo Redis sustituye `$json` por `{clave: contador}`; el contexto se lee con `$('<nodo previo>')`.
  `TEST Email Templates` desactivado. `ASSET logo` no tiene `errorWorkflow`.
- **Voz v21 publicada** (la publicó Manuel; el clasificador bloqueó al agente). Saludo: «Hola, soy
  Alex, el asistente virtual de EcoBox. Te aviso de que la llamada se graba. ¿En qué te puedo ayudar
  hoy?» (grabación activa: `data_storage_setting: everything`). Arista `e-damage-to-date` exige seguro,
  rodando/grúa y taller; matrícula confirmada o 2 intentos → `PENDIENTE` (Reservar la acepta y el email
  al taller la marca "⚠ revisar"). KB: 4 fuentes reescritas en vivo (cancelar y estado no derivan,
  1 hueco, sin extras por iniciativa); 11 fuentes.
- **Chatwoot** `https://chatecobox.agentesialabs.com` (4.17.0, cuenta Ecobox360 id 1, inbox WhatsApp
  id 2). Creado `cristian@ecobox360.es` administrador + miembro del inbox; contraseña fijada desde Super
  Admin y verificada con login, en 1Password EcoBox "Chatwoot Ecobox — Cristian". El usuario del ítem
  "Chatwoot Ecobox" es SuperAdmin; el formulario de `/super_admin/sign_in` usa `super_admin[email]` /
  `super_admin[password]` (con `user[...]` da "Invalid credentials").

## Sesión 2026-09-15 — auditoría voz + chat y dos rondas de fixes (6 agentes + auditoría cruzada)

**Voz (Retell), publicada v19:**
- **El número servía el BORRADOR.** `inbound_agents` sin `agent_version` = sirve la última versión
  *incluido el draft*: el 3-jun una llamada corrió en v11, publicada el 26-ago. Contradice lo que decía
  la skill `n8n-surgical-edit` ("absent = latest published"). Fijado a `latest_published`.
- `{{from_number}}` fuera del flow: el teléfono lo pone n8n desde el canal. Buscar/Cancelar sin `phone`
  en el schema; Reservar/Aviso solo con número oculto. Adiós "¿con este número o con otro?".
- "(año 2026…)" fuera del `global_prompt`. Cancelar exige `sede`. Motivos nuevos en el prompt.
- **Transferencia Netelip 5/5 fallida:** SIP 500 porque Netelip no deja presentar como llamante un
  número ajeno. `show_transferee_as_caller: false` (Simarro y Elphis transfieren por el mismo trunk sin
  esa opción). El compañero ve el 910054813, no al cliente. Pendiente de prueba real.

**Tools n8n (contrato "teléfono del canal"):** `phone = N(body.call.from_number || body.channel_phone)`.
- Cancelar comprueba que el `Tel:` del evento es del canal (`no_es_tuya`); 404 ≠ error de Google.
- Reservar: lock `lock:<sede>:<fecha>` (INCR sin TTL + `Set lock TTL` solo al ganador, 3 reintentos de
  1,5 s), liberado en todas las ramas; idem con matrícula; Redis caído → `error_temporal`, nunca cita
  sin lock. **Ventana residual:** si Redis falla entre el INCR ganador y el SET TTL y también al liberar,
  la clave queda sin TTL y bloquea esa sede/día hasta borrarla a mano.
- **Buscar_reserva llevaba tiempo sin encontrar nada** (Google no casa `q=+34…`): ahora lista 180 días
  y compara `Tel:` normalizado. Los WhatsApp de confirmación de Netelip salían sin el 34: arreglado.
- **2027 NO ampliado:** a 15-sep no hay BOE, decreto CAM ni locales de Las Rozas/Majadahonda.
  `fuera_de_calendario` con motivo claro; el aviso de festivos salta a mediados de octubre.

**Chat (bot `lv7pee2XAU5OngOB`):**
- **Bug preexistente desde el 10-sep: los 4 tools del chat fallaban SIEMPRE** ("tool input did not match
  expected schema"). La cabecera se guardó en `headerParameters` y n8n 2.18.7 lee `parametersHeaders`
  en `toolHttpRequest` 1.1 → genera un parámetro requerido de nombre vacío. Movido. Sin impacto real:
  desde el 10-sep solo hubo actividad en la conversación de pruebas.
- `channel_phone` como `fieldValue` desde `Edit Fields`; el modelo ya no elige teléfono.
- Dedup por id + debounce 8 s en Redis `chat:` (fail-open). Adjuntos pasan el filtro con nota.
  **Abierto:** el acuse de la foto no sale fiable (el LLM saluda genérico).
- Handoff: mensaje saliente con `sender.type:"user"` → pausa; asigna a "Ecobox" y reabre; el mensaje
  sale aunque falle la etiqueta (verificado por config, no por fallo inyectado).
- Payloads: contacto `sender.type:"contact"`, bot `"agent_bot"`. Integración por webhook de cuenta
  (el agent bot no está asignado a inbox; funciona así). Sin automation rules.

**Recordatorios `QVPf25PZyLv0UHII`:** nunca habían enviado nada. Ahora claim atómico → Meta → marca
solo con `messages[0].id`; rama 48 h creada; ventana 9-21 h; solo eventos con `Cliente:`; números
extranjeros intactos; cita reservada después del momento natural no recibe recordatorio; alertas de
Slack deduplicadas en Redis (Meta y errores de GCal/Postgres). Plantillas genéricas
`recordatorio_{24h,48h}_cita` (sin sede). **No verificado que la de 48 h siga APPROVED**: falta el WABA
ID (no está en 1Password; sacarlo de WhatsApp Manager y guardarlo).

**Meta:** `CONNECTED`, calidad GREEN, `name_status: AVAILABLE_WITHOUT_REVIEW`, `TIER_250`. No hay
limitación real; el "LIMITED" de la primera auditoría era erróneo.

**Sin verificar:** retención de ejecuciones n8n (~15 h visibles). `dokploy-safe.sh` redacta el compose
entero y la clave SSH no está autorizada en 185.99.186.132:5251 → mirar a mano en Dokploy
`EXECUTIONS_DATA_*`. Filas de prueba en `ecobox_chat_memory` del 617314938 sin limpiar.

**Datos que estaban mal en este HUB (corregidos abajo):** número de voz, modelo, voz, tools.

## Sesión 2026-09-10 (noche) — motor de citas: segunda pasada, teléfono obsoleto y auth a medias

Scripts en `…/scratchpad/entrega/` (20-31), todos idempotentes; el detalle en `30-LEEME-horario.md`.

- **8 alertas en el Slack del cliente y NO era producción**: un bucle mío con `set -- $W` en zsh
  mandó una URL malformada a 8 webhooks. Pero destapó un defecto real — la validación colgaba
  **detrás** de dos llamadas a Google → puerta `Validar consulta` delante, y las fechas imposibles
  (`2026-04-31`, `10:60`, `2026-13-05`, ventana invertida) devuelven 200 con motivo en vez de 500.
- **Dos críticos MÍOS que encontró la contraauditoría** (y verifiqué): la fecha normalizada nunca
  llegaba a Google —siete nodos releían `Edit Fields`— así que el bug del `+02:00` seguía vivo
  entero; y `sede='Majadahonda'` con mayúscula hacía que la puerta mirase los festivos de un taller
  y Google escribiese en el calendario del otro. Arreglados en el **punto de entrada único**.
  Ver [[normalizar-en-un-nodo-intermedio-no-protege-a-quien-relee-el-de-entrada]].
- **El teléfono obsoleto `+34 636 521 315` estaba vivo de cara al cliente**: KB de voz, prompt del
  bot y botón de WhatsApp del **correo de confirmación**. Contrastado contra Meta
  (`display_phone_number` = `+34 910 05 48 13`), no de memoria. Y **Majadahonda no existía en la KB**.
  Corregido y publicado (voz **v16**).
- Las **8:00 y las 15:00 eran inconsultables por teléfono** (a una consulta se le aplicaba la regla
  de una reserva) y los seis textos de rechazo eran **código muerto**: ni voz ni chat leían `message`.
- Verificación: 66 casos verdes, 8 mutantes con víctima, ejecución 5356 como prueba en vivo.
- **Sin hacer todavía**: una reserva REAL de punta a punta. `15-limpiar-pruebas.sql` sigue sin correr.
  `GCal create.description` escribe un `\n` literal.

## Sesión 2026-09-10 — la WEB: reforma completa + segunda sede (commit `acc8a9c`, en `main`)

Primera vez que se toca la web desde el alta. Auditoría contra las webs maduras del
estudio (22 hallazgos, veredicto del cliente uno a uno) **más el alta del segundo
taller**. Todo en `main` de `AgentesIA-MAdrid/ecobox`, 62 ficheros, +6.103/−887.

**El negocio tiene DOS talleres**, confirmado hoy: C/ Rotterdam 3 (Las Rozas, domicilio
social) y **C/ Monjitas 13, 28220 Majadahonda**. Mismo teléfono, mismo horario, mismos
seis servicios, mismo domicilio fiscal. **Ninguna de las dos tiene ficha de Google
Business Profile** — es la tarea de mayor impacto pendiente y no es de código.

- **`src/lib/` es la única fuente de verdad** (once módulos). Ningún componente escribe
  ya un teléfono ni una dirección. Las sedes viven en una lista `LOCATIONS`, no en dos
  campos: quien pinta direcciones las recorre.
- **El JSON-LD se genera**, ya no se escribe a mano. `@graph` con la sociedad (CIF) y una
  ficha `AutoBodyShop` por taller unidas con `branchOf`; Majadahonda **sin `geo`** a
  propósito. Ver [[dos-locales-del-mismo-negocio-van-en-un-graph-con-branchof]].
- **Teléfono: +34 910 054 813** para voz y WhatsApp, en las dos sedes. El `+34636521315`
  del onboarding está **obsoleto** y así consta con fecha en `phones.ts`.
- **0 KB de JS de cliente**: fuera la isla React y framer-motion; FAQ con `<details>` y nav
  móvil con CSS puro. Hero de 862 KB → 79 KB con AVIF/WebP.
- **Contraste**: el texto sobre el verde de WhatsApp iba a 2,47:1 (falla AA), ahora 7,84:1.
  Ver [[tailwind-v4-emite-oklch-y-el-hex-de-la-tabla-v3-mide-otro-color]].
- **Legales nuevos** (`/aviso-legal`, `/privacidad`, `/cookies`) generados desde `legal.ts`,
  con `LEGAL_REVIEW.reviewed = false`: **no los ha visto un abogado**, y el DPA sigue sin firmar.
- **19 pruebas** con los dientes medidos por mutación, no supuestas. Una de ellas
  (`frescura.test.mjs`) existe porque las demás leen `dist/` y una build vieja daba verde.
  Ver [[mutate-guard-cruza-rutas-del-stage-mutar-desde-el-subproyecto-no-desbloquea]] y
  [[los-scripts-mjs-no-los-typechequea-astro-check-y-un-cambio-de-shape-los-rompe-mudo]].

**Bloqueante de despliegue**: `www.ecobox360.es` contesta un Traefik con certificado por
defecto y 404 en http y https — **la app no está enrutada**. Nada de lo anterior se ve en
producción hasta que el dominio apunte a `ecobox-web-exjura` (host 185.99.186.132).

**Decisiones que quedan del cliente**: el mapa de contacto (sin iframe / con banner de
cookies / carga al pulsar), la barra de CTA en móvil, y las coordenadas exactas de cada
taller. **Recomendación explícita: NO hacer página por sede todavía** — con los mismos
servicios, teléfono y horario saldrían casi idénticas y competirían entre ellas; merecen
la pena cuando cada taller tenga fotos y contenido propio.

Informe con el antes y el después: https://claude.ai/code/artifact/7739ff8d-01b8-4cc7-9047-38d7d0609b21

## Sesión 2026-06-02 — 2ª ronda test E2E (voz): transfer, doble-booking, fecha, sustitución

Tras checklist E2E (chat A1-A12 OK; voz B1-B3 OK) salieron 3 fallos en voz, todos corregidos y verificados:

1. **No transfería** — `n-transfer-human` estaba en `warm_transfer` (espera descuelgue + detección humano 30s) **y** el nº destino `+34617314938` es el del propio caller (Manu) → marca su línea ocupada → falla siempre. Fix: `transfer_option` → `cold_transfer` (reenvío directo). Nº mantenido (probar desde OTRO móvil). Flow v10, número usa `inbound_agent_version:None` = latest, ya live. Ver [[retell-cold-vs-warm-transfer-y-numero-distinto-del-caller]].
2. **Doble-booking** — voz reservó sobre un evento ya existente a las 17:00. El `event_id` determinista solo bloquea mismo phone+slot, no a otro cliente. Fix: guard server-side en `Reservar_cita` (`Check overlap` GCal getAll ventana [hora,hora+30m] → `Eval overlap` → `IF slot libre` → si ocupado `Respond slot ocupado` status:error, sin crear ni WhatsApp). Verificado: hueco ocupado rechaza, libre crea. Ver [[n8n-reservar-overlap-guard-server-side-anti-doble-booking]].
3. **Fecha hardcodeada** (`global_prompt`: "HOY es viernes 29 de mayo") — reemplazada por las variables de sistema de Retell `{{current_time_Europe/Madrid}}` + `{{current_calendar_Europe/Madrid}}` (rellenadas por llamada, calendario 14 días con "(Today)"). Sin cron. También quitada la fecha hardcodeada de `n-confirm-cita`. Ver [[retell-current-time-y-current-calendar-dynamic-vars-evitan-fecha-hardcodeada]].
4. **Sustitución/recogida por voz** — reforzada la prohibición en global #5 y `n-collect-damage` con la pregunta concreta vetada.

Hallazgo menor: `buscar_reserva` no encuentra una cita creada segundos antes (lag q-search GCal) → solo afecta "reservar+cancelar en la misma llamada". Backups `retell_flow_backup_2026-06-01_*_pre_coldtransfer.json`, `wf_reservar_backup_2026-06-01_*_pre_overlap.json`.

### Transfer voz — fix definitivo (routing)
El cold_transfer no bastaba: el transcript mostró que Alex decía "te paso con un compañero" pero NUNCA disparaba el nodo. Causa real: el cliente pedía humano **dentro de un subagente** (`n-collect-damage`/date/confirm/info) y esos nodos **no tenían edge a `n-transfer-human`** (solo `n-classifier` y `n-gestionar`). Fix: añadido edge "pide humano/se enfada → n-transfer-human" a los 4 subagentes. `n-transfer-human` no es global (`global_node_setting:null`). Número transfer `+34617314938` (= nº de Manu; al probar, llamar desde OTRO móvil). Flow v10, número usa `inbound_agent_version:null` = latest → live sin publish. Ver [[retell-subagente-sin-edge-a-transfer-no-puede-derivar]].

## Sesión 2026-06-02 (cont.) — Email rebrand + doc cliente + observabilidad

### Email rediseñado (marca EcoBox 360)
Nodo `Build Emails HTML` de `Reservar_cita` reescrito: cabecera carbón #1E2429 + **logo real** (banner blanco), bloque fecha en carbón, botón "Cómo llegar", pasos honestos. **Sin** sustitución/recogida (el cliente confirmó que NO ofrece esos servicios — pendiente quitarlos también de prompts voz+chat, KB y FAQs si se confirma del todo). **Sin** "un compañero te llamará" (la cita ya se cierra con hora concreta). Email cliente + interno rebrandeados. Previews navegables en `Ecobox/email_previews/{cliente,interno}_ecobox360.html`. Test enviado OK.
- **Logo hospedado** en n8n: workflow `ASSET — logo EcoBox360 PNG` (id `aSjTWzxmfdb2glCz`) sirve el PNG en `https://n8necobox.agentesialabs.com/webhook/ecobox-logo` (1200×300, base64 embebido). Fuente: `Ecobox/assets/ecobox360-logo-1200.png` (extraído del PDF de marca AAFF). Cuando Cristian dé un PNG oficial hospedado, swap en la var `LOGO`.
- Email interno sigue a `m.delmonte.p@agentesia.madrid` (pendiente cambiar a `cristian@ecobox360.es`). Sale por voz Y por WhatsApp (mismo workflow).

### Documento entregable "Cómo funciona" (cliente)
`Ecobox/docs/EcoBox360_como_funciona.pdf` (10 pág, A4, autocontenido) + `.html`. Logos EcoBox + AgentesIA (`~/Downloads/aia.svg`). Pantallazos **reales**: WhatsApp (mock), 2 emails, y Chatwoot real (inbox, handoff conv 18, alta de agente). Generado con Playwright (`/tmp/pw`, chromium 1223). Capturas sueltas en `docs/*.png`.

### Observabilidad — Error Handler (NUEVO, lo que faltaba)
Antes: CERO alertas si un workflow fallaba (te enterabas por queja del cliente). Ahora:
- Workflow **`Error Handler — EcoBox`** (id `z2EWXyATOsj6qtAW`): Error Trigger → Set contexto → **Slack #01-incidencias** (`C0ASNEXM2N4`) + **Email a `info@agentesialabs.com` + `m.delmonte.p@agentesia.madrid`**.
- `errorWorkflow=z2EWXyATOsj6qtAW` enlazado en los 7 críticos (Reservar, Cancelar, Buscar, Mirar, Bot, Recordatorios, Meta health).
- Slack vía bot token: cred `slackApi` `hFSlkCZGERfTE0Ll` (bot `n8n_aia_bot`, workspace Agentesia Lab). **Hubo que unir el bot al canal** (`conversations.join`, no era miembro) si no daba `not_in_channel`.
- **Gotchas**: (a) el handler DEBE estar `active` para que `errorWorkflow` lo invoque, y n8n **no activa** si un nodo tiene credencial requerida ausente → el nodo Slack bloqueaba; resuelto creando la cred. (b) `errorWorkflow` SÍ se puede setear por public API (está en la whitelist de settings). (c) credencial `slackApi` por API exige enviar también `signatureSecret` y `notice` (vacíos) aunque `required` solo liste `accessToken`. Ver [[n8n-error-trigger-handler-debe-estar-activo-y-sin-cred-faltante]].
- Verificado E2E: fallo forzado en `Mirar_disponibilidad` → Slack `ok:True` + email a los 2. **Pendiente opcional**: cron de salud diario (token Meta/OAuth GCal/Chatwoot a punto de caducar).

## Sesión 2026-06-01 — Chat WhatsApp E2E real + 6 fixes workflows + cleanup GCal

Primer test real de Cristian/Manu por WhatsApp (Chatwoot inbox 2 → bot Alex). Destapó 3 síntomas → 6 bugs reales arreglados sobre ejecuciones de producción (no simuladas). API key n8n del `.credentials.local` **volvió a funcionar** (los PUT/activate fueron 200 todo el día — el 401 del 05-29 era restart de contenedor, ya no aplica). Backups frescos en `Ecobox/wf_{bot,reservar,buscar,cancelar,mirar}_backup_2026-06-01_*.json`.

**Fix A — Audio ignorado.** `Chatwoot Bot Alex`: `IF mensaje cliente` exigía `body.content` notEmpty → las notas de voz llegan con `content=null` + audio en `attachments[0]` (file_type=audio, .ogg/opus) → el bot ni arrancaba. Fix: IF acepta content **o** audio; rama nueva `IF audio → Download audio (HTTP GET data_url, response=file) → Transcribe (HTTP a OpenAI /v1/audio/transcriptions whisper-1, cred predefinida openAiApi) → Edit Fields`. `message = content || $json.text`.

**Fix B — Bot reservaba en pasado / sin hora.** El chatbot NO tenía `fecha_hoy` (solo lo tenía Retell voz) → calculaba un "miércoles" arbitrario (reservó 2026-03-11 08:00). Fix: inyectada `fecha_hoy` en el `text` del AI Agent (`[ctx fecha_hoy=YYYY-MM-DD (díasemana) …]` vía `$now` Luxon) + system prompt: fecha siempre futura desde fecha_hoy + OBLIGATORIO hora HH:MM concreta (prohibido "por la mañana").

**Fix C — No se enviaba plantilla WhatsApp.** `Reservar_cita` NO tenía nodo de envío (solo GCal + emails). Fix: nodo `WhatsApp confirmacion` (HTTP Graph `/{PHONE_NUMBER_ID}/messages`, template `confirmacion_cita_ecobox_2`, {{1}}=name {{2}}=fecha natural Luxon es-ES, cred Meta `AXKaZLlt5xzkjukL`). **Verificado**: enviado y `accepted` por Meta al +34617314938. `Email al cliente` → `onError:continue` (leads WhatsApp no traen email).

**Fix D — Guard fecha pasada.** `Validate input` ahora rechaza `preferred_date < hoy` (boolean `DateTime.fromISO(preferred_date) >= $now.startOf('day')`). Antes solo validaba `startsWith "2026"`.

**Fix E — buscar/cancelar/mirar parseaban null** (el `.args.` sin `?.` — el 05-29 SOLO se arregló en Reservar_cita, estos tres quedaron pendientes). Los tools del chat mandan body PLANO (`{phone}`, `{event_id}`, `{After,Before}`); sin `args`, `.args.X` revienta → null. Síntomas: `buscar` searcheaba `+34` y matcheaba un evento ajeno; **`mirar` con After/Before null → GCal getAll sin ventana → devolvía TODOS los eventos de otros días → "está ocupado" siempre** (causa del "no hay nada el miércoles pero dice ocupado"). Fix: optional chaining `body?.args?.X || body?.X` en los 3 + `Format slots` de mirar filtra ocupados a la ventana [After,Before]. Verificado: 3-jun mañana→count 0 libre; 2-jun→solo eventos del 2-jun.

**Fix F — Respond hardcodeado a éxito (reserva/cancelación fantasma).** `reservar.Respond OK` y `cancelar.Respond` devolvían SIEMPRE "Listo, te he agendado/cancelado", y GCal create/delete tienen `onError:continue` → el error de Google se ignoraba y el bot mentía. Fix reservar: nodo `IF created ok` (`!$json.error`) tras GCal create → true→Build Emails+WhatsApp; false→`Respond reservar error` (`status:error`, SIN WhatsApp). Fix cancelar: `Respond` ternario sobre `$('GCal delete').item.json.error` → `status:ok/error`. Prompt bot: regla "HONESTIDAD DE TOOLS" (prohibido confirmar sin `status:ok`; cancelar debe pasar el event_id EXACTO `ecXXXX`, nunca la matrícula).

**Colisión id determinista**: re-reservar el MISMO slot → mismo `event_id` (FNV de phone+preferred_date) → GCal 400 → ahora cae limpio en rama error (no doble-booking, no falsa confirmación). Latente: re-reservar tras cancelar puede colisionar con id borrado (Google retiene ids un tiempo).

**Cleanup GCal**: 5 eventos de test borrados por event_id explícito vía `cancelar_cita` (4356ADA, SAB123, 7777FIX, CONC123, 6094HTX) — el borrado en bloque lo bloqueó el classifier (destructivo sobre calendario compartido), lo ejecutó Manu con comando preparado. Agenda limpia.

**Pendiente real**: smoke E2E chat de un hueco NUEVO (cancelar + reservar miércoles 9:00) confirmando que cancela de verdad, no choca y llega plantilla. Inbound de clientes reales aún requiere publicar la app Meta (dev mode) + logo/color/firma de Cristian.

Learnings nuevos para vault (ver /obsidian-1): IF mensaje cliente debe aceptar audio; transcripción Whisper inline en n8n vía HTTP cred predefinida; `mirar` con ventana null devuelve calendario entero; Respond hardcodeado a éxito + onError:continue = bot miente; optional chaining pendiente en buscar/cancelar/mirar (no solo reservar); n8n PUT API rechaza `settings` no-whitelisted (binaryMode) con 400.

## Identidad

- **Razón social**: ECOBOX 360 S.L · CIF B27609114
- **Domicilio**: Calle Rotterdam 3, 28232 Las Rozas (Madrid)
- **Contacto**: Cristian Sánchez Alonso — cristian@ecobox360.es
- **Web**: www.ecobox360.es
- **WhatsApp actual (app móvil personal)**: +34 636 521 315 (NO migrar — se queda con Cristian)
- **Slug interno**: `ecobox`

## Stack final desplegado

| Pieza | Detalle |
|---|---|
| Dokploy dedicado | `https://ecobox.agentesialabs.com` · server Stackscale `185.99.186.132:5251` |
| n8n self-hosted | `https://n8necobox.agentesialabs.com` · postgres17 + redis7 + n8n 2.18.7 |
| Chatwoot **dedicado EcoBox** | `https://chatecobox.agentesialabs.com` (pivot 2026-05-22: pasó de compartido a propio) |
| Retell agent voz | `agent_250ae0d683b8086fdcaaed9027` — Alex — flow en `gpt-4.1` cascading, temp 0.3, `tool_call_strict_mode` (verificado 15-sep; el gpt-4o que ponía aquí ya no es cierto) |
| Retell Conversation Flow | `conversation_flow_5f455ab09cf4` — Rigid, 5 tools custom (Mirar_disponibilidad, Reservar_cita, Buscar_reserva, Cancelar_cita, Aviso_estado). Publicada **v23** (15-sep tarde: v21 arista/KB/saludo; v22 la transferencia explica el motivo, p.ej. «al venir de Mutua te tengo que pasar directamente con mis compañeros»; v23 taller justo tras seguro/grúa + PASO 0 en fecha, hora dentro de horario sin «lo siento», y latencia: `eleven_flash_v2_5` + `stt_mode: fast` + `enable_dynamic_responsiveness: false`, ver [[eleven-v3-en-retell-cuadruplica-el-tts-frente-a-flash]]) |
| Retell KB | `knowledge_base_34f85cf8295d3369` — 11 fuentes de texto, top_k 3 |
| Número de voz real | **`+34910054813` "Ecobox Netelip"**, `agent_version: latest_published` (fijado 15-sep). El `+34919932797` (Zadarma) es hoy "Peluqueria Muestra (demo)" y lo atiende otro agente |
| Voz | `custom_voice_b1e828eb8fc685cb9e0caa21ce`, eleven_v3 (cambiada el 15-sep 08:29, v17; antes Pablo Fernández `custom_voice_ba7fd23dc476d2ac821f8edd10`) |
| Número transfer humano | **`+34617314938`**, cold, `show_transferee_as_caller: false` (Netelip da SIP 500 con `true`) |
| 1Password vault | "EcoBox" en agentesialab — 9 items |

## Estado workflows n8n (2026-05-25)

> **Histórico.** Al 15-sep los 12 workflows están activos (incluidos Recordatorios, Meta health check,
> Aviso_estado `622XAIV0Dek8NEJI`, Calendario festivos `kuR5tIxQ66VrvbhJ`, Error Handler
> `z2EWXyATOsj6qtAW`). Lo vigente de cada uno está en "Sesión 2026-09-15"; esta tabla no.

| WF | ID | Estado | Notas |
|---|---|---|---|
| Chatwoot Bot Alex | `lv7pee2XAU5OngOB` | ACTIVO | v1 sin tools (chat aún sin migrar) |
| Mirar_disponibilidad | `iO9m2aSifPYY9LuA` | **ACTIVO** | `alwaysOutputData=true` en GCal getAll (calendar vacío rompía downstream). Smoke OK |
| Reservar_cita | `bJwoFHSBO6BK7gUe` | **ACTIVO** | Guard `Validate input` (rechaza `{{from_number}}` literal y años !=2026/2027) + crypto module fix (FNV-1a puro en `Gen GCal event ID`) + fallback `phone` desde `call.from_number` cuando arg es placeholder/vacío + `onError: continueRegularOutput` en Email cliente (skip si no destinatario) + `Respond OK` corto sin doble readback |
| Buscar_reserva | `HHryz8eDv3GOxZMF` | **ACTIVO** | **Reescrito**: ya NO usa Chatwoot search (devolvía "Authorization failed for bots"). Ahora busca directo en GCal `q` por `+34XXX` con `timeMin=now`. Devuelve `event_id` |
| Cancelar_cita | `L2W64JNIQmd0IJLV` | **ACTIVO** | **Simplificado**: borra por `event_id` que viene de Buscar_reserva. Garantiza cancelar SOLO esa una, deja resto del histórico intacto. `onError: continueRegularOutput` |
| Recordatorios cron 48h+24h | `QVPf25PZyLv0UHII` | inactivo | depende de Meta token + plantillas HSM aprobadas |
| Meta token health check | `Jbf5rZepHYM21MPQ` | inactivo | depende de Meta token |
| TEST Email Templates | `DogJ9b1iOHmJeS2S` | ACTIVO | webhook `/test-email-templates` — verificado envío real |

## Credenciales n8n (10)

| Tipo | Cred ID | Notas |
|---|---|---|
| Google Calendar OAuth | `LbmjQyqyDIWblulm` | Cuenta `ecobox360taller@gmail.com` — autorizado 2026-05-25 |
| OpenAI | `O7HC4LlEMW9qnNs9` | rotado 2026-05-22 |
| Postgres EcoBox interno | `QFMXn2QCNc74b4Us` | |
| Redis EcoBox interno | `2DcMeBcStZb57rcI` | |
| Chatwoot Bot Header (EcoBox dedicado) | `n8Zq72EUU23qB9cp` | |
| Chatwoot Admin Header (EcoBox) | `XP8mZAkDC0QRQNMI` | |
| Chatwoot Bot Header (legacy compartido) | `09Sm4jv8M6R6RcGG` | sin uso |
| SMTP Gmail | `BqK8VZqSh1ylDONz` | **App password** `ecobox360taller@gmail.com` — FROM = `EcoBox <ecobox360taller@gmail.com>` (cambio a `notificaciones@ecobox360.es` requiere Send-As alias o Workspace) |
| Meta WhatsApp Bearer | `dczhQTAKaeGVe1gr` | PLACEHOLDER — pendiente token Meta |
| Telegram | `ramEttKmAly4wflv` | PLACEHOLDER — descartado (sin Telegram alerts) |

## Google Workspace EcoBox

- Cuenta operativa: `ecobox360taller@gmail.com` (2FA + app password generada)
- **GCAL_ID**: `ecobox360taller@gmail.com` (calendario principal — no se creó "Peritajes" dedicado por petición del cliente)
- **DRIVE_FOLDER_FOTOS**: `1yrD1PlG9H42tKQSfWfFLZNPqL66fM2Eo`
- Drive/Sheets APIs habilitadas en el GCP project (pero no se usan en el stack final — pivot a Chatwoot dedicado)

## Pipeline conversacional Alex (voz — operativo)

```
n-welcome ("Hola, soy Alex de EcoBox, ¿en qué te puedo ayudar hoy?")
  → n-extract-1 (intent + nombre)
  → n-classifier
    ├─ nueva_cita
    │   → n-collect-damage (subagent: nombre, daño, coche, matrícula, seguro si aplica)
    │   → n-collect-date (subagent + Mirar_disponibilidad: OBLIGATORIO consultar agenda real)
    │   → n-confirm-cita (subagent + Reservar_cita: confirma teléfono "¿te guardo este número?" → resumen → reserva → confirmation_text corto)
    │   → n-end-cita
    ├─ gestionar_cita (subagent + Buscar_reserva + Cancelar_cita)
    │   ├─ CASO A cancelar → pregunta "¿con este nº o con otro?" → Buscar → confirmar → Cancelar by event_id → fin
    │   ├─ CASO B cambio fecha → "mándanos un mensaje por WhatsApp" (NO transfer)
    │   ├─ CASO C ¿cómo va? → pide matrícula → "déjame consultar..." → "están avanzando, te avisarán" → solo transfer si insiste
    │   └─ CASO D pide humano explícito → transfer
    ├─ info_rapida → KB
    └─ humano / fuera idioma → transfer +34617314938
```

## Decisiones clave acumuladas

- [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo]] — Chatwoot **dedicado** EcoBox (2da revisión: compartido → propio)
- [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode]] — Rigid €0.135/min
- **Notificaciones** = nativas Chatwoot (sin Telegram)
- **Email** solo en chatbot WhatsApp (por voz es incómodo). Por voz solo va email a Cristian (alert interno)
- **Plantillas email**: 2 (confirmación cliente HTML + alert Cristian)
- **Recordatorios HSM 48h/24h**: descartados (workflows desplegados pero inactivos)
- **Sin Sustitución / Recogida** ofrecidas por iniciativa de Alex — solo si el cliente las pregunta
- **Voz**: probadas en orden 11labs-Santiago, cartesia-Manuel, custom Borja, **custom Pablo Fernández** (final)
- **Modelo flow**: `gpt-4o` (más rápido que gpt-4.1, suficiente para Rigid)
- **Latencia**: `responsiveness=1.0`, `enable_backchannel=true` con "ajá/vale/claro", `begin_message_delay_ms=500`

## Meta WhatsApp Cloud API (LIVE 2026-05-28)

Número `+34 910 05 48 13` (provider Netelip) llegó CONNECTED + CLOUD_API + VERIFIED tras 3h de iteración:
1. WABA original (`1277706597676685`) + Phone original (`1124445220757479`) quedaron huérfanos cuando Cristian desvinculó el número de la app móvil WhatsApp Business (Meta hizo auto-cleanup que invalidó las referencias — el token retuvo validez pero perdió acceso a esos objects).
2. User recreó WABA + Phone vía API en mismo Portfolio — IDs nuevos abajo.
3. PIN 2FA custom seteado vía `POST /register`.
4. 3 plantillas HSM creadas (PENDING review Meta).

| Activo | ID |
|---|---|
| Portfolio empresarial | `1011127821491282` |
| **WABA actual** (Ecobox 360) | `1488289103073845` |
| **Phone Number ID actual** | `1136826222847102` (`+34 910 05 48 13`, CLOUD_API, CONNECTED, VERIFIED) |
| WABA huérfana (legacy) | ~~`1277706597676685`~~ |
| Phone huérfano (legacy) | ~~`1124445220757479`~~ |
| Message template namespace | `7049d1fc_3cb6_4dd5_b2fa_168acb7376ef` |
| System User `ecobox-api` (control total) | `61590397051384` |
| App Meta `Ecobox360` | App ID `1643186026903792` |
| **Token permanente + PIN 2FA** | `Ecobox/.credentials.local` (`META_PERMANENT_TOKEN`, `META_PHONE_PIN`). Pendiente espejar a 1P EcoBox cuando sesión `op` se reabra. |
| Plantillas HSM (PENDING review) | confirmacion_cita_ecobox `980688254703968` · recordatorio_48h_ecobox `2117110505903801` · recordatorio_24h_ecobox `2156080465190409` |
| App Secret / Verify Token webhook | NO entregados — solo bloquean INBOUND (cliente WhatsApp → bot). Outbound (recordatorios + confirmaciones) ya funcional. |

## Bloqueadores externos restantes

1. ✅ ~~Crear WABA + Permanent Access Token Meta~~ — hecho 2026-05-28.
2. ✅ ~~Migrar +34910054813 a Cloud API + verificación~~ — DONE 2026-05-28 (vía recreación WABA + Phone tras desvincular app móvil).
3. ⏳ **Esperar aprobación HSM Meta** — 3 plantillas en PENDING desde 2026-05-28 (UTILITY suele aprobar <1h). Cuando aprueben, activar workflows `Recordatorios cron` (`QVPf25PZyLv0UHII`) y `Meta token health check` (`Jbf5rZepHYM21MPQ`) tras actualizar cred n8n `dczhQTAKaeGVe1gr` con el token.
4. ✅ ~~Regenerar API key n8n (401 desde PUT bot v2)~~ — la key del `.credentials.local` volvió a funcionar 2026-06-01 (todos los PUT/activate 200). Era restart de contenedor, no rotación.
5. ⏳ App Secret + Verify Token webhook Meta — solo necesario cuando activemos inbound (cliente WhatsApp → bot Chatwoot). Outbound ya operativo.
6. ⏳ Conectar inbox Chatwoot al Phone Number ID `1136826222847102` (Chatwoot Cloud channel WhatsApp). Sin esto, ningún mensaje cliente llega al bot.
7. ⏳ Logo PNG público + color marca hex (defaults `#0F1B2D` + `#E76F51`) + firma email.
8. ⏳ URL Google Maps corta de Rotterdam 3.
9. ⏳ Confirmar definitivamente cómo gestionar "cómo va mi reparación" — Alex finge consulta hoy.

## Learning capturado 2026-05-28

- [[meta-waba-orfana-tras-desvincular-app-movil-recrear-via-api]] (NUEVO) — al eliminar la cuenta WhatsApp Business app, Meta puede dejar la WABA + Phone Number en estado huérfano (token válido pero `Object does not exist` en Graph API). Solución: recrear via API directamente, no esperar a que Meta libere los IDs antiguos.
- [[whatsapp-cloud-api-vs-business-app-numero-exclusivo]] ya confirmado con caso real: un número en app móvil aparece como `platform_type=ON_PREMISE + status=DISCONNECTED` aunque no esté en On-Premise legacy real.
- [[chatwoot-3x-whatsapp-cloud-display-phone-number-bug-doble-plus]] — Chatwoot 3.x `Webhooks::WhatsappEventsJob#get_channel_from_wb_payload` concatena `"+"` siempre al `display_phone_number`. Meta real envía sin `+` así que no afecta producción, pero rompe simulaciones curl con `+` literal.

## Fixes 2026-05-29 — Smokes chat tool calls

**Bug 1 — Bot Chatwoot llama tools con args NULL** (4 agentes en consenso). Causa raíz: `parameters.jsonBody` envuelto en `={{ JSON.stringify({...}) }}` global con todos los `$fromAI()` dentro. n8n langchain 1.9 NO puede extraer schema individual desde esa sintaxis. El LLM ve la tool como `query: {}` opaco → llama con objeto vacío. Retell funciona porque define JSON Schema explícito con `required:[...]`. **Fix aplicado**: los 4 `toolHttpRequest` (`mirar_disponibilidad`, `reservar_cita`, `buscar_reserva`, `cancelar_cita`) ahora tienen `jsonBody` literal JSON con `"={{ $fromAI('field', 'desc', 'type') }}"` por valor. Learning para vault: [[n8n-langchain-toolhttprequest-jsonbody-no-envolver-en-jsonstringify-global]].

**Bug 2 — Workflow Reservar_cita acepta args null y miente al bot**. Cuando args null: Edit Fields colapsa todo a null, GCal create falla con "Bad request" pero `onError: continueRegularOutput` deja seguir, Respond OK devuelve `"Listo, . Te llega un WhatsApp"` con coma huérfana, emails se envían con basura. **Fix aplicado**: nuevo nodo `Validate input` después de Edit Fields con 3 conditions AND (name notEmpty, matricula notEmpty, preferred_date startsWith "2026"). Si rechaza → `Respond ValidateError` con `confirmation_text` instructivo que el bot lee al cliente. Learning para vault: [[n8n-workflow-validate-input-guard-evita-mentir-cuando-bot-manda-null]].

**Bug 3 — Edit Fields sin optional chaining colapsa todo a null cuando body no tiene `args` wrapper**. Las expresiones usaban `$json.body.args.name || $json.body.name || 'Cliente'`. Cuando el bot chat manda directo `body.name` (sin `args` wrapper), `body.args.name` lanza `TypeError: Cannot read property 'name' of undefined` y n8n silently devuelve null. Por eso voz Retell (que sí wrapea `body.args`) funcionaba, chat no. **Fix aplicado**: cambiadas todas las expresiones de Edit Fields a `$json.body?.args?.name || $json.body?.name || 'Cliente'` con optional chaining. Learning para vault: [[n8n-expressions-optional-chaining-obligatorio-cuando-body-args-puede-faltar]].

**Smokes pasados tras los 3 fixes** (2026-05-29):
- Args null → workflow rechaza con `confirmation_text: "No pude reservar porque faltan datos..."` ✓
- Args válidos test mode (`matricula=ZZZ0000`) → entra a Respond TEST sin tocar GCal ✓
- Pendiente: smoke real desde Chatwoot bot con cliente final → debe crear evento GCal en `ecobox360taller@gmail.com` + enviar email

## E2E multi-perspectiva 2026-05-29 — verificación post-fixes

**4 agentes paralelos** (happy path chat, edge cases chat, voz Retell simulada via webhooks, auditor estado). Hallazgos:

- ✅ **Voz Retell funciona al 100%** — 6 tests webhook con formato `body.args + body.call` pasan + 2 citas reales creadas hoy en producción + flujo cancel E2E OK
- 🔴 **Bot Chatwoot rompía** — bot llamaba tool con `query:{}` y alucinaba "cita confirmada". Causa raíz: el `jsonBody` con expresiones `={{ JSON.stringify(...) }}` o `"={{ $fromAI }}"` o `"{{ $fromAI }}"` no se interpolaba — n8n mandaba el body LITERAL con las expresiones como strings al webhook. **Fix definitivo** (fix6): cambiar a `specifyBody: "keypair"` con `parametersBody.values[]` declarados uno por uno con `valueProvider: modelRequired/modelOptional`. Tras fix6, exec 197 confirmada con args reales + GCal event creado + emails HTML generados.

Learning para vault: [[n8n-langchain-toolhttprequest-specifybody-keypair-es-el-formato-correcto-para-fromai]] — solo `specifyBody: "keypair"` permite a n8n declarar el schema correcto al LLM. Las formas `json` con `JSON.stringify` o expresiones inline NO funcionan porque n8n no parsea las expresiones dentro del jsonBody string a menos que TODO el campo empiece con `=` (lo cual rompe el JSON literal).

Bonus de la auditoría: **plantillas HSM Meta ya APROBADAS** las 3 (`confirmacion_cita_ecobox_2`, `recordatorio_24h_ecobox`, `recordatorio_48h_ecobox`).

## Pendientes (al cierre 2026-05-29, post 6 fixes encadenados)

1. **Smoke real bot chat E2E del user** — conversación turn-by-turn desde WhatsApp `+34617314938`. El sistema YA está verificado E2E con POST simulado pero aún no con WhatsApp real (formato Meta entregando webhook completo). El POST simulado y el webhook real son idénticos en estructura, pero conviene confirmar.
2. **Smokes funcionales adicionales chat**:
   - Buscar reserva existente ("ver mi cita")
   - Cancelar cita ("cancela mi cita")
   - Info rápida ("a qué hora abrís", "dónde estáis")
   - Handoff humano ("quiero hablar con persona") → label `humano` aplicado
   - Pregunta fuera de scope ("hacéis ITV") → derivación
3. ✅ ~~Cron diario actualizar fecha en Retell flow~~ — RESUELTO 2026-06-02 sin cron: `global_prompt` usa `{{current_time_Europe/Madrid}}` + `{{current_calendar_Europe/Madrid}}` (variables de sistema Retell rellenadas por llamada). Ver [[retell-current-time-y-current-calendar-dynamic-vars-evitan-fecha-hardcodeada]].
4. **Recordatorios cron** (`QVPf25PZyLv0UHII`) tiene nodos `noOp` TODO send HSM. Implementar `httpRequest` POST a Meta Cloud API `/messages` con template `confirmacion_cita_ecobox_2` + nodo `postgres` que update `reminders_sent`. Activar cuando plantillas HSM aprueben.
5. **Plantillas HSM**: las 3 siguen PENDING review Meta desde 2026-05-28. Revisar cada hora. UTILITY simples suelen aprobar <24h.
6. **Meta health check** workflow (`Jbf5rZepHYM21MPQ`) tiene bug en nodo `IF error` ("Conversion error: string '' can't be converted to object"). El endpoint Meta /me responde 200 OK. El bug es del workflow, no del token. Cosmético — no urgente.
7. **App Meta en dev mode**: solo recipients autorizados (Manu `+34617314938`). Para clientes reales → publicar app (necesita URL privacidad → necesita web).
8. **App Secret + Verify Token Meta** para validar firma `X-Hub-Signature-256`. Chatwoot tolera sin esto pero es buena práctica. Añadir cuando haya web.
9. **Logo PNG + color marca hex + firma email + URL Maps Rotterdam 3** (Cristian).
10. **Decisión definitiva "¿cómo va mi reparación?"** — Alex finge consulta hoy.

## Cambios infra reciente

| Pieza | Antes | Después (2026-05-29) |
|---|---|---|
| LLM bot Chatwoot | gpt-4o-mini | **gpt-4o** (mismo que voz) |
| jsonBody tools bot | `JSON.stringify({...})` global | literal con `$fromAI` por valor |
| Edit Fields Reservar_cita | `body.args.X || body.X` (sin `?.`) | `body?.args?.X || body?.X` (optional chaining) |
| Reservar_cita workflow | sin validate input | + nodo `Validate input` + `Respond ValidateError` |
| Retell global_prompt | "HOY es lunes 25 de mayo" hardcoded | "viernes 29 de mayo" hardcoded (TODO: cron diario) |
| Retell n-confirm-cita | "PASO 4 — Reservar_cita" suave | "PASO 4 ← TOOL OBLIGATORIA NO TERMINES SIN EJECUTARLA" |
| Backup workflows pre-fix | — | `Ecobox/wf_bot_backup_pre_fix4.json` + `Ecobox/wf_reservar_backup_pre_fix4.json` + `Ecobox/retell_flow_backup_2026-05-29_pre_fix.json` |

## Bot Chatwoot v2 con tools (2026-05-28)

Workflow `lv7pee2XAU5OngOB` actualizado: 17 nodos = 13 originales + 4 `toolHttpRequest` (`mirar_disponibilidad`, `reservar_cita`, `buscar_reserva`, `cancelar_cita`) reusando los mismos webhooks que la voz Retell. System prompt v2 enseña al LLM cuándo usar / cuándo no usar cada tool. Text del agente inyecta `[ctx phone=… name=…]` dinámico desde Edit Fields para que el bot no pida el phone al cliente. Verificado via API (nueva key n8n regenerada): 17 nodos activos + 4 conexiones `ai_tool`. Falta smoke E2E con mensaje real cuando Meta termine handshake webhook.

## Chatwoot WhatsApp Cloud inbox (LIVE 2026-05-28)

| Activo | Valor |
|---|---|
| Inbox ID | `2` (Channel::Whatsapp, provider=whatsapp_cloud) |
| Phone | `+34 910 05 48 13` apuntando a Meta phone_number_id `1136826222847102` |
| Callback URL (la que va en Meta App → Webhooks UI) | `https://chatecobox.agentesialabs.com/webhooks/whatsapp/+34910054813` |
| Verify token (debe coincidir con Meta UI) | guardado en `.credentials.local` `CW_INBOX_WHATSAPP_VERIFY_TOKEN` |
| Account webhook (Chatwoot → n8n bot) | id=1, only `message_created`, HMAC secret guardado |
| Meta app suscrita a WABA | `POST /v18.0/1488289103073845/subscribed_apps` OK 2026-05-28 |
| Plantillas HSM importadas auto al crear inbox | 3 PENDING (confirmacion_cita, recordatorio_48h, recordatorio_24h) |

Webhook Meta UI (Manu) configurado 2026-05-28. Field `messages` suscrito. App en dev mode aún — entrega solo a WhatsApp de usuarios con rol app o en lista de recipients (campo "A" del use case). Por eso mensajes reales del user no llegaron hasta que confirmó número (+34617314938 era el suyo, no de Cristian — error de mi memoria, hub corregido).

**Pipeline E2E verificado**: POST simulado `FIX_1779984161` (2026-05-28 18:02) → conv id 6 creada en Chatwoot → bot Alex respondió "Parece que no tengo tu nombre completo. ¿Cómo te llamas?" (LLM funcionando con system prompt v2).

**Bug Chatwoot 3.x descubierto durante el debug**: `Webhooks::WhatsappEventsJob#get_channel_from_wb_payload` siempre concatena `"+"` al `display_phone_number` del payload (`"+#{metadata.display_phone_number}"`). Si el payload viene con `+` (como mis simulaciones curl), construye `"++34..."` → no encuentra channel → `channel.blank?` → return early silencioso. Meta real envía sin `+` según spec oficial, no afecta producción. Mover este learning a [[chatwoot-3x-whatsapp-cloud-display-phone-number-bug-doble-plus]] en próximo /obsidian-1.

## Bugs conocidos / cleanup pendiente

- ✅ ~~Eventos smoke acumulados en GCal `ecobox360taller@gmail.com`~~ — 5 borrados 2026-05-28 vía workflow oneshot `_cleanup_smoke_gcal` (1 en junio 2024 + 4 en mayo 2026). Re-run idempotente devuelve 0. Workflow oneshot eliminado tras éxito.
- ✅ ~~API key n8n 401 tras PUT del bot v2~~ — RESUELTO 2026-06-01: la misma key vuelve a aceptar `/api/v1/*` (era restart del contenedor, no rotación). Sin cambios en `.credentials.local`.
- ⏳ Retell flow audit hallazgo menor: `global_prompt` y nodo `n-collect-date` tienen "2026" hardcoded — debería usar `{{ano_actual}}` (como ya hace `n-confirm-cita`). No bloqueante.

## Archivos locales

- `/Users/manueldelmonte/Ecobox/CLAUDE.md` — estado completo
- `/Users/manueldelmonte/Ecobox/ARQUITECTURA.md` — diseño Chatwoot
- `/Users/manueldelmonte/Ecobox/CHECKLIST_ARRANQUE.md` — 14 pasos para arrancar
- `/Users/manueldelmonte/Ecobox/email_templates.md` — 2 plantillas
- `/Users/manueldelmonte/Ecobox/email_previews/` — HTMLs navegables
- `/Users/manueldelmonte/Ecobox/whatsapp_templates.md` — sintaxis Meta `{{N}}`
- `/Users/manueldelmonte/Ecobox/.credentials.local` — IDs y tokens
- `/Users/manueldelmonte/Ecobox/retell_flow_backup_2026-05-25.json` — backup pre-restructure tools

## Learnings de esta sesión (2026-05-25/26)

- [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
- [[retell-tools-conversation-flow-require-tool-id-field]]
- [[retell-knowledge-base-api-requiere-multipart-form-data]]
- [[retell-subagent-nodes-dividen-agentes-monoliticos-en-especializados]]
- [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]]
- [[chatwoot-custom-attribute-definitions-endpoint-v3-renombrado]]
- [[chatwoot-bot-token-vs-admin-token-scopes-distintos]]
- [[chatwoot-search-contact-api-no-autorizada-para-bot-token]] (NUEVO 2026-05-25)
- [[n8n-network-external-true-falla-en-dokploy-sin-pre-create]]
- [[n8n-postgres-webhook-lastnode-solo-devuelve-primer-row]]
- [[n8n-public-api-google-oauth-schema-buggy-crear-en-ui]]
- [[n8n-crypto-module-bloqueado-en-task-runner-usar-fnv-puro]] (NUEVO 2026-05-25)
- [[n8n-public-api-no-permite-update-credentials-solo-post-delete]] (NUEVO 2026-05-25)
- [[n8n-respondtoWebhook-json-mode-requiere-expresion-objeto-no-literal]] (NUEVO 2026-05-25)
- [[n8n-gcal-getall-empty-no-propaga-downstream-usar-alwaysOutputData]] (NUEVO 2026-05-25)
- [[n8n-emailsend-onError-continueRegularOutput-skip-si-sin-destinatario]] (NUEVO 2026-05-25)
- [[n8n-gcal-create-additionalFields-description-escapar-newlines-no-backslash]] (NUEVO 2026-05-25)
- [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]
- [[gcal-eventid-charset-restriction-a-v0-9-base32hex]] (NUEVO 2026-05-25)
- [[gcal-q-search-no-encuentra-eventos-recien-creados-eventual-consistency]] (NUEVO 2026-05-25)
- [[retell-custom-voice-labels-pueden-estar-mal-etiquetadas-pese-al-nombre]] (NUEVO 2026-05-25)
- [[retell-from_number-no-auto-sustituye-en-tool-args-necesita-fallback-n8n]] (NUEVO 2026-05-25)
- [[retell-tool-call-strict-mode-no-fuerza-ejecutar-tool-solo-valida-args]] (NUEVO 2026-05-25)
- [[retell-zadarma-sip-no-popula-retell_llm_dynamic_variables-from_number]] (NUEVO 2026-05-25)
- [[llm-conversational-current-date-debe-inyectarse-explicito-en-prompt]] (NUEVO 2026-05-25)
- [[retell-boosted-keywords-stt-letras-españolas-zeta-efe]] (NUEVO 2026-05-25)

## Pendientes

- **Smoke grúa/Mutua → handoff + email** — verificar que el caso grúa/seguro Mutua dispara handoff a humano y envía email de aviso interno.
- **Smoke reserva E2E que dispare `Build Emails`** — corrida real de reserva que pase por el nodo `Build Emails HTML` de `Reservar_cita` (cliente + interno).
- **Smoke tope 7º** — comprobar el límite de 7 citas/huecos (tope al 7º).
