---
title: Centro Elphis — HUB
date: 2026-05-18
updated: 2026-09-04
source: investigación + onboarding firmado + discovery Clientify + propuesta enviada
tags: [cliente, agentesia, elphis, voz, whatsapp, retell, clientify, doctoralia, n8n, dokploy]
---

# Centro Elphis · HUB

Centro privado de tratamiento de adicciones en Madrid. Cliente Agentesia: paquete avanzado (voz Retell + chatbot WhatsApp + Clientify).

## Estado actual · 2026-09-04

**El aviso rojo de las 08:32 no era una avería: era el circuito de avisos, que llevaba 8 días clasificando mal.**

- ✅ **La cancelación se procesó bien** (exec 11899, Simone Fiorentini, cita del 8-sep): 3 deals a «Volver a contactar» con nota. El `throw` final de `Avisar correo descartado` es el diseño — así la cancelación llega a Slack en vez de morir en `error_log`.
- ✅ **Arreglado el reconocimiento de los códigos de negocio en `error-handler-global`**: n8n parte `'<codigo>: <detalle>'` en `description` + `message`, y el `startsWith` sobre `message` que entró el 27-ago dejó **los 10 códigos** en rojo, sin explicación ni pie, y con clave de dedup genérica — dos pacientes con `enlace_no_enviado` en la misma hora volvían a colapsar en un aviso. Ahora se compara por igualdad contra `description` limpia y el prefijo de `message`. → [[n8n-parte-el-mensaje-de-error-en-el-primer-dos-puntos]]
- ✅ Verificado: gate **463 checks** (10 códigos × 3 formas de llegada + falso positivo SQL + clave por caso + payload real de la 11899), **9 mutaciones con víctima**, y E2E con un workflow temporal → aviso azul real en `#01-incidencias` a las 12:02. Backup `~/Projects/elphis/avisos-20260814/errh-pre-fixcodigo-20260904.json`. → [[un-gate-cuyo-fuente-es-copia-de-lo-desplegado-caduca-y-nadie-lo-corre]]
- ✅ Actualizados el texto de `cancelacion_detectada` (decía «no se creó ni movió nada en Clientify», y desde el 3-sep sí mueve deals) y el sticky `Doc` del handler.
- 🔴 **Hallazgo: el webhook de WhatsApp no valida la firma de Meta desde julio.** `META_APP_SECRET`, `META_APP_ID` y `META_HMAC_ENFORCE` **no existen en el contenedor** (`META_PHONE_NUMBER_ID` sí), así que `Validate HMAC Meta` devuelve `_hmac: sin_secreto` y `POST /webhook/wa-inbound` (path adivinable) acepta cualquiera. Un payload falso hace que el bot responda por WhatsApp al número que venga dentro: spam desde su WABA y contactos falsos; no hay fuga de datos. Meta sí manda `x-hub-signature-256`. **Orden**: rotar en Meta (pendiente desde el 17-jul) → env en Dokploy + redeploy → ver `_hmac: ok` → `META_HMAC_ENFORCE=true` → añadir `hmac_meta_invalido` a `CODIGOS_NEGOCIO`. Nunca encender enforce antes del paso 3.
- 🔜 Sigue pendiente del 3-sep todo lo de abajo (decisión a/b de los deals, vigilar el primer lead de voz, voz v31).

## Estado previo · 2026-09-03

**Doctoralia ya actualiza el lead en Clientify, y recepción tiene guía.** Lo abrió Olga: imprimía los avisos de voz sin saber qué hacer con ellos ni cómo buscar «deal 32108592». Agentes por modelo (Sonnet construye, Opus verifica); pruebas solo contra nuestro correo y teléfono.

