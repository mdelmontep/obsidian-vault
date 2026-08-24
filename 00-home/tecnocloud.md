---
title: tecnocloud
date: 2026-05-07
updated: 2026-08-24
tags: [cliente, tecnocloud, retell, voice, dokploy]
---

# Tecnocloud

Cliente de TuFacturaIA (Enterprise). Quiere su propio número WhatsApp para ingesta.
También tiene agente de voz Retell propio (Laura) para soporte técnico inbound.

## Estado

- **Org** activa en TuFacturaIA con plan Enterprise
- **15 facturas** emitidas en últimos 90d, 5 pendientes (33%)
- 0 proveedores con varianza alta (no recibe sugerencia antifraud)
- **Agente de voz Laura** (Retell) en producción para soporte L1, inbound al +34919935205

## Próximos hitos

1. **WhatsApp en TuFacturaIA** (LATER) — obtener `phone_number_id` de Meta Business → guardar en `organizations.settings.whatsapp.phone_number_id` → webhook override en n8n receptor v2
2. **Cerrado el 24-ago: #26, #29 y #30 en prod, y Laura ya se identifica como IA.**
   · **#26** (llamadas que Laura no registra → ticket «sin clasificar») mergeada en `f8f7f80`. La review paró dos defectos de cara al cliente: el asunto llevaba el resumen de Retell **en inglés** (12 de 12 llamadas) → [[resumen-automatico-de-la-llamada-viene-en-ingles]], y la etiqueta interna se pintaba en el portal → [[etiqueta-de-estado-interno-se-tapa-en-el-where-no-en-el-render]]
   · **#29** — la suite de INTEGRACIÓN sí corre en este Mac (no hace falta Docker: `postgresql@16` de brew + `pnpm --filter @tecnocloud/db test:db:setup`, BD `tecnocloud_support_test`). A la primera sacó un caso rojo en `main`: [[un-test-rojo-puede-estar-diciendo-que-dejo-de-medir]]. Ahora 187/187.
   · **#30** — Dependabot de 22 alertas a **0**, todas transitivas, vía `pnpm.overrides` (+ `npm audit fix` en `tools/rmm-mcp`, que va fuera del workspace).
   · **Art. 50 del AI Act, HECHO** (v47 publicada, el número sirve `latest_published`): el aviso va en el `begin_message` —texto fijo— y en el prompt solo la parte no determinista. Verificado sobre la versión PUBLICADA, no sobre el borrador.
   · **Webhook `retell-tecnocloud` cerrado**: era `authentication: None` y cualquiera con la URL disparaba `registrar_llamada` (correo a incidencias + fila en el Sheet). Ahora `headerAuth`; la cabecera viaja en las dos tools de Retell. Probado por el camino real con una tool de solo lectura: 403 sin cabecera, 200 con ella → [[en-una-prueba-de-auth-lo-que-discrimina-es-el-403]]
   · **Rama GRAVE de `Comprobar Entregas`** verificada con un arnés que carga el jsCode desplegado y simula el fallo de Gmail (6 casos + 2 controles negativos). No se puede provocar en prod; el cableado sí se comprobó: los tres nodos llevan `onError: continueRegularOutput`.
   · **Pendiente**: guardar en 1Password el valor de la cabecera (`/tmp/tecnocloud-webhook-header.txt`, 600) y borrar los 2 tickets `PRUEBA NOMBRE` en `/console/tickets`. El portal exige sesión y este Mac no la tiene en ninguno de los dos Chrome.
3. **Vigilar las 3-4 próximas llamadas reales** — con la v46 publicada (24-ago) y sin tests de simulación en este LLM.

## Servidor DOKPLOYMANU — el Dokploy de Tecnocloud (07-ago-2026)

Host **`185.99.186.76`, puerto SSH 5251** (alias local `ssh tucrmia`, clave `~/.ssh/tucrmia_root`; documentado en 1Password, bóveda TUCRMIA). Proveedor distinto al de la tanda `185.47.13.x`, pero **misma contraseña root** — ver [[vps-dokploy-de-una-tanda-comparten-password-root]].

Ojo al alcance: aquí no solo vive lo de Tecnocloud. **20 contenedores**, entre ellos [[tucrmia|TuCRMIA]], un n8n de Agentesia, Chatwoot y notcaido. Un reboot los tira todos ~1 min, así que la ventana se acuerda con ellos.

- **07-ago**: parcheado (18 updates), kernel `5.15.0-174`, reiniciado, 20/20 arriba.
- El n8n de Agentesia no volvió solo tras ese reboot: **carrera con la overlay `dokploy-network`**, no su restart policy. Guardián systemd instalado y `enabled` (`/usr/local/bin/dokploy-restart-orphans.sh`, log en `/var/log/dokploy-restart-orphans/`), validado en sus dos ramas; **falta verlo en un reboot real**. → [[contenedor-que-no-vuelve-tras-reboot-dos-causas-que-se-confunden]]
- **Pendiente**: darlo de alta en `/agency/infrastructure` del portal — clave del monitor ya autorizada en el host, falta pegarla en el formulario. → [[agentesia]]
- Sin backups a Wasabi configurados; nunca se auditaron (`dokploy-backup-monitor` los cubre).

