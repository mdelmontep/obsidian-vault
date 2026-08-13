---
title: Simarro — fix captura de preferencias WhatsApp + 3 bugs de dedup en el chatbot (13-ago)
date: 2026-08-13
source: claude-code-session
tags: [simarro, n8n, kommo, whatsapp]
---

# Contexto

Antes de responder a los 8 puntos de queja de Dani (11-ago), se verificaron 2 cosas concretas:
recordatorios 24h y la llamada outbound con vivienda actualizada/alternativa. Del análisis salió
un gap real: WhatsApp nunca escribía en Kommo las preferencias de búsqueda del cliente (zona,
presupuesto, habitaciones) — solo la vivienda concreta elegida. Voz sí las capturaba (vía análisis
post-llamada de Retell), pero solo 3 de 9 campos, y con un gate de status que las dejaba fuera de
`lead_preferences` si el lead era nuevo.

# Decisión

1. `Reconcile lead_preferences` (`UQHBaQxeVsutlLWX`): `POOL_STATUSES` ampliado de 3 a 4 fases,
   añadido `105137095` ("Lead Caliente", Embudo de ventas) — sin cambiar en qué fase se crea el
   lead nuevo (eso es triaje humano intencionado, no se toca).
2. `Buscar_viviendas_catalogo` (`5NRXALN9lBVE9fTs`): nuevo tramo que persiste zona/precio
   máx/mín/habitaciones en Kommo cuando la llamada trae `Lead_id` (solo WhatsApp lo manda; voz
   no, así que no le afecta — sus preferencias las captura por otro lado `Captura_interes_llamadas_voz`).

# Regresiones propias en el camino (2, ninguna llegó a afectar tráfico real)

- **v1**: rama nueva colgando en paralelo desde `Start`. El sub-workflow quedó con 2 nodos
  terminales que se ejecutaban a la vez en la misma corrida → el `Execute Workflow` que lo llama
  devolvió el output del nodo nuevo (vacío) en vez del de la búsqueda real. Revertido al detectarlo
  con una llamada de prueba al webhook de voz (encontró 10 viviendas por dentro, el cliente habría
  recibido "no tengo viviendas").
- **v2**: nodos en serie pero el Code node hacía `return []` cuando no había `Lead_id` (caso
  voz, que es siempre) → 0 items cortaba el flujo ahí mismo, `Return búsqueda` nunca se ejecutaba
  para voz. Revertido igual.
- **v3 (correcta)**: el Code node SIEMPRE devuelve 1 item con flag `shouldPatch`; un IF nuevo
  decide si se llama a Kommo o se va directo al terminal único. Simulados los 6 caminos posibles
  en papel antes de desplegar. Probado en vivo contra el webhook de voz (3 escenarios: found>1,
  found=0, found=1) — comportamiento idéntico al de antes de tocar nada.
- Impacto real de ambas roturas: **cero**. Revisadas las ejecuciones de la ventana rota
  (2-7 minutos cada vez) en `Buscar_viviendas_catalogo`, `Voz_buscar_viviendas` y `Chatbot Simarro`
  — solo aparecen mis propias pruebas, ningún cliente llamó ni escribió en esas ventanas.

Ver [[n8n-execute-workflow-nodo-terminal-ambiguo-con-multiples-ramas]].

# Bug real pre-existente encontrado de rebote: WhatsApp lleva desde el 12-ago sin poder responder

Al probar el fix con un mensaje real de WhatsApp, el bot no contestó. Causa: el fix de
deduplicado de mensajes desplegado el 12-ago (`Redis - Check duplicado`, un GET con
`propertyName: "duplicado"`) sustituye `$json` entero por `{duplicado: ...}` — y **3 nodos
distintos** aguas abajo en `Chatbot Simarro` seguían leyendo `$json.body[...]` esperando el body
del webhook original, que ya no está ahí:

1. `Redis - Marcar mensaje` — key `undefined` → Redis SET lanza excepción real (`Invalid argument
   type`). **Esta sí avisó a Slack** (`#01-incidencias`, confirmado con la respuesta `"ok"` del
   webhook) — el Error Workflow de n8n SÍ se disparó.
2. `Edit Fields` — Type/contact_id/mensaje/Lead_id todos `null`, sin excepción. El resto del flujo
   procesaba con datos vacíos.