- ✅ **Reserva en Doctoralia → todos los deals abiertos del lead a «1º Visita Programada»**, con nota «Cita Doctoralia: DD/MM/YYYY HH:MMh · servicio» y vencimiento = día de la cita; crea «Cita Doctoralia» solo si no había ninguno. Cancelación → «Volver a contactar» (+7 días); reprogramación actualiza la nota. → [[ADR-079-una-reserva-de-doctoralia-mueve-todos-los-deals-abiertos-del-lead]]
- ✅ **La rama de cancelación llevaba inerte desde el 15-ago**: leía `$input` detrás de un Postgres que emite `{success:true}`. → [[el-nodo-postgres-emite-success-true-cuando-el-returning-sale-vacio]]
- ✅ **WhatsApp: si motivo, nombre o relación llegan después de registrar, el deal se actualiza sin avisar dos veces** (`update_only` de `chatwoot-event` a `registrar-lead`, caché por `chatwoot_conv_id`). El caso «Marta» sin nombre: el bot preguntó y ella no contestó; el nombre de WhatsApp sí queda en la ficha.
- ✅ **Guía para recepción con 7 capturas** (artifact «Guía Clientify Elphis», privado hasta compartirlo) y mensaje de respuesta entregado. Lo esencial: el aviso no significa «atendido»; buscar por teléfono o `app.clientify.com/deals/<id>/`; deal en «1º Visita Programada» con nota de Doctoralia = ya tiene cita.
- 🔴 **Incidente propio (13:08)**: la primera prueba de `registrar-lead` mandó WhatsApp y email reales a recepción con datos ficticios — el flag no estaba en el schema del trigger. Regla en [[n8n-executeworkflowtrigger-schema-estricto-filtra-campos]].
- 🔴 **Dos fallos reales tras desplegar, corregidos el mismo día**: PATCH 400 por pipeline (el POST lo ignora; 88 deals viejos inconsistentes, sin backfill por decisión) y bigint en leads de voz (`conv_id` `postcall-…`). El deal real 32290400 se reparó con replay del payload. → [[clientify-post-deals-ignora-pipeline-y-un-patch-parcial-reevalua-etapa-y-vencimiento]] · [[un-agente-que-reporta-fallo-por-529-puede-haber-terminado-el-trabajo]]
- ⚠️ **Los emails «Contacto creado desde API» de Clientify se quedan** (decisión 3-sep): aviso estándar del CRM por contacto nuevo.
- 🔜 **Tuyo, bloqueado por el clasificador de auto-mode** (escritura a deals reales): (a) aplicar la cita del 08/09 10:00 a los 3 deals de Camilo (32109777 / 32109813 / 32109765); (b) cerrar como Lost los ~10 deals de prueba del contacto 161749243. Las etiquetas de prueba solo se quitan desde la UI.
- 🔜 **Vigilar el primer correo real de Doctoralia y el primer lead de voz** por el código nuevo (`doctoralia-email-sync` / `registrar-lead`).
- 🔜 Sin construir, opciones abiertas: aviso diferido 30 min con «ya tiene cita / pendiente de llamar»; dejar de crear el deal «Primera visita» al mandar el enlace; dedup de contactos por email en `clientify-upsert-contact`.
- 🔧 Backups pre-cambio de los 5 workflows en el scratchpad de la sesión (`backup-<id>-pre-*-20260903.json`); gotchas de la API en [[clientify-discovery-elphis]].

## Estado previo · 2026-08-29

**v31 publicada y servida.** Salió de auditar las últimas llamadas reales: el nombre no llegaba al CRM
en llamadas de familiares, Laura se despedía dos veces, insistía explorando y quedaba guion residual.
Seis parches escritos, **dos descartados por medida propia**.

- ✅ **Se va el guion «Encantada, X»**: 10/45 → **0/45**. Era la última percha entrecomillada viva.
- ✅ **El aviso de coste deja de ir pegado al turno del nombre**: 28 % → **11 %**. Lo consigue la
  condición de parada de la exploración, no el parche del coste (sin ella vuelve al 31 %).
- ✅ **Crisis 12/12** frente a 10/12 de la base. Regresión igual: 41/45 en ambos.
- ❌ **Prohibirle despedirse a un nodo, descartado**: `cierre` tiene que producir turno, así que en vez
  de callar recitó la instrucción al paciente. → [[prohibirle-a-un-nodo-que-hable-hace-que-recite-la-instruccion-en-voz-alta]]
- ❌ **Salida por línea ininteligible, descartada**: derivaba a devolución de llamada a gente a la que
  sí se entendía.
- ⚠️ **Cuatro horas de medición contaminadas** por comparar borradores contra la versión publicada; el
  borrador no-op idéntico a v29 sacó 64 %, no 83 %. → [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]]
- 🔜 **La doble despedida real sigue viva y es estructural**: `cierre` habla y `despedida` repite. Se
  arregla con aristas, no con prompt, y necesita su propio lote medido.
- 🔜 **Nombre perdido en llamadas de familiares**: la suite simulada no lo reproduce (8/9 lo capturan),
  así que P1 quedó sin validar. Hace falta un caso de prueba que lo reproduzca antes de tocar nada más.
- 🔜 **Para Enrique y Alba**: qué responde el centro ante situación irregular y ante barrera idiomática.
- 🔧 Vuelta atrás en una orden: `v30/ROLLBACK.sh 29` (verifica sola qué queda sirviendo).

## Estado previo · 2026-08-28

**Laura deja de recitar: v29 publicada y servida.** Lo abrió Manu tras una llamada real: «dice *cannabis entonces*, me ha dicho porros… es como que no da conversación natural». No era la voz ni el modelo, era el prompt. Ciclo medir-corregir-remedir de **8 configuraciones y 231 llamadas simuladas**; el número no fija versión, así que republicar una vieja es rollback completo (`ROLLBACK.sh 21`).