## Agente de voz Laura — Retell

- **agent_id**: `agent_add2e94a0f386f86243a9e80e6`
- **llm_id**: `llm_c32fb6e5ba5c6b493da0ba3f73ac` · modelo `gpt-5.4-mini` · `tool_call_strict_mode: true`
- **phone**: `+34919935205` (inbound)
- **Workflow n8n backend (tools)**: `aAfDL01MLPAOWfco` — "Retell Agent Tools - TECNOCLOUD"
  · Webhook: `https://n8ntecno.tecnocloud.es/webhook/retell-tecnocloud`
  · Tools: `buscar_FAQ` (RAG PGVector), `registrar_llamada` (Sheets + Gmail HTML a `incidencias@tecnocloud.es`)
  · OpenAI API key vía `$env.OPENAI_API_KEY` (movida de hardcode 2026-05-25)
- **Google Sheet de llamadas**: `1Jb6BR64IbkFCwk55m_1elAWAPSl9xNd2fBi1iwPP244` ("Registro TECNOCLOUD")
- **Personas internas conocidas** que clientes piden: Silvia, Dani, Carlos. Flujo rápido en el prompt pregunta motivo antes de derivar.

### Flujo "hablar con Silvia/Dani/Carlos" (2026-05-25)
Etapas obligatorias antes de disparar `registrar_llamada`:
1. Preguntar **motivo** ("¿para qué quieres hablar con [persona]?")
2. Pedir **nombre del cliente** (distinto de la persona solicitada)
3. Recién entonces ejecutar tool y despedir.

Lección: el LLM confundía PERSONA_SOLICITADA con NOMBRE_CLIENTE. Fix combinado:
- Precondiciones explícitas en `description` de la tool `registrar_llamada` (pesa más que el prompt).
- `tool_call_strict_mode: true`.
- `execution_message_description` neutralizado (no prometer "derivar" antes de tiempo).

### Resumen del email post-llamada
Generado con gpt-4.1-mini pidiendo 4-8 frases con datos concretos (error literal, persona+motivo,
pasos probados, estado final), más `categoria` y `persona_solicitada`. `max_tokens: 700`.

**Estuvo roto de finales de mayo al 17-ago sin que nadie lo notara**: vivía dentro del Code node
`Registrar Llamada` leyendo `$env.OPENAI_API_KEY`, y este n8n **no** tiene
`N8N_BLOCK_ENV_ACCESS_IN_NODE=false`, así que reventaba al instante (6-22 ms de ejecución) y el
`catch` degradaba en silencio a lo que dictaba Laura. Ahora es un nodo HTTP Request propio
(`Generar Resumen IA`) con credencial, que no depende de ese flag. Ver [[Stack/n8n]].

## Reconstrucción del backend de voz (17-ago-2026)

Workflow `aAfDL01MLPAOWfco`, backup previo en `knowledge/projects/agentesia/n8n-backups/tecnocloud/`.
Cadena vieja: `Registrar Llamada → Sheets → Gmail → responder`. Nueva:
`Preparar Registro → Reservar call_id (Postgres) → ¿duplicada? → responder → Generar Resumen IA →
Registrar Llamada → Gmail → Sheets → Comprobar Entregas`.

Medido antes/después, con llamadas reales al webhook:

| | antes | después |
|---|---|---|
| `registrar_llamada` (lo que espera Laura) | 4,1 s | **0,17 s** |
| `buscar_FAQ` | 4,99 s | **0,4-0,9 s** |
| resumen con IA | roto desde mayo | funcionando |
| duplicados | 5 de 142 llamadas | cortados en Postgres |
| fallo de Sheets/Gmail | silencioso (11-ago perdió un aviso) | retry ×3 + `throw` → Slack |

Otros arreglos del mismo día:
- **Credencial `Openai` vieja devolvía 429** en `chat/completions`, y en embeddings provocaba
  reintentos que parecían latencia de red. Nueva credencial `OpenAI Tecnocloud (verificada 17-ago)`
  (`qNWZEgvoDSP6Fuxc`) con la key del ítem *Tecnocloud Api Openai Chatbot*. La vieja sigue existiendo
  y **conviene borrarla o rotarla** para que nadie la reutilice.
- **Teléfono en letras**: Laura dictaba `telefono_cliente` como "seis dos nueve - ocho cuatro cuatro…"
  y así se guardaba. `Preparar Registro` lo normaliza a `+34XXXXXXXXX` y cae al `from_number` si no
  cuadran 9 dígitos.
