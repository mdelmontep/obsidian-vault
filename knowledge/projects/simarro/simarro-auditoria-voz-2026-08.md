---
title: Simarro — auditoría de voz+n8n de agosto 2026 (detalle técnico)
date: 2026-08-12
tags: [simarro, retell, n8n, auditoria]
---

Detalle técnico de la sesión que atacó los 8 puntos de queja original del cliente. Resumen en [[simarro]].

## Workflows n8n tocados (todos con backup pre-fix en `knowledge/projects/agentesia/n8n-backups/simarro/`)

- **`Leads entrantes`** (`iMoTKZWxYLymGuHF`) — el más tocado: tarea de visita Kommo (expresión JS sin `{{ }}`, corregida en WA y Retell), `service_type`+zona guardados en cualquier llamada, 4 nodos de la rama WA sin `onError` silencioso (igualado a Retell), WA ya no se queda mudo si el slot está ocupado, teléfono de voz normalizado a +34, guardado de `calendar_id`+`event_id` al reservar (custom fields Kommo `1379550`/`1379552`, nuevos). **12-ago, tras pruebas reales del cliente**: `Update contacts1` pisaba el teléfono real del contacto de WhatsApp con lo que el LLM creía extraer del texto — nuevo `Get Contacto Actual WA` + `Validar Telefono WA` leen el dato real primero, el del LLM solo rellena si no había ninguno. Ver [[no-dejar-que-el-llm-sobrescriba-un-dato-que-el-canal-de-origen-ya-conoce-con-certeza]].
- **`Leads cambio de fecha o anulacion`** (`om8iBm8ovENIgaxv`) — cancelación ya no confirma sin verificar el borrado real; vía rápida (lee `calendar_id`/`event_id` del lead, 1 delete directo) con fallback a los 8 calendarios de agente para reservas sin ese dato. Cierra la tarea de Kommo al cancelar con éxito.
- **`Recordatorios`** (`Oa1lSQuDgEZvZCNS`) — margen de ventana 15→20 min (reduce huecos entre escaneos de 30 min).
- **`Derivacion Humano`** (`DFtb3qVtxWwqHHkR`) — webhook de Retell tenía una conexión duplicada que rompía el mapeo de datos; ahora avisa a Slack `#01-incidencias` con el lead y link a Kommo (antes no avisaba a nadie).
- **`Sync_catalogo_idealista`** (`nzxtGnblEFwwkofO`) — 4 Code nodes con `helpers.httpRequestWithAuthentication` (roto por cambio de plataforma) migrados a HTTP Request nativo + `alwaysOutputData` + Code de envoltura; nuevo sweep que borra del Google Sheet las filas de propiedades retiradas (nunca lo hacía, solo upsert).
- **`Watchdog_catalogo_idealista`** (`9zsC2ZyFUGj8nxka`, creado hoy) — de 1 corrida/día (umbral 26h) a cada 6h (umbral 8h) + cooldown de 24h entre avisos repetidos del mismo corte.
- **`Buscar_viviendas_catalogo`** (`5NRXALN9lBVE9fTs`) — las 3 rutas de búsqueda no filtraban por `status=active`: el chatbot podía ofrecer y reservar visitas sobre pisos vendidos.
- **`Enriquecer_lead_vivienda`** (`bdwFEMMZ6pGoihVb`) — mismo bug de `status=active` en otro flujo.
- **`Voz_buscar_viviendas`** (`0eVxjZJXPU8hj6qq`) — `match_count` hardcodeado a `15` en `Map args`, ignoraba lo que mandara el LLM.
- **`Retell Inbound Dynamic Variables`** (`Ek8aM9sJviWA3675`) — ahora busca el teléfono en Kommo y pasa el nombre del cliente conocido a Ana (antes hablaba siempre en genérico).
- **`Matching semanal`** (`RGu1FLq9l3PKaX2B`) y **`Reconcile lead_preferences`** (`UQHBaQxeVsutlLWX`) — cron zombie reactivado; Matching además cortaba con error falso cuando no había coincidencias nuevas (el caso normal, `alwaysOutputData` en `Find new matches`).