3. `If2` — el IF que decide foto-vs-texto (`combinator: and`, ambas condiciones leían
   `$json.body[...]`) siempre evaluaba `false` → todo mensaje con adjunto se enrutaba como si
   fuera texto plano, sin excepción, desde el 12-ago.

Verificado con las 14 ejecuciones reales del propio 12-ago: **ninguna pasó por esta rama** —
todas corrieron antes de que el fix se desplegara esa tarde. El mensaje de prueba de hoy fue el
primer mensaje real en tocar este código desde que se escribió.

Fix: los 3 nodos ahora referencian `$('Recibir mensaje').item.json.body[...]` explícitamente en
vez de `$json.body[...]`. Verificado con un barrido completo del grafo de conexiones (BFS desde
`Redis - Check duplicado`) buscando cualquier otro nodo alcanzable con el mismo patrón — ninguno
más. Confirmado end-to-end con un mensaje real: el bot respondió correctamente, con búsqueda en
catálogo incluida.

Ver [[n8n-json-narrowed-rompe-nodos-lejanos-sin-error]].

**Nota sobre el aviso de Slack**: no avisó del fallo silencioso (#2 y #3) porque no es una
excepción — es el límite real de lo que un Error Workflow puede detectar, no un bug del propio
sistema de avisos.

# Bug adicional en el propio fix de preferencias: Kommo rechaza el PATCH entero

Al probar en real, `Actualizar preferencias lead` devolvió `Bad request`. Causa: el campo
"Habitaciones" (`1373289`) en Kommo es tipo `select` con opciones fijas (`1`,`2`,`3`,`4`,`5+`), no
numérico libre — mandar `{value: 2}` (número) en vez de `{value: "2"}` (string exacto de una
opción) hace que Kommo rechace el `custom_fields_values` **entero** del payload, no solo ese
campo: zona y precio (que sí eran válidos) tampoco se guardaron. Confirmado leyendo el lead
después del intento fallido (sin ningún CF de los 3 escrito). Fix: mapear `minRooms` a la opción
más cercana (`5+` para 5 o más). Ver [[kommo]] (Stack).

# Pendiente

- Confirmar con un mensaje real más que el PATCH de preferencias ya no falla tras el fix del
  campo Habitaciones (no hubo tiempo de repetir la prueba en la misma sesión).

# Barrido cross-cliente — mismo patrón en otros clientes activos

Revisado tras encontrar el bug en Simarro, por si el mismo patrón (nodo que reduce `$json` vía
`propertyName`, seguido de un nodo aguas abajo que sigue leyendo `$json.body[...]`) se repetía:

- **Laserys Las Rozas** (local + vivo, `n8n-lasrozas.agentesialabs.com`): tiene el mismo patrón
  de nodo reductor (`Redis1`, GET con `propertyName`) pero **limpio** — todos los nodos aguas
  abajo referencian `$('Recibir mensaje').item.json...` explícitamente, nunca `$json.body`.
- **Clínica Zen** (vivo, `n8nclinicazen.agentesia.madrid`): mismo patrón que Laserys (`Redis1` +
  `Redis Get Acumulado`), **limpio** por el mismo motivo — construido sobre la misma plantilla.
- **Centro Elphis** (vivo, `n8n-elphis.agentesia.madrid`): sus workflows de WhatsApp/Chatwoot
  (`wa-inbound-bridge`, `chatwoot-event`, `router-ia`) **no tienen ningún nodo reductor de este
  tipo** — arquitectura distinta (idempotencia por tabla Postgres, no Redis GET con
  `propertyName`), el patrón exacto no aplica.
- **EcoBox** (vivo, `n8necobox.agentesialabs.com`): igual que Elphis, `Chatwoot Bot Alex` no
  tiene nodos reductores de este tipo.
- **AGH Ibérica**: descartado sin revisar workflows — decisión de arquitectura documentada en su
  CLAUDE.md, el agente va en código (Mastra/TS), n8n no se usa para el runtime conversacional.

**Conclusión**: el bug era específico de Simarro (la única instancia donde el nodo de dedup se
escribió con `$json.body` a secas en vez de pinear el nodo webhook). No se repite en el resto de
clientes con chatbot WhatsApp activos.