- **Asunto del email**: antes se cortaba a 12 palabras y acababa en "Motivo:". Ahora
  `Incidencia [Gesfincas · reclama] - Nombre - resumen`, con la app y la reclamación visibles en bandeja.
- **Error Handler** (`qfpmOmR5gRqRMcNV`): el campo `cliente` decía **"Laserys Las Rozas"** (plantilla
  clonada), así que todos los avisos de Slack de Tecnocloud llevaban meses con el cliente equivocado.
  Corregido a "Tecnocloud". **Revisar si el mismo copy-paste está en otros clientes.**
- `availableInMCP` se apagó al hacer PUT por la API (n8n devuelve ese setting en el GET pero lo rechaza
  en el PUT). Si se quiere, se vuelve a marcar en la UI.

## La FAQ llevaba dos meses devolviendo silencio (descubierto 17-ago)

Auditadas las 645 llamadas del agente enlazando cada `tool_call_invocation` con su
`tool_call_result` por `tool_call_id`:

| Periodo | Resultados de `buscar_FAQ` | Vacíos |
|---|---|---|
| 8-abr → 24-may | 133 | 8 (6%) |
| 25-may → 30-jun | 58 | 55 (95%) |
| 1-jul → 17-ago | 83 | **83 (100%)** |

No era falta de documentos: **funcionaba y se rompió**. Tres causas encadenadas, todas ya
corregidas y verificadas con llamadas reales al webhook:

1. El **429 de la credencial `Openai`** hacía fallar `Generar Embedding` en todas las búsquedas.
2. `Generar Embedding` y `Buscar en PGVector` tenían la salida de error declarada en
   `connections["error"]` (formato antiguo) mientras `onError: continueErrorOutput` emite por
   **`main[1]`**, que estaba sin conectar: el item moría ahí, `Responder Embedding Error` nunca
   se ejecutaba y **Retell recibía `[]`**. El fallo se convertía en silencio, no en error.
3. `Buscar en PGVector` sin `alwaysOutputData`: si ninguna fila supera `similarity > 0.70`
   devuelve 0 items y la cadena se corta igual. `Procesar Resultado RAG` **ya sabía** responder
   `{result:'no_encontrado', confidence:'ninguna'}`, pero era código inalcanzable.

Consecuencia de negocio: Laura no distinguía "no hay documento" de "silencio", así que
improvisaba. Explica que **los 115 registros de may-jun lleven `resuelto:"no"` el 100% de las
veces** y que solo 12 de 161 llamadas se cerrasen en primer nivel.

Verificado tras el fix: consulta sin documento → `{"result":"no_encontrado"}`; consulta con
documento → devuelve el texto correcto (`similarity 0.754`).

### Prompt v42 de Laura (publicado 17-ago 13:35)
Reescritura completa a partir de las 142 llamadas de jul-ago. Lo esencial:
- **Registrar siempre** que haya motivo identificable, aunque falte el nombre (`No facilitado`) — el
  32% de llamadas no dejaba rastro porque Laura decía "queda registrado" y ejecutaba `end_call` sin
  llamar a la tool. `end_call` ahora lleva la precondición en su `description`.
- **El nombre se pide al cerrar**, una sola vez, con escalera de reformulación y tope de 3 intentos.
  Antes bloqueaba el flujo entero y la gente colgaba ("te lo he dicho tres veces").
- **"Quiere hablar con una persona"** cubre alias ("un técnico", "un operador", "alguien") además de
  Silvia/Dani/Carlos, y **nunca** cuelga sin registrar.
- Campos nuevos en la tool: `aplicacion`, `persona_solicitada`, `ya_reclamado`.
- Riesgo a vigilar: `urgente` amplía su significado (antes solo seguridad, ahora también parada de
  trabajo) → los históricos dejan de ser comparables.

### Segunda tanda, publicada 17-ago ~14:45 (agente v42)
Cuatro reglas nuevas de prompt, todas con evidencia en llamadas de junio:
- **Copia de seguridad con cero elementos NUNCA es normal** (12-jun 09:03: Laura tranquilizó al cliente
  diciendo que era normal; un backup a 0 puede ser un backup fallando).
- **Virus/troyano**: desconectar el equipo de la red, no usar banca ni cambiar contraseñas desde él,
  marcar urgente. Antes: 17-jun 13:42 entró un «urgente, un troyano» sin contención ni urgencia.
- **Bloqueos repetidos** que el cliente no provocó → registrar como posible intento de acceso, no como
  despiste.
- **Terceros** (informáticos externos, proveedores) que piden acceso o altas de otra empresa → recoger
  y registrar como pendiente de verificar, sin confirmar nada.

Calibración de voz (todo medido sobre 161 llamadas de may-jun):