## Retell (agente `agent_0df7f123e7e3c24d99c9152358`, flow `conversation_flow_19ca70e19b3f`)

Versiones publicadas v12→v22 (cada cambio verificado por integridad de nodos/edges antes de publicar):
- v12: esquema de `Mirar_disponibilidad` (`_after`/`_before` → `After`/`Before`, coincidiendo con `required` y con lo que n8n lee); `idealista_id` añadido al override de cambio de fecha.
- v14: `match_count` añadido al esquema real de `Buscar_viviendas`; confirmación breve de día+hora+nombre antes de pedir consentimiento (antes prohibido parafrasear, sin ningún control previo a ejecutar la reserva); 7 nodos de error (uno por tool) con pregunta al cliente "¿lo intento otra vez?"; `boosted_keywords` a nivel de agente con los topónimos reales de la cartera.
- v16: corregido el texto del prompt sobre `match_count` (no tiene efecto en búsquedas sin filtro, donde el código fuerza un mínimo de 25 resultados a propósito).
- v18: rediseño del reintento — ya no pregunta; avisa brevemente y reintenta sola una vez, si falla otra vez lo dice claro y escala. Patrón: [[retell-reintento-sin-variable-de-estado-usando-contexto-conversacional]].
- v20: `n_brief_comprador` reforzado (nunca decir "Claro."/"Dale." sin transitar en el mismo turno; edge relajado para aceptar zona aunque la frase sea confusa) — **insuficiente**, reprodujo en llamada real el mismo bug con una transcripción muy confusa.
- v22: tercera vía explícita para "no reconozco nada identificable" — preguntar en vez de decir la palabra suelta. Sin validar aún con llamada nueva. Patrón: [[retell-nodo-conversacional-debe-cubrir-explicito-el-caso-no-entendi]].

Patrón usado para editar flows publicados: `create-agent-version` (`base_version:N`) → edita la draft → `publish-agent`. Ver [[retell-published-flow-400-crear-nuevo-y-reasignar]].

**Corrección de dato**: el número real vinculado al agente es `+34 910 05 46 75` ("Simarro Netelip" en Retell), no `+34 919 93 28 52` que tenía el hub — verificado con `list-phone-numbers`.

## Validado con datos/llamadas reales (no solo lectura de código)

- Tarea de Kommo creada de verdad tras el fix (antes: 0 en la historia del sistema).
- Disponibilidad de voz: con el payload exacto que el LLM mandaría, antes → "no me ha llegado la fecha"; después → responde bien.
- Cancelación: 7,9-9s → 2s con la vía rápida; verificado que además cierra la tarea de Kommo.
- `match_count`: 1 en Madrid trae 1 resultado, 10 trae los 3 reales que hay — confirmado que antes siempre traía 15 fijo.
- Derivación a humano: mensaje real llegó a Slack con el lead y link a Kommo.
- Reconoce cliente conocido por teléfono en llamada de voz entrante (probado con contacto real de Kommo).

## Investigado y descartado

Error de WhatsApp "necesitas vincular un método de pago válido" (código 3107 de Meta) al enviar la
confirmación de cita — parecía facturación, no lo era: método de pago vinculado y vigente,
plantilla "Visita Confirmada" aprobada, número conectado con calidad alta. La causa real era el
teléfono roto del contacto (arriba). El error genérico de Meta puede saltar por varias causas
distintas del mensaje textual que muestra.

## Efectos secundarios de las pruebas (a resolver, ver [[simarro]] §Otros pendientes)

Leads de test en Kommo (`34790206` + contacto `38931342`) y 2-3 emails reales de "visita" a `rss@`/`pss@simarroproperties.com` por las reservas de prueba usadas para medir la latencia. Contacto `38942304` ("Manuel del Monte") con teléfono roto (`+34` sin dígitos) — a corregir a mano; el fix evita que vuelva a pasar pero no repara datos ya guardados mal.