- ✅ **La causa dominante eran las comillas del prompt.** Turnos que reproducen una frase palabra por palabra: **32,6 % → 18,2 %**. Las frases de ejemplo se convierten en «cosas que transmitir, no un texto que recitar»; se declaran literales solo el aviso del art. 50, las frases de crisis y la fórmula de consentimiento. → [[las-frases-entrecomilladas-de-un-prompt-son-un-guion-que-el-modelo-recita]]
- ✅ **Usa SU palabra**: si el paciente dice «porros», Laura no le contesta «cannabis». Corregirle el vocabulario le coloca en el papel de paciente antes de tiempo.
- ✅ **Un turno para entender antes de pedir nada.** Al oír la sustancia ya no salta al siguiente campo del formulario: una pregunta abierta construida sobre lo que acaba de decir, y esa respuesta se usa después para ofrecer la primera visita conectada con lo suyo. Exploración real 3 → 4 de 21.
- ✅ **Faltaba la salida de despedida.** El grafo era alcanzable (BFS: 0 nodos atrapados en v21 y v29) pero ninguna condición disparaba con un «gracias, ya está». Tres aristas nuevas, **añadidas al final** para no pisar la prioridad de las de crisis. Fugas de conversación **3 → 0**. → [[un-grafo-alcanzable-no-prueba-que-se-pueda-salir-la-trampa-esta-en-la-condicion]]
- ❌ **Temperatura 0,6 descartada, medida**: rompió 2 de 21 llamadas en nodos que no se habían tocado — la temperatura evalúa también las condiciones de arista. Se queda en 0,22. → [[subir-la-temperatura-de-un-agente-de-voz-le-rompe-el-enrutado]]
- ❌ **`claude-4.6-sonnet` descartado**: sin ganancia medible sobre haiku 4.5, y cuesta latencia y dinero.
- ⚠️ **Pedía el consentimiento dos veces** (v27): la fórmula estaba en el `global_prompt` y en su nodo. Mismo error que la sesión anterior. Ahora vive solo en el nodo. → [[repetir-una-instruccion-en-el-prompt-global-y-en-el-nodo-la-ejecuta-dos-veces]]
- 🧪 **Suite: ±2 casos de ruido.** v21 sin tocar dio 7/9, 9/9 y 8/9; la de crisis en v29, 11/12, 11/12 y 12/12 fallando un caso distinto cada vez. No se declara ganador por un punto. Y el juez sigue mintiendo: en el caso 06 dijo «insiste en pedir el nombre» en una transcripción donde no lo pidió ni una vez.
- ⚠️ **El eco sigue ahí, y es infraestructura**: 4 de 4 llamadas reales, siempre durante la presentación — el ASR transcribe la voz de Laura como si fuera el paciente. Mitigado con una regla de cabecera («si oyes tu propia voz, es la línea»), pero **bloquea subir `interruption_sensitivity`**: subirla la haría interrumpirse a sí misma. **Pregunta abierta a Manu: ¿llamas con manos libres?** Si sí, es acoplamiento acústico; si no, es el trunk del `+34910054950`.
- ⏭️ **Sin tocar a propósito**: `voice_model` (`eleven_flash_v2_5` → `eleven_multilingual_v2`) se probará solo, para poder juzgarlo de oído.

## Estado previo · 2026-08-27

**Auditoría y arreglo integral del agente de voz (Laura, Retell).** Lo abrió Alba: «es muy lenta, entra en bucle con el saludo, las transferidas no llegan a recepción». Agente `agent_e21120298343bc2ef8b4a535c9`, flow `a42bf76dcfa0`, **v15 publicada** y servida (el número no fija versión). Suite de simulación **9/9**.

- ✅ **Latencia e2e 2.720 → 1.859 ms** (mediana de p50 sobre 40 llamadas partidas por versión); el TTS solo, 686 → 175 ms.
- ✅ **El bucle del saludo tenía dos causas**, no una. (a) Eco: el ASR transcribía la propia voz de Laura como si fuera el usuario. (b) `welcome` era `static_text`, así que **volver a entrar en el nodo reemitía la frase** — y se volvía a entrar porque, como intuyó Alba, la gente dice "hola, ¿hay alguien?" durante la espera. El eco está mitigado, no eliminado: si vuelve a partirse en una llamada real, apunta al trunk de Netelip.
- ✅ **Colgaba sin despedirse**: los nodos `end` de Retell no hablan. Nodo `despedida` propio. → [[retell-el-nodo-end-no-habla-la-despedida-necesita-nodo-propio]]
- ✅ **El "bucle del nombre" que reportó Alba era una condición de arista**, no el prompt: la única salida de `intake` exigía el nombre, así que quien no lo daba veía a Laura pedirlo cuatro veces ignorando sus preguntas. → [[retell-la-condicion-del-edge-manda-sobre-el-prompt]]
- ✅ **Opción 2 de Alba implementada**: no se transfiere a recepción, se recogen datos y se avisa al equipo. La frase *"te paso con nuestro equipo"* sobrevivía en las transiciones y ahora es prohibición dura del `global_prompt`, con la de no pedir el teléfono (ya se conoce de la llamada). `recepcion_transfer` queda huérfano a propósito, por si se reactiva. → [[prohibir-una-frase-en-un-nodo-no-cubre-lo-que-se-dice-al-transicionar]]
- ✅ **No dejaba colgar**: ante "gracias, que tengas un buen día" respondía *"Espera un momento, antes de que cuelgues…"* y volvía a ofrecer la cita, hasta cuatro veces. No lo pedía ningún prompt. Salió leyendo transcripciones de casos que PASABAN. → [[la-transcripcion-de-un-test-que-pasa-es-donde-esta-el-defecto-que-nadie-mide]]
- ✅ **Falso 112**: mandaba a urgencias a quien solo describía su consumo con normalidad. Nodo `estado_afectado` acotado; caso 07 de la suite lo cubre.
- ✅ **Las reservas volvían vacías**: los `args` de la tool llegaban como `{}` o con `{{dv_x}}` literales. Propiedades con `const` en la custom function (las aplica Retell, no el LLM) + guard que descarta variables sin resolver y valores basura ("sin nombre", "ninguno") en los dos `retell-tool-*`. Verificado en la ejecución 10595: `motivo`, `relacion` resueltos, `link_enviado: true`, `wamid` real.
- ✅ **Consentimiento RGPD en voz**: vivía dentro de un nodo `function` (mudo), así que **no se pedía nunca**. Nodo `consentimiento` propio antes de extraer datos.
- ✅ **Dedup de deals muerto desde julio**: `ON CONFLICT DO NOTHING` no refrescaba la fila caducada, 26 claves en ese estado. → [[on-conflict-do-nothing-nunca-refresca-una-fila-caducada]]
- ✅ **Alerta si el enlace no sale**: `reservar_visita` devolvía `ok:true` aunque el WhatsApp fallara. Ahora `ok` exige `link_enviado` y el código `enlace_no_enviado` entra en el error-handler.
- 🧪 **Suite de 9 casos** en Retell (handoff, crisis, ingreso, reserva, saludo pisado, nombre ininteligible, falso 112, composición de sustancias, confidencialidad). Tres daban `ERROR` por el usuario simulado, no por el agente. → [[un-usuario-simulado-sin-condicion-de-salida-se-reporta-como-error-del-agente]]
- ⚠️ **Sin ejercitar aún en llamada real**: despedida, nodo de consentimiento, tope de dos intentos con el nombre, fuera de horario, texto de `recepcion_aviso`, fallback de nombre en Clientify y la alerta `enlace_no_enviado`. La simulación los cubre; el trunk no.
- ⚠️ **Decisión pendiente tuya**: mover precios y horarios a la knowledge base ahorraría ~180 ms, pero con `filter_score: 0.6` una consulta por debajo del umbral deja a Laura sin poder citar precios. No aplicado a propósito.