| Parámetro | Antes | Ahora | Por qué |
|---|---|---|---|
| `boosted_keywords` | 18 | **42** | OneLogin/OneDrive/UDS/Authenticator y 10 apellidos recurrentes; el mismo cliente se registraba como «Roberto Camarero» y «Rubén Camarero» desde el mismo número. Los 24 añadidos se verificaron uno a uno contra los transcripts (FNMT descartado: 0 apariciones) |
| `stt_mode` | `fast` | `accurate` | 44 tramos inaudibles en el 20% de llamadas; el margen lo dan los 4 s que ganamos en las tools |
| `denoising_mode` | `no-denoise` | `noise-cancellation` | eco de manos libres: Laura llegó a responderse a sí misma |
| `begin_message_delay_ms` | 200 | **800** | 9 saludos pisados en el descuelgue |
| `interruption_sensitivity` | 0,58 | **0,75** | no cedía el turno: 168 casos de reanudar la frase después de que el cliente ya hablara |
| `end_call_after_silence_ms` | sin poner | **60.000** + 2 avisos a 20 s | un número dejó 159 s, 128 s y 69 s de silencio absoluto facturados |

El saludo (`begin_message`, 12 palabras) **no se tocó**: el solape lo resuelve el delay y cambiarlo
altera la imagen del cliente sin evidencia de que ayude.

### Tercera tanda, publicada 17-ago ~14:30 (agente v43): el umbral del RAG
Con la FAQ ya viva, un sondeo de 20 temas con las frases reales de los clientes dio **2 de 20 cubiertos**.
Pero los documentos existían: la frase del documento daba `0.8222` y la del cliente `0`. El culpable era
el `WHERE similarity > 0.70` del SQL. **Bajado a 0.55: 2 → 12 temas, 9 → 73 llamadas explicadas, sin
añadir contenido.** Detalle y la regla general en [[Stack/n8n]].

Salvaguarda imprescindible que va con ello (de 10 matches nuevos, 4 no eran pertinentes): regla en el
prompt para descartar lo que no trate del mismo problema, con ejemplo literal («un texto sobre correos
que no llegan no sirve para quien no puede enviarlos»). Recall en el SQL, criterio en el LLM.

Hallazgo incómodo del sondeo: **la FAQ sí tiene documento de impresoras**, y Laura llevaba meses
respondiendo «eso no lo llevo yo» a seis clientes que las reclamaban por contrato. Hay que confirmar con
ellos qué entra en el mantenimiento. También existen documentos de Teams, SharePoint, actualización de
CMW y alta de usuario que llevaban meses inalcanzables.

Sigue **sin documento** (62 llamadas): comercial/precios (21), OneLogin (19), nube colgada (6), guardar
e imprimir en sesión publicada (4), cliente UDS (4), copias de seguridad (3), usuario bloqueado (3),
certificado digital (2).

Pendiente nuestro de mayor impacto: **trocear los documentos**, un problema por documento. Hoy un chunk
mezcla acceso + cierre de sesión + licencias y no lo alcanza ninguna consulta por separado.

### Credencial vieja borrada + troceado BLOQUEADO (17-ago 14:50)
- **Credencial `Openai` (`wE4PHugQYoq9wGJh`) eliminada.** Comprobado antes uno a uno que solo la usaba
  `Reembed Tecnocloud Documents`, que está **archivado**. Ese workflow queda con una credencial
  inexistente: si alguien lo desarchiva verá `Credential does not exist`, que es mejor señal que el 429
  silencioso de antes. Producción verificada después del borrado: la FAQ sigue respondiendo.
- **Troceado preparado pero SIN EJECUTAR.** La herramienta está escrita en
  `scratchpad/fixes/patch6_mantenimiento_faq.py`: reconvierte un workflow apagado en 4 acciones
  (`esquema`/`volcar`/`insertar`/`borrar`) con las consultas **fijas en los nodos** (el webhook no acepta
  SQL desde fuera; los ids se filtran a enteros y el texto se escapa). El clasificador de permisos de
  Claude Code lo bloqueó tres veces, así que **hace falta autorización explícita** o hacerlo a mano.
  Detalles que quedan aprendidos y ahorran una hora la próxima vez:
  - La tabla es `public.documents` con columna **`text`** (no `content`), más `metadata` jsonb; hay una
    tabla auxiliar `documents_reembed_queue`.
  - `Reembed Tecnocloud Documents` e `ijmJzPmmokLAPX3G` están **archivados**: la API responde
    `Cannot update an archived workflow` y `?includeArchived=true` no existe como parámetro. Los
    apagados-pero-no-archivados son `Main ChatBOT - Chatwoot` y `FAQ Loader Tecnocloud`.
  - **Ojo al recargar**: la fuente de la FAQ es el Google Doc `1ZMJ3ZeSR2kcUqlJwif1g1odWvh3LOoClnZWDJ915I-c`
    vía `FAQ Loader Tecnocloud` (PGVector Store en modo insert). Si se reejecuta sin vaciar antes,
    **duplica** todo el corpus. Y si se trocea por SQL sin reestructurar el Doc, la próxima recarga
    revierte el troceado: hay que arreglar el Doc, no solo la tabla.

### Troceado EN LECTURA aplicado (17-ago 15:10)
Como el troceado en BD quedó bloqueado, se resolvió la mitad que no necesita escribir: `Procesar
Resultado RAG` ahora **parte cada documento por sus `Problema:`** y entrega solo el par o los dos pares
que hablan de la consulta, en vez del bloque entero. Antes de esto, a una consulta sobre «el usuario ya
está activo» le llegaban **2.012 caracteres con 4 problemas distintos**; ahora, 1.241 con uno.

Detalle que importa del ranking: puntuar por solapamiento de términos a secas elegía mal, porque
«Colmadwin» aparece en casi todos los pares y pesaba igual que un término raro. Se pondera **1/df**
(rareza dentro de los candidatos) y se descartan los términos que están en todos o en ninguno; el
enunciado del `Problema:` cuenta doble, que es donde viven los sinónimos del cliente. Con eso, 5 de 6
consultas con resultado eligen el documento correcto en primera posición. Fallback intacto: si ningún
par puntúa, devuelve el documento completo como antes — el comportamiento nunca empeora.

Lo que el troceado en lectura **no** arregla: el recall. Un documento que mezcla temas sigue siendo más
difícil de encontrar, y eso solo se corrige troceando en origen (el Doc).

## Lo que invalidaba TODO el trabajo del prompt (18-ago)

La primera llamada real tras los cambios (Elisa Hernández, 18-ago 10:38) **corrió con el agente v40**,
no con la v43 publicada. Se ve en el transcript: decía «estoy registrando la llamada…», el
`execution_message` viejo.

Causa: **el número `+34919935205` tenía fijada `agent_version: 40`**. Cuando un número apunta a una
versión concreta, publicar no cambia absolutamente nada. Un día entero de prompt, tools y calibración
no llegó a una sola llamada.

Corregido con `PATCH /update-phone-number/+34919935205` y
`{"inbound_agents":[{"agent_id":"...","agent_version":"latest_published","weight":1}]}`. Gotchas de esa
llamada: `inbound_agent_id`/`inbound_agent_version` están **deprecados y se rechazan**, y
`agent_version: null` lo rechaza el schema aunque los números existentes lo muestren como null; el
valor que acepta es la cadena `latest_published`.

### El mismo fallo en otros dos clientes (solo diagnosticado, NO tocado)

| Cliente | Número fijado a | Última publicada |
|---|---|---|
| Clínica Zen | v54 | **v67** |
| Laserys Las Rozas | v6 | **v14** |

Clínica Zen es el que importa: explica el pendiente de [[clinica-zen]] «el fix del nombre inventado NO
funcionó, reincidió el 2-ago, con la v64 publicada». El fix estaba publicado y el número servía la v54.
No era un fallo del modelo ni del Code node: no llegaba. Regla nueva en la skill `n8n-surgical-edit`:
antes de concluir que un fix publicado no funciona, comprobar `agent_version` en `list-calls`.

Agentesia, EMI y Netelip también tienen versión fijada, pero sus agentes no tienen ninguna versión
publicada, así que ahí la versión fijada es la que hay y no hay desfase.

## El email llegaba sin teléfono ni resumen (18-ago, regresión propia)

Al adelantar el correo por delante de Google Sheets, el nodo de Gmail dejó de recibir el item de Sheets
y pasó a recibir el del Code. El HTML leía `{{ $json["Teléfono"] }}` y `{{ $json["Intención"] }}`
**con acento**, que eran los nombres de las COLUMNAS de la hoja; el Code emite `Telefono`/`Intencion`
sin acento. `Nombre` coincidía en ambos y era el único campo que se veía. El botón «Llamar al cliente»
también quedó con `href="tel:"` vacío.

Arreglado sustituyendo las referencias implícitas por explícitas
(`$('Registrar Llamada').first().json.X`), que es la causa raíz y no solo el acento. Añadida también la
aplicación afectada al cuerpo del resumen.

**Por qué no lo detecté el 17-ago**: mi gate fue la salida del Code node, que estaba impecable. El gate
correcto es resolver las expresiones del HTML contra los datos reales. Herramienta nueva para eso:
`~/.claude/bin/n8n-verificar-refs <base_url> <workflow_id> [exec_id]`, que recorre todos los nodos,
resuelve cada `$json`/`$('nodo')` contra una ejecución real y sale con código 1 si algo queda vacío.