## Estado anterior · 2026-08-18

- ✅ **Ya no se presenta en cada mensaje (18-ago tarde).** Lo reportó Alba: «se presenta 17 veces en la misma conversación». La marca `ia_disclosed` vivía en los `custom_attributes` de Chatwoot, pero el nodo que los escribía los **reconstruía**, y ese endpoint reemplaza en vez de fusionar: duraba un turno. Se llevaba por delante también `clientify_*` y `bot_paused` (una conversación pausada podía despertarse sola). Al verificarlo salió un segundo defecto —la frase literal estaba en el prompt y el modelo la copiaba: salía dos veces— y un tercero: el aviso abre con «Hola» y el modelo abría con el suyo, dos saludos pegados; ahora el nodo recorta el saludo de apertura. Probado end-to-end por el webhook real, dos turnos. → [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]
- ✅ **No se dan horarios de primera visita (18-ago tarde).** Lo pidió Alba: la disponibilidad la ve el paciente en el enlace. La regla ya existía, pero 157 líneas por debajo del horario del centro y dentro de «Flujo de reserva»; a un "horario de visitas" el modelo no estaba reservando y sirvió el horario del centro. Aviso pegado al dato: **2/5 → 0/5** medido contra la API real. Su segunda petición —«si en el enlace no encuentran hueco, que nos lo digan»— se pidió primero al prompt (0/5) y acabó en el **texto fijo** del mensaje del enlace (`book-and-notify` → `Build enlace`), donde sale siempre. Pendiente: en **voz** ese texto es la plantilla HSM `elphis_cita_link` y hay que recrearla en Meta. → [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]]
- ✅ **Avisos de lead por canal, EN PROD (18-ago).** Dos plantillas HSM aprobadas — `elphis_lead_llamada_v2` (voz) y `elphis_lead_whatsapp` (chat) — con 7 datos: nombre, teléfono, motivo, relación, urgencia, tipo y **resumen**. Antes había una sola y decía «a través del bot de WhatsApp… revísalo en Chatwoot» viniera de donde viniera: el 17-ago mandó a Alba a buscar en Chatwoot un lead que había **llamado**. La de voz cierra en «Ficha completa en Clientify», sin mencionar el canal que no es. Verificadas con envío real al móvil de Manu. → [[plantilla-hsm-por-canal-y-lo-que-la-manda-a-revision-manual]]
- ✅ **El bot vuelve a tener memoria.** `conversation_state` tenía **8 filas y ninguna de agosto**: `Upsert conv_state` fallaba en cada mensaje con el `bigint: "null"` que se arregló el 12-ago **solo en su nodo gemelo**, y `onError: continueRegularOutput` lo hacía mudo. Cada turno llegaba con `paciente_data: {}`. Probado contra la BD real con `BEGIN/ROLLBACK`. → [[un-guard-envejece-por-partes-arregla-una-regla-y-sus-hermanas-siguen-rotas]]
- ✅ **La ficha de Clientify ya cuenta algo.** Contacto con nombre real —o `Lead voz <tel>` si no lo dio, sin pisar nunca un nombre que sí se sabía—, etiquetas `canal_*` y `motivo: *`, y descripción con canal, motivo, relación, urgencia, tipo, «Nombre en WhatsApp» y **resumen**. El resumen de Retell existía y se quedaba en el webhook; en chat no existía y ahora lo genera la extracción. La nota del deal salía pegada sin saltos porque `sanitize` se comía los `\n`.
- ✅ **Voz: ASR calibrado y guion que pide el nombre antes** (agente v5). «Juego» se transcribía «jueves» y el agente contestó *«Perfecto, anotado para el jueves»* sin haber anotado nada: `stt_mode: accurate`, 38 palabras potenciadas del dominio, cancelación de ruido, y regla nueva de no dar por buena una palabra que no encaja ni decir que ha anotado algo. El nombre se pide en cuanto se conoce el motivo — el lead del 17-ago colgó tras 2 min 44 s sin darlo porque el guion lo dejaba para el final.
- ✅ **`dry_run` vuelve a ser seguro**: estaba clavado a `false` en `retell-tool-crear-lead`, así que un smoke mío creó lead real y avisó a Alba. → [[un-flag-de-dry-run-que-el-reenviador-ignora-convierte-el-smoke-en-produccion]]
- ⚠️ **Los teléfonos de prueba avisan al equipo.** La whitelist `+3460000009X` protege Clientify pero **no** las notificaciones: tres smokes míos del 17-18 ago le sonaron el móvil a Alba. Guard propuesto (que se registren pero no notifiquen) — **pendiente de tu OK**.
- ⚠️ **Lo que sigue sin cubrir**: quien reserva en Doctoralia **sin haber escrito nunca por WhatsApp** no tiene fila en `conversation_state`, y el sync escribe con `UPDATE … WHERE phone`, así que su cita no se guarda en ningún sitio. Arreglarlo pide tabla de citas propia y contradice [[ADR-053-la-cita-de-doctoralia-vive-en-conversation-state]] — **decisión tuya**.
- ⚠️ **El repreguntar el motivo YA estaba arreglado** (15-ago): medido contra la API real reproduciendo el turno, 0/5 y 0/5. Lo que se vio era una conversación del 11-ago, anterior al fix. → [[antes-de-arreglar-lo-que-viste-en-un-log-mira-contra-que-version-paso]]