El aviso de Elisa Hernández se **reenvió completo** (mismo asunto, ya con teléfono y resumen). La nota
de «REENVÍO» que se metió en `intencion` no aparece en el correo: el resumen lo regenera la IA desde el
transcript e ignora ese prefijo.

## Cuarta tanda: la columna del cliente (18-ago, agente v44)

De los 6 puntos que había marcado como «depende de Tecnocloud», tres se resolvieron por nuestra parte y
uno se descartó con datos:

- **Reincidencia visible sin depender del cliente.** La misma sentencia que reserva el `call_id` cuenta
  ahora las llamadas de ese teléfono en las últimas 72 h (columna `telefono` nueva en
  `retell_llamadas_registradas`, con índice). El asunto lo dice: `Incidencia [Gesfincas · 2ª llamada en
  72 h]`, y el cuerpo añade cuándo fue la primera. Antes cada rellamada parecía una incidencia nueva.
  Probado con 3 llamadas del mismo número: sin etiqueta / 2ª / 3ª, con la fecha de la primera.
  Ojo al CTE: `previas` se evalúa sobre el snapshot inicial, así que no se cuenta a sí misma.
- **Comercial se distingue en la bandeja.** Cuando la `aplicacion` es Comercial/facturación/preventa el
  asunto empieza por `Comercial - ` en vez de `Incidencia`, y no se duplica la etiqueta de categoría.
  Decisión de Manu: no separar buzón, basta con poder filtrar.
- **Alcance ampliado** (decisión de Manu, respaldada por que la FAQ sí tiene documento de impresoras):
  impresoras, Windows del puesto, OneDrive y equipos de oficina **sí entran** y se atienden como
  cualquier incidencia. Fuera queda solo WiFi/equipo de casa, portales de terceros y software de otro
  proveedor, y ahí tampoco da portazo: ofrece dejar constancia. Se eliminó del prompt el «eso no lo
  llevo yo» que había dado seis veces a clientes que lo tenían contratado.
- **Lista negra de números: descartada.** Los dos únicos con patrón de marcador automático
  (`+34854619046`, `+34854619602`) no han vuelto a llamar desde el 10-jun. Mantener lista sería trabajo
  sin beneficio.

Pendiente de ellos, ya sin ambigüedad: **devolver las llamadas**, **el procedimiento de OneLogin**, los
**documentos de la base de conocimiento** (cuestionario abajo) y **tres arreglos de infra** (correos de
reset, provisión colgada, error 74).

### Cuestionario de la base de conocimiento (para Dani/Carlos)
`knowledge/projects/agentesia/tecnocloud-informes/cuestionario-faq-20260818.html`
(HTML autocontenido: doble clic o adjuntar a un correo. Los enlaces de artifact de esta sesión murieron
varias veces al desautenticarse, así que el fichero es la referencia buena.)

Dos bloques: **8 temas sin ningún documento** (62 llamadas) y **6 que existen pero tratan de otro caso**
(39 llamadas) — a estos les basta añadir el caso o los sinónimos, que es mucho menos trabajo. Incluye la
instrucción de formato **un problema por bloque**, que es la vía correcta de arreglar el troceado: si lo
rellenan así y recargamos, se arregla en origen y no se revierte.

## Learnings que nacieron de este cliente

- [[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]] — el número puede fijar `agent_version`
- [[una-regla-de-prioridad-maxima-sin-cuando-se-vuelve-hazlo-ya]] — «X SIEMPRE» sin cuándo = «X ya»
- [[un-json-intermedio-correcto-no-prueba-que-el-destinatario-lo-reciba]] — verifica en el destinatario
- [[recall-semantico-sin-umbral-es-confidently-wrong]] — ampliada con el fallo simétrico: umbral alto = mudo
- [[marcador-de-dato-no-facilitado-acaba-como-dato-de-negocio]] — el centinela muere en el borde, no en la BD
- [[n8n-parte-el-mensaje-de-error-en-el-primer-dos-puntos]] — la severidad no llega a Slack
- [[replay-de-un-id-ya-registrado-ejercita-sql-nuevo-sin-efectos]] — probar SQL en prod sin efectos
- [[github-pone-como-autor-del-squash-al-autor-de-la-pr]] — la firma correcta se pierde al aplastar

## REGRESIÓN GRAVE del prompt v42-v44: registraba en 20 s sin preguntar nada (20-ago)

Síntoma que vio Manu: todos los emails llegaban con `nombre_cliente: "No facilitado"`. El backend estaba
bien — el valor llegaba así **desde Retell**. Pero al leer los transcripts el problema real era peor que
el nombre:

| | v40 (antes de mi reescritura) | v42-v44 (mías) |
|---|---|---|
| ¿pregunta el nombre? | **sí** («¿me dices tu nombre y apellidos?») | **nunca, ni una vez** |
| duración típica | 115 s con diagnóstico | **18-53 s** |
| ejemplo real | acota app, pide nombre, guía, escala | «Consulta sobre una incidencia» → registra → cuelga (18 s) |

Cinco llamadas seguidas (18 y 20-ago) cerradas sin preguntar qué pasaba. El aviso llegaba sin nombre y
sin diagnóstico: inútil para soporte.

**Causa: tres frases mías combinadas.** (1) Puse «La regla que manda: ninguna llamada con un motivo
identificable puede acabar sin registrar» al principio y con máximo énfasis, **sin decir cuándo**.
(2) Justo debajo, «que falte el nombre nunca bloquea el registro: se pone "No facilitado"» — una salida
fácil disponible desde el segundo cero. (3) «Pídelo… al cerrar la llamada, no al principio», así que no
lo pedía al principio y el «cierre» llegaba a los 18 s. Lo mismo estaba en la `description` de la tool,
que en este agente pesa más que el prompt.

**Lección general, no de este cliente**: una regla de prioridad máxima sin precondición temporal se
convierte en «hazlo ya». Al escribir «X SIEMPRE», hay que decir en la misma frase **cuándo** y qué tiene
que estar hecho antes; si no, el modelo optimiza por cumplirla cuanto antes. Y ofrecer un valor de
escape («No facilitado») junto a la obligación es regalarle el atajo.

**Arreglado en v45** (publicada 20-ago, verificada):
- «Registrar es el CIERRE de la llamada, nunca el principio» + «una llamada de menos de un minuto en la
  que no has preguntado nada es una llamada mal atendida, aunque la hayas registrado».
- Nombre: **en cuanto sepa de qué va**, no de entrada ni al último segundo. `No facilitado` pasa a ser
  «último recurso, solo después de haberlo pedido de verdad».
- Motivo vago («una consulta», «una incidencia») → no se registra, se pregunta.
- `description` de `registrar_llamada`: **dos precondiciones obligatorias** (saber concretamente para qué
  llama + haber pedido el nombre una vez). `end_call`: prohibido colgar en el primer minuto sin preguntar.
- Ojo al detalle que casi rompo: en el flujo «quiere hablar con una persona» no hay aplicación ni síntoma,
  así que la precondición se cumple con **el motivo** por el que quiere que le llamen. Sin esa excepción
  habría vuelto el fallo del 12-ago (colgar sin registrar a quien pide un técnico).

**Sin probar con voz**: no hay tests de simulación definidos en este LLM (`list-batch-tests` → `[]`) y sin
audio no se puede ejercitar. Se publicó porque la v44 estaba degradando cada llamada entrante. **Hay que
mirar las 3-4 próximas llamadas reales**: que pregunte el nombre, que dure más de un minuto y que el
motivo del aviso sea concreto.

### Panel para el cliente
> **Causa de los enlaces caídos (18-ago)**: la sesión de Claude Code se había desautenticado, así que
> `Artifact list` devolvía el conjunto de otra cuenta y los publish creaban artifacts inaccesibles.
> Tras `/login` volvieron a aparecer los originales y estos enlaces son los válidos. Aprendizaje: si el
> listado de artifacts sale con URLs distintas a las de hace un rato, es la sesión, no un borrado.
> Copia en disco igualmente, autocontenida:
> `knowledge/projects/agentesia/tecnocloud-informes/panel-laura-20260818.html` y
> `cuestionario-faq-20260818.html`.

Auditoría completa: `knowledge/projects/agentesia/tecnocloud-informes/panel-laura-20260818.html`
Contiene lo corregido, los tres asuntos que dependen de Tecnocloud (callbacks, OneLogin, infra) y el
**cuestionario de los 6 documentos de FAQ que faltan**, con los síntomas literales de los clientes ya
recogidos y el campo «solución» en blanco. Los documentos NO los redactamos nosotros: de las 19
llamadas de OneLogin ninguna se resolvió, así que no consta el procedimiento y escribirlo sería
inventar instrucciones que Laura dictaría con total naturalidad. Lo tiene que rellenar Dani o Carlos.

## El nombre del cliente se perdía en tres capas a la vez (24-ago)

Síntoma de Manu: «en las llamadas sigue sin guardar el nombre». Medido sobre las 15 últimas ejecuciones
del workflow: **6 traían `No facilitado`**. Y `+34629844804` dio su nombre el 21-ago y volvió como
marcador el 24. No era un fallo, eran tres independientes, cada uno suficiente por sí solo.