## Histórico · 2026-08-17

- ✅ **Los dos canales ya se identifican como IA, EN PROD (17-ago).** Lo pidió Alba tras una llamada de prueba del comercial de Movistar y antes de activar el desvío del fijo; entró en vigor el 2-ago el art. 50 del AI Act. Ninguno de los dos decía nada: voz abría con *"Hola, estás llamando a Centro Elphis"* y el chat solo se declaraba "agente virtual" al negarse a hablar de sustancias.
  - **Chat**: nodo Code `Aviso IA primer contacto` en `chatwoot-event`, entre `Call router-ia` y `Post reply` — prefija *"Hola, soy Laura, la asistente virtual con IA de Centro Elphis."* y marca `ia_disclosed` en los `custom_attributes`. **Determinista a propósito**, y la marca en los attrs y no en el historial (Chatwoot solo devuelve 20 mensajes). Probado con 5 casos en local; sin drift de posiciones.
  - **Voz**: nodo `welcome` del flow `a42bf76dcfa0` + regla de identidad en el `global_prompt`; agente **v3 publicado** (sin `publish-agent` no llega a las llamadas). Aquí va "inteligencia artificial" desarrollado, no la sigla: el TTS lee inestable las de dos letras. **Llamada de prueba verificada por Manuel.**
  - Ambos prompts llevan además la regla de no afirmar nunca ser una persona. → [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]] · [[n8n-put-solo-acepta-executionorder-en-settings-y-conserva-el-resto]]
  - ⚠️ **Falta el smoke del chat**: no entra un mensaje desde el 11-ago, así que el aviso de WhatsApp sigue sin ejercitarse en camino real. Un WhatsApp desde un número nuevo lo cierra — y de paso estrena las 15 correcciones de agosto.

## Histórico reciente · 2026-08-15