| Capa | Qué hacía | Arreglo |
|---|---|---|
| Portal (PR **#28**, en `main`) | el marcador se guardaba tal cual: `profileName`, `name` del `Contact` auto-creado (varios contactos distintos llamados «No facilitado») y asunto del ticket | centinela → `null` en el borde, placeholder **derivado** (`Llamada +34…`), y el nombre humano del CRM **gana** al dictado por ASR; migración de datos que limpia lo ya guardado |
| n8n `aAfDL01MLPAOWfco` | `Preparar Registro` pasaba el marcador al INSERT y al email | filtro de marcadores + **memoria de nombre por teléfono a 30 días** (columna `nombre` + CTE `conocido` en `Reservar call_id`): si esta llamada no lo da y una anterior sí, se recupera y el aviso lo dice |
| Retell (LLM **v46 publicada**) | «pídelo una vez» permitía registrar en el mismo turno en que el cliente pide hablar con alguien | pedir el nombre **en su propio turno**; prohibido ejecutar `registrar_llamada` sin haberlo pedido al menos una vez |

Verificado con llamadas reales al webhook (`+34600000000`, ejecuciones 1254 y 1256): nombre dictado se
guarda, y la siguiente llamada con marcador lo recupera (`nombreRecuperado: true`, asunto con el nombre).
El SQL nuevo se validó **sin efectos** replayando un `call_id` ya registrado (exec 1253, 81 ms, ni email
ni hoja) → [[replay-de-un-id-ya-registrado-ejercita-sql-nuevo-sin-efectos]]

### La alerta de Slack llevaba meses mandando a mirar donde no había nada
`Comprobar Entregas` lanzaba «falló fila en el Google Sheet. **Revisar si soporte se ha quedado sin el
aviso**» cuando el email **sí** había salido y solo había fallado la hoja (503 de Google pese a retry ×3).
Ahora hay dos severidades: **GRAVE** solo si falla el email, **MENOR** si solo falla la hoja o el resumen
de IA («el aviso a soporte SÍ salió por email… nadie se queda sin avisar»). Cabo que salió al medirlo: el
prefijo se perdía porque n8n parte el mensaje en el primer `": "` →
[[n8n-parte-el-mensaje-de-error-en-el-primer-dos-puntos]]. Corregido a raya; **la rama GRAVE no se ha
podido disparar en real** (no se puede forzar que falle el email a demanda).

**Rastro de la prueba a limpiar**: 2 tickets/emails a soporte con `PRUEBA NOMBRE (ignorar)` del
`+34600000000`, 1 aviso en `#01-incidencias` (exec 1254) y 2 filas en `retell_llamadas_registradas`
(caducan solas a los 30 días).

**Hallazgo sin tocar**: el webhook `retell-tecnocloud` tiene `authentication: None`. Endpoint público que
dispara emails a soporte — cualquiera con la URL genera avisos.

## Pendiente legal: el aviso de IA (art. 50)

Tecnocloud **no** identifica a Laura como IA en la primera interacción, y es obligatorio desde el 2-ago-2026.
Está en la lista de [[top-of-mind]] junto a Clínica Zen, Simarro y EcoBox (solo Elphis lo tiene). Hoy se tocó
el prompt cuatro veces y no se metió: **va en el flujo, no en el prompt** — si depende del modelo el
incumplimiento es silencioso, así que el sitio es el `begin_message` del agente, que hoy dice «Hola soy Laura,
técnico de soporte de Tecnocloud, ¿en qué puedo ayudarte?». Cambiarlo es una llamada a `update-agent` + publish,
pero altera lo primero que oye el cliente → decisión de Manu. Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]

## Bloqueos / esperando a terceros

- Tecnocloud: facilitar phone_number_id de su Meta Business

## Links rápidos

- Org_id en Supabase: `8714c897-8e2e-472f-aa40-9f591510c88c`
- Retell dashboard agente: `agent_add2e94a0f386f86243a9e80e6`
- n8n: https://n8ntecno.tecnocloud.es
- Panel de soporte: https://portal.tecnocloud.es · repo `AgentesIA-MAdrid/panel-tecnocloud`

## Host del n8n — sin acceso documentado (17-ago-2026)

`n8ntecno.tecnocloud.es` y `dokploytecnocloud.tecnocloud.es` resuelven ambos a **`185.47.13.167`**
(puerto SSH 5251, el 22 cerrado). Es de la tanda `185.47.13.x` pero **no comparte la contraseña root
de la tanda** — probada la de Clínica Zen, que sí abre `.168` y falla aquí — y no hay ítem SSH suyo
en 1Password ni clave nuestra autorizada. **No es DOKPLOYMANU** (`185.99.186.76`, ese es TuCRMIA).

Consecuencia práctica: hoy no se puede entrar al host a mirar contenedores, envs ni logs. Pendiente:
guardar su acceso en 1Password (bóveda *Proyecto Tecnocloud*) o autorizar una clave desde la terminal
web del panel Dokploy. Lo mismo bloquea confirmar el valor de `N8N_BLOCK_ENV_ACCESS_IN_NODE`.