- **Auditoría de calidad de las conversaciones del bot (39 en Chatwoot, 28 con transcripción, 6-jul→11-ago) y 12 correcciones aplicadas.** El guion comercial funciona (8 de 28 acaban con enlace de cita, precios siempre correctos, filtra bien spam/empleo/intento de compra de droga); fallaba lo de alrededor. Aplicado en `router-ia`, `chatwoot-event`, `book-and-notify` y `doctoralia-email-sync`, con backup previo y sin drift de posiciones.
  - ✅ **El bot ya puede confirmar una cita.** Era el peor: un paciente en recaída preguntó si su cita de mañana estaba bien puesta y se llevó *"no puedo acceder a la información de las reservas"*. `doctoralia-email-sync` extraía la fecha pero solo la escribía en Clientify. Ahora la persiste en `conversation_state.paciente_data.cita` (dos nodos: uno para la cita y **otro para las cancelaciones**, que el guard mandaba a skip) y el router se la pasa al LLM ya formateada y clasificada (PENDIENTE / PASADA / CANCELADA / NINGUNA). → [[ADR-053-la-cita-de-doctoralia-vive-en-conversation-state]] · [[el-estado-derivado-tambien-hay-que-sincronizarlo-en-la-rama-que-descarta]]
  - ✅ **«Segunda visita» ya dispara el handoff.** Cierra el «revisar con volumen» del 04-ago: el regex de contacto previo no cubría *"¿podría ser mañana esa segunda entrevista?"* y a esa persona se le mandó el enlace de **primera visita gratuita** siendo ya paciente. +4 patrones, 33 casos de test con 15 mensajes reales de leads nuevos como control. → [[regex-word-boundary-no-casa-acentos-js-normalizar-nfd]]
  - ✅ **Consentimiento RGPD**: una paciente respondió *"Ansiedad"* a *"¿estás de acuerdo?"*, el bot lo tomó por un sí y envió el enlace. Ahora exige sí explícito.
  - ✅ **Muro de confidencialidad separado del cajón de sastre**: preguntar por un hijo ingresado y un spammer de SEO recibían la misma frase. Ahora confidencialidad = texto propio + `pause_bot` siempre (aviso a Alba); publicidad = corte seco **sin** handoff, para no generar avisos basura.
  - ✅ **«Estoy esperando en el enlace»** (una persona plantada en la consulta; el bot improvisó *"a veces tarda un poco"*): pre-check determinista → aviso etiquetado `URGENTE, paciente esperando`. Los patrones exigen "**en** el enlace", no "el enlace": *"estoy esperando el enlace"* lo sigue resolviendo el bot reenviándolo.
  - ✅ **Enlace duplicado** (una paciente recibió 4 en un minuto): guard idempotente en `book-and-notify` con `slot_lock`, ventana de **90 s** — el número sale del corpus, no de la intuición: la ráfaga cayó en el mismo minuto y el reenvío legítimo de *"no me ha llegado nada"* fue a los 2 min, así que 10 min habrían roto un caso bueno. Fail-open a propósito (perder una cita por un lock caído es peor que un enlace repetido); contrapartida: un fallo del lock es silencioso.
  - ✅ **Saludo del enlace a familiares**: llegaba *"Hola Miguel, reserva **tu** primera visita"* al móvil del padre. Ahora neutro si `relacion=familiar`. La plantilla HSM de voz sigue con el nombre del paciente (texto aprobado por Meta, no se cambia sin re-aprobación).
  - ✅ **Respuesta vacía** (`Post reply` posteaba `reply_text` sin validar → burbuja en blanco) y **retirada de benzos/alcohol/opioides** siempre bajo supervisión médica — esto último **que lo valide Enrique**, es criterio clínico.
  - ✅ **Cambiar o anular una cita** (salió al repasar las 11 conversaciones viejas que quedaban, conv 17 del 8-jun): el bot respondía *"no puedo acceder a la información de citas, llama al centro al 659 877 708"* — **el mismo número desde el que la persona escribe** — y el equipo no se enteraba de que ese hueco quedaba libre. Ahora es el tercer disparador determinista del pre-check, con aviso `Quiere cambiar o anular su cita`. 19 casos de test.
  - ✅ **El consentimiento RGPD ya NO depende del modelo.** Guard determinista en `Tool prep`, justo antes de ejecutar `book_visit`: vale si el mensaje que dispara la reserva es una afirmación explícita, o si antes el bot pidió consentimiento y el usuario dijo que sí. Si no consta, **no cancela**: devuelve `CONSENT_REQUIRED` y el modelo vuelve a preguntar (un turno, cero leads perdidos). Calibrado contra las 9 conversaciones reales que llegaron a reservar: pasan 7/7 las que tenían un sí claro, frena "Ansiedad" y un "Di". → [[una-regla-de-prompt-que-el-modelo-cumple-a-medias-suele-ser-decidible-en-codigo]]
  - ✅ **El bot ya no da ningún teléfono.** El 659 877 708 salió del prompt: es el mismo WhatsApp por el que escribe la gente, así que "llama al centro" no tiene sentido. Cambiar/anular cita responde *"Lo traslado al equipo y te llaman enseguida a este mismo número"* y entra en Clientify + WhatsApp a Alba + email como cualquier otro lead (vía `registrar-lead`, `tipo_consulta:handoff` → `destino:recepcion`). Los únicos teléfonos que quedan son los de crisis (112 / 024 / 717 003 717), a propósito.
  - ✅ **Recordatorio final de 7 reglas al cierre del prompt** (efecto de recencia), con lo que más se salta: consentimiento, no dar teléfono, confidencialidad, sustancias, no repetir enlace, no decir que no puede ver las reservas, formato.
  - ⚠️ **El prompt del router ha crecido un 33% hoy** (3.4K → 4.5K tokens, 25 secciones). El coste es despreciable, pero `gpt-4o-mini` con un prompt así se salta reglas más fácilmente. Mitigado en parte porque lo crítico (crisis, contacto previo, espera, cambio de cita) es **regex determinista, no prompt**; lo que sigue colgando del modelo es confidencialidad, consentimiento, uso de la cita y aviso de benzos. Si aparecen incumplimientos con volumen: subir el router de modelo o bajar más reglas a pre-check, en ese orden.
  - 🟠 **Los TRES canales callados a la vez, y ninguno por avería.** Voz sin llamadas, Doctoralia sin correos desde el 3-ago, WhatsApp sin mensajes desde el 11-ago 12:35. Se verificó cada uno por separado y los tres están sanos: eso es justo lo que descarta el fallo técnico — son independientes (Retell, IMAP, Meta) y no comparten dónde romperse a la vez. **La pregunta pasa a ser de negocio: ¿se ha parado publicidad, ha cambiado algo en la web o en la ficha de Google?** → [[tres-canales-en-silencio-a-la-vez-es-demanda-no-averia]]
  - ⚠️ **Efecto colateral: las 15 correcciones del bot siguen sin estrenar.** No entra un mensaje desde el 11-ago 12:35 (última ejecución de `wa-inbound-bridge`), con el canal sano (`CONNECTED`/`GREEN`, app suscrita al WABA). Encaja con el silencio de Doctoralia desde el 3-ago: huele a agosto, pero hay que probarlo. **Un WhatsApp al 659 877 708 valida casi todo de una sentada**; para las citas, además reservar en Doctoralia con ese número.
  - Dos trampas que me tendí solas, por escrito: [[un-campo-descriptivo-puede-ser-de-enrutamiento-grep-antes-de-rellenarlo]] · [[una-regla-de-prompt-condicional-dispara-en-toda-la-poblacion-si-el-defecto-la-cumple]]
  - Confirmado de paso: lo del **tussi ya estaba cerrado** (regla dura 7 del prompt, con el argot listado) y el bug del `bigint`, también.

- **El aviso naranja diario del trigger IMAP, silenciado (16-ago).** Salía cada día a las 08:0x CEST, siempre por el corte de Webempresa, y siempre lo arreglaba solo el `imap-watchdog` a las :20 — un canal de incidencias con ruido diario predecible se acaba ignorando. `error-handler-global` marca ahora ese caso como ruido previsto (**solo** `doctoralia-email-sync` + `IMAP Trigger` + ventana 05:50-06:30 UTC; una caída a otra hora avisa igual) y no lo manda a Slack; se sigue registrando en `error_log`. El escenario accionable lo cubre el watchdog, que avisa **en rojo** si NO consigue reactivarlo. Probado con el payload real del aviso de hoy y 5 casos (dentro y fuera de ventana, y una ejecución rota del mismo workflow, que nunca se silencia). **Dependencia nueva a vigilar**: si el watchdog se parase, esta caída dejaría de avisar. → [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]]
  - El 🔴 del 15-ago 10:32 («sync de Doctoralia CAÍDO») **no fue un incidente**: era `zz-WD-victima` apuntando a un host inexistente, la prueba del camino rojo del watchdog. Ese workflow ya no existe.

- **El circuito de avisos, reparado de verdad; y debajo tres logs que no escribían nada.** El aviso diario «Nodo: sin nodo · unknown error» era un fallo del **trigger IMAP**: Webempresa corta la conexión en una **ventana fija diaria 06:02-06:08 UTC** (medida 5 días seguidos) — `forceReconnect: 60` no lo evita, se deja por inocuo.
  - ✅ **`error-handler-global` reescrito**: lee las dos ramas del Error Trigger, tres severidades con barra de color (rojo ejecución / naranja trigger / azul flujo previsto: `cancelacion_detectada`, `campos_minimos_faltantes`), dedup por severidad y queries a prueba de comas. Gate de 115 checks (mata con 8 mutaciones) en `~/Projects/elphis/avisos-20260814/`. Ver [[el-error-trigger-entrega-dos-payloads-y-el-de-trigger-no-trae-el-nodo]] · [[el-nodo-postgres-emite-success-true-cuando-el-returning-sale-vacio]] · [[queryreplacement-trocea-por-comas-todo-valor-que-no-sea-json]].
  - ✅ **Tres logs que no habían escrito NUNCA** (`wa-send::Log outbound`, `retell-post-call-webhook::Log call` y `::Log crisis`): credencial Postgres `R9aMmpO1jdJ8XPJP` inexistente **y** columnas que no existían, tapado por `onError: continueRegularOutput`. Se perdieron todos los mensajes salientes de WhatsApp, todas las llamadas y **todas las detecciones de crisis en voz**. `bot_outbound_log` ampliada (`phone`, `meta_message_id`, `response_status`, `payload_excerpt`); las 4 queries probadas contra la BD con valores con comas. Ver [[un-nodo-de-log-con-onerror-continue-puede-no-haber-escrito-nunca]].
  - ✅ **`imap-watchdog`** (`qQXVufU68Tj4mBeQ`, cada hora en el :20, tz Madrid): el corte puede dejar el trigger **desregistrado con `active: true`** (n8n reintenta 5 veces y calla). Fuerza desactivar/activar y verifica con el **código HTTP del `activate`** (400 = no conecta, con la causa); silencio si todo bien, rojo si no lo consigue. Probado en los dos caminos. Cred `n8n-api-elphis` (`xfHenPvyWG56Vukb`). Ver [[un-trigger-puede-quedar-muerto-con-el-workflow-en-active-true]].
  - ✅ El bug del `bigint` de `chatwoot-event` **confirmado cerrado** (la query desplegada ya lleva el `NULLIF`; sin errores desde el 11-ago).
  - 🟠 **Doctoralia lleva desde el 3-ago sin mandar un solo correo** (23 procesados en 30 días, 0 en los últimos 7). No es técnico: el sync está vivo (captó un correo en 4 s) y Clientify responde 200. **Preguntar a Alba si ha habido reservas por Doctoralia desde el 3-ago**; si dice que sí, mirar config de Doctoralia o si alguien los abre en el webmail antes (el trigger solo coge los NO leídos).
  - ⚠️ El ruido horario de `workflow_history` en el log **no** se quita con `N8N_WORKFLOW_HISTORY_PRUNE_TIME=-1` (en Community manda el límite de licencia): solo actualizando n8n.

## Histórico reciente · 2026-08-12

- **Auditoría completa del bot. Todo lo encontrado, cerrado salvo el canal de voz.**
  - ✅ **`chatwoot-event` ya no falla** (era el 🔴 desde el 3-ago, 55 errores en 14 días): `queryReplacement` mandaba el TEXTO `"null"` y `$3::bigint` cascaba antes del `COALESCE`. Fix `NULLIF(NULLIF($N,'null'),'')`, probado con `BEGIN/ROLLBACK` contra la BD (rojo con la vieja, verde con la nueva). **Impacto real mucho menor del que decía la ficha**: 54 de 55 respondieron al paciente y liberaron el lock — reventaba en el último nodo, solo perdía persistir ids. Limpiadas 5 filas con `'null'` literal en `conversation_state`. Ver [[una-expresion-que-evalua-a-null-viaja-como-el-texto-null]].
  - ✅ **Avisos de error a `#01-incidencias`** (bot `n8n_aia_bot`, dedup 60 min por workflow+nodo) y handler asociado a **28 de 28** workflows — antes estaba en 2. El montaje pasó nueve checks y **no avisaba**; se detectó leyendo el canal. Ver [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] · [[n8n-error-handler-global-via-errorworkflow]].
  - ✅ **Desactivados 4 webhooks vivos de la fase de pruebas**, uno peligroso: `purge-idem` era un `TRUNCATE` de `idempotency_log`+`slot_lock` **sin autenticación**. También los dos test-runners y `retell-tool-buscar-huecos`. Ver [[el-utillaje-de-pruebas-se-queda-encendido-en-produccion]].
  - ✅ Sanos: certificados hasta el **17-oct** (la nota decía agosto), env de avisos correcto en runtime, suscripción del webhook de Meta activa, disco al 32%.
  - ~~🔴 ÚNICO CABO: el canal de voz.~~ ✅ **CERRADO 15-ago: no ha habido llamadas** (confirmado por Manuel), así que no era el webhook de Retell ni había leads de voz perdiéndose. `retell-post-call-webhook`, `retell-tool-reservar-visita` y `retell-tool-crear-lead` llevan 14 días a **cero ejecuciones**. O no ha entrado ninguna llamada, o el webhook de Retell no llega y se están perdiendo los leads de voz. Se cierra con `POST /v2/list-calls` filtrando por los tres `agent_id` de Elphis.
  - Los cuatro `agenda-*` siguen activos y sin uso desde el rediseño de junio: son sub-workflows (no exponen URL), se dejan por si vuelve la reserva desde el bot.

## Histórico

- **10-ago: los avisos internos de lead no llegaban al equipo, por dos causas.** (1) `ELPHIS_NOTIF_INGRESO`/`_RECEPCION` seguían con el móvil del dev porque «el número de la recepcionista» figuraba como pendiente… cuando **el de Alba llevaba en §Datos clave desde mayo**; ahora ambos en `+34687448210` y el email en `info@centroelphis.com`. (2) El `else` de `Decidir etapa` ponía `destino='none'` y ahí caían el default `'info'` y cualquier `tipo_consulta` inventado por el LLM: 65 de 73 ejecuciones sin avisar a nadie, todo en `success`; cambiado a `destino='recepcion'` sin tocar la etapa de Clientify. Verificado E2E (`wamid` de Meta + `250` del SMTP) y con tráfico real el 11-ago. Volumen: **13 personas en 14 días, pico de 4/día** — contar ejecuciones en vez de personas infla ×10. `notify-cita-confirmada-email` desactivado por huérfano. **Limpiar en Clientify**: contacto `170386983` / deal `31693026`. Ver [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]] · [[workflow-activo-no-significa-llamado-grep-su-id-antes-de-editarlo]].

- **04-ago: bot de chat contestando composición/efectos de sustancias (Alba: «el tussi lleva heroína») y sin avisar cuando alguien decía «ya tuve visita» — ambos corregidos en `router-ia`.** Sustancias: regla dura en el prompt, 4/4 en vivo contra la API real (prompt-only vale aquí porque no hay acción externa). «Contacto previo»: prompt-only NO garantizaba el aviso (0/3 y 1/2 llamando a `pause_bot`), así que se añadió nodo determinista `Contacto previo pre-check` (regex, patrón de `Crisis pre-check`) + rama a `registrar-lead`, 9/9 casos. Voz corregida igual (agente `Laura ... Flow v4` `agent_e21120298343bc2ef8b4a535c9`, flow `conversation_flow_a42bf76dcfa0`, número **`+34910054950`**), con el caveat de que Conversation Flow no admite capa determinista (transiciones `type: prompt`). ~~Regex de «contacto previo» es primera pasada, revisar con volumen.~~ ✅ **revisado 15-ago** con 28 conversaciones reales: le faltaba «segunda visita» (ver Estado actual). Ver [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]].
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
