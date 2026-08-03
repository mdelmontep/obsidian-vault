---
title: Agentes de cliente — ficha de 3 capas (harness / loop / grafo)
date: 2026-08-03
source: artículo "Agent Harness Engineering vs Loop Engineering vs Graph Engineering" (@LunarResearcher, 28-jul-2026) contrastado contra los hubs de cliente del vault
tags: [agentes, harness, loops, n8n, retell, observabilidad, clientes]
---

# Agentes de cliente — ficha de 3 capas

Mapa de los agentes en producción por capa, para **diagnosticar en qué capa cae un fallo antes de
elegir el fix**. Complemento de [[claude-code-harness]], que cubre el harness de Claude Code (mi
herramienta); esto cubre los agentes que le vendemos al cliente.

Las tres capas:

| Capa | Responde a | En nuestro stack es |
|---|---|---|
| **Harness** | qué puede ver y hacer el agente | prompt + KB de Retell, tools, credenciales, Chatwoot/Kommo/Clientify, Calendar, retención de ejecuciones, error handler |
| **Loop** | cómo se reintenta y **cómo se prueba que funcionó** | reintentos, dedup, marcado de enviado, ventanas horarias, recheck de disponibilidad |
| **Grafo** | qué paso puede ocurrir después | el workflow de n8n, el Conversation Flow de Retell, el Digital Pipeline de Kommo |

**Regla de diagnóstico**: no puede operar → harness · casi funciona pero es inconsistente → loop ·
el proceso es complejo (ramas, aprobaciones, especialistas) → grafo.

## El veredicto, antes de las fichas

Revisados los fallos reales registrados en los hubs entre mayo y agosto de 2026:

1. **Ninguno fue del modelo.** `entity_type` como string en vez de entero, Switch sin `options`,
   `.args` sin optional chaining, lock retenido 15 s, `EXECUTIONS_DATA_MAX_AGE` en horas creyendo
   que eran días, idempotencia que gateaba la notificación. Todo harness y loop.
2. **El grafo está sobrado en todas partes.** Nadie necesita más nodos. Clínica Zen tiene 14
   workflows, Simarro 34. Añadir topología no arregla nada de lo que falla.
3. **La capa que falta en TODOS es la evidencia de éxito.** Verificamos que la ejecución acaba en
   `success`, no que el efecto ocurrió. De ahí salen los tres casos peores del año:
   - Clínica Zen: los recordatorios de WhatsApp **no funcionaron nunca** — los dos bots de Kommo
     con **0 lanzamientos** históricos — y el marcado previo al envío lo tapó desde el primer día.
   - Agentesia (chatbot propio): `Registro Sheets` fallaba **en cada lead** con la ejecución en
     `success`. Ver [[error-de-tool-de-ai-agent-no-marca-la-ejecucion-como-fallida]].
   - Agentesia: el chat web **sin una sola ejecución desde el 19-jul** y nadie se enteró.
4. **Instrumentación ≠ vigilancia.** Clínica Zen tiene error handler que sí notifica: el fallo del
   28-jul llegó al colector y estuvo **7 horas** ahí hasta que lo encontré a mano. EcoBox lo hace
   mejor (Slack `#01-incidencias` + email). NotCaído detecta y sus avisos no llegan a nadie.

Corolario: el siguiente euro de ingeniería en clientes no va a más nodos ni a mejores prompts. Va a
**una consulta semanal por cliente que mida EFECTO** (citas creadas, recordatorios entregados, leads
registrados) y avise cuando el contador se queda a cero.

## Fichas por cliente

### Clínica Zen — voz + chat LIVE

| | |
|---|---|
| **Harness** | Retell `agent_350620f6…` v64, 4 tools · Kommo 36308863 (7 CF, 8 bots, 6 plantillas WABA aprobadas) · Google Calendar con credencial **de una cuenta personal del contacto legacy** · RAG Supabase self-hosted sin dominio público · retención de ejecuciones 14 d (arreglada 29-jul, estaba en 7 h) |
| **Grafo** | 10 workflows activos + `FMotimghgUBzEgdm` como `errorWorkflow` de los 9 restantes |
| **Loop** | reintento de recordatorios arreglado 28-jul (marcado sale del filtro, margen 30 min → cada evento cae en dos pasadas) + ventana horaria 08:00–21:30 |
| **Falla hoy en** | **Harness (vigilancia)**: el colector de incidencias apunta a `n8n-borja.tecnocloud.es` y no está decidido quién lo mira. **Loop (evidencia)**: falta el smoke E2E de la reserva por voz, y la prueba de que los recordatorios ya salen es «cuando los contadores de `63810`/`63808` dejen de estar a 0». |
| **Medido el 3-ago** | 268 ejecuciones retenidas de `PJBMjLLE0vNJjZH8`, **todas en `success`, cero envíos**: ninguna pasó del nodo de filtrado. No es bug (no hay citas en ventana), pero deja el fix del `entity_type` **sin verificar** desde el 28-jul. Y el fix del nombre inventado **reincidió** el 2-ago con la v64 publicada: `Reservar` se llamó con `"name":"Paciente nuevo"`. Detalle en [[clinica-zen]]. |
| **Riesgo de harness sin cerrar** | credencial de Calendar de una cuenta personal ajena; `emiafd@agentesia.madrid` hardcodeado recibiendo datos de pacientes |

→ [[clinica-zen]]

### EcoBox 360 — voz + chat LIVE

| | |
|---|---|
| **Harness** | Retell Flow v10 · Chatwoot · Google Calendar · WhatsApp Cloud API (plantilla `confirmacion_cita_ecobox_2`) · transcripción de audios por Whisper |
| **Grafo** | 7 workflows críticos + `Error Handler — EcoBox` (`z2EWXyATOsj6qtAW`) enlazado en los 7 |
| **Loop** | guard de solapamiento server-side en `Reservar_cita` (GCal getAll en la ventana antes de crear) — **el mejor loop con evidencia real que tenemos en un cliente**: comprueba el efecto en el sistema de destino, no la intención del modelo |
| **Falla hoy en** | **Loop (evidencia)**: 3 smokes pendientes — grúa/Mutua → handoff + email · reserva E2E que dispare `Build Emails` · hueco nuevo sin doble-booking |
| **Nota** | es el único cliente donde la observabilidad llega a un canal que alguien mira (Slack `#01-incidencias`). Patrón a copiar en el resto. |

→ [[clientes/ecobox/index|ecobox]]

### Centro Elphis — voz + chat WhatsApp LIVE

| | |
|---|---|
| **Harness** | WhatsApp Cloud API en el 659 (HMAC verificado activo contra el env real, no solo en el código) · Clientify · Chatwoot · 3 plantillas HSM aprobadas · Dokploy propio en el monitor del portal |
| **Grafo** | `chatwoot-event` → `router-ia` → `registrar-lead` / `book-and-notify`, más `retell-tool-crear-lead` y `doctoralia-email-sync` |
| **Loop** | dedup de notificación de 60 min separado del guard de deal de 30 días (arreglado 22-jul: la idempotencia de entidad estaba matando el side-effect) |
| **Falla hoy en** | **Harness (identidad y secretos)**: `clientify-upsert-contact` matchea **solo por teléfono** y pisa el nombre — con ~50 % de contactos que son familiares reservando por el paciente, ya ha mezclado dos personas reales. Decisión explícita de dejarlo, pero es deuda de harness, no del modelo. Y siguen sin rotar `META_APP_SECRET`, la clave RSA de Dokploy y la API key. |
| **Loop pendiente** | probar `pause_bot` con un WhatsApp real (solo verificado el wiring) |

→ [[clientes/centro-elphis/index|centro-elphis]] · [[telefono-como-identity-key-en-upsert-crm-colisiona-si-se-comparte]]

### Simarro Properties — voz + chat + outbound

| | |
|---|---|
| **Harness** | Retell Conversation Flow `conversation_flow_19ca70e19b3f` (el `agent_7b02aa…` retell-llm está en desuso) · Kommo (4 pipelines) · catálogo Idealista en Supabase vía Apify · Docuseal para contratos |
| **Grafo** | 34 workflows; `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`) como SSOT de disponibilidad compartida voz+WhatsApp |
| **Loop** | recheck de disponibilidad antes de confirmar — **arreglado en WhatsApp (01-jun), NO en voz** |
| **Falla hoy en** | **Loop, y es el peor caso abierto de la cartera**: por voz, `Respond FAST` (atado al timeout de 6 s de Retell) confirma la cita **antes** de rechequear, y `Create new leads3/2` crea el lead en Lead Caliente, lo que dispara el salesbot. Resultado: confirma slots ocupados y no crea el evento. Abierto desde el 01-jun. |
| **Además** | verificación E2E de reserva tras el recableo pendiente desde el 25-jun; 7 cambios aplicados sin probar en vivo |
| **Nota de grafo** | el bug de voz es exactamente lo que el grafo debería haber hecho explícito: la confirmación es un nodo que ocurre antes del gate. En WhatsApp se reordenó; en voz el timeout de Retell fuerza el orden malo. Aquí sí hay trabajo de topología, no solo de loop. |

→ [[simarro]]

### AGH Ibérica — agente "Carlos", PROD

| | |
|---|---|
| **Harness** | multi-tenant desde el día 1, HITL en todo write, tools fakeables detrás de interfaces, Postgres pgvector |
| **Grafo** | brain seam (`test/brain-seam.test.ts`), canales como adaptadores finos |
| **Loop** | `npm run gate` local (lint 0 `any` + typecheck + tests + gate del dashboard) — decisión de ADR: sin CI, el gate local es el contrato |
| **Evaluación** | **el único cliente que mide**: eje `query` al 72,7 % |
| **Falla hoy en** | **Evaluación**: la medición no es estacionaria — el endpoint deriva entre horas, así que comparar dos versiones no atribuye la mejora a un cambio real. Es literalmente la pregunta del checklist («¿puedes atribuir una mejora a un cambio concreto?») y es el problema difícil, no el fácil. |

→ [[agh-iberica]] · [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]]

### Agentesia (chatbot propio) — el peor instrumentado

| | |
|---|---|
| **Falla en** | **Harness (observabilidad)** y nada más: `Registro Sheets` perdía cada lead con la ejecución en `success`, arreglado el 31-jul y **sin tráfico desde el fix, sin verificar**; el chat web lleva sin ejecuciones desde el 19-jul; hay un secret en el `jsCode` |

→ [[agentesia]]

## El check que falta (aplicable a los 5)

Un cron semanal por cliente que consulte **efecto, no ejecución**, y avise cuando un contador se
queda a cero. Con lo que ya sabemos de cada uno, la consulta concreta es:

- **Clínica Zen** — lanzamientos de los bots `63810` (24 h) y `63808` (4 h) > 0 esta semana. Solo se
  ve en la GUI de Kommo, no por API: eso mismo es una deuda de harness que hay que cerrar.
- **EcoBox** — eventos creados en Calendar esta semana > 0 y sin solapes.
- **Elphis** — leads en Clientify creados esta semana vs conversaciones de Chatwoot: si divergen,
  la notificación se está comiendo leads otra vez.
- **Simarro** — tareas Meeting (type 2) creadas vs eventos en el calendario del agente.
- **Agentesia** — filas nuevas en el Sheets de leads > 0.

Lo mismo que dice [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]] pero un nivel más
arriba: no basta con que el error se escriba, tiene que llegar a alguien y tiene que medir el
resultado de negocio, no el estado HTTP.

## Qué NO hacer con esto

- **No montar grafos nuevos.** Todos los clientes tienen topología de sobra; ninguna incidencia de
  los últimos tres meses se habría evitado con más nodos.
- **No añadir tools "por si acaso"** a los agentes de Retell. Más superficie de acción = más errores
  de selección; y en Flex, más tokens compilados ([[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]).
- **No usar un LLM como checker** de estos flujos. El veto lo tiene el sistema de destino: Calendar,
  Kommo, Clientify. Es la misma regla que en [[claude-code-harness]].

## Primer run del check (3-ago-2026) — dos hallazgos que nadie tenía fichados

`~/.claude/scripts/agentes-check.py` sobre los 4 clientes con n8n accesible:

- 🔴 **Centro Elphis — `chatwoot-event` lleva 65 ejecuciones con ERROR en 7 días** (de ~300, o sea
  ~1 de cada 5), la última el 3-ago a las 18:29. Nodo `Persist ids conv_state`, error
  `invalid input syntax for type bigint: "null"`. Es el bot de WhatsApp VIVO en el 659, con
  pacientes reales: los nodos ejecutados llegan hasta `Lock eval`, así que revienta **después** de
  coger el lock de conversación. Hermano del incidente del 21-jul ([[lock-conversacion-liberar-tras-responder-no-tras-trabajo-post]]).
  Sin diagnosticar aún — mirar qué id llega como `"null"` (string, no NULL) y de dónde sale.
- 🔴 **Simarro — 4 workflows de CRON sin ejecutarse en lo retenido**: `Matching semanal (Flujo A)`,
  `Reconcile lead_preferences`, `Llamadas_outbound (reactivacion)` y `Leads cambio de fecha o
  anulacion`. El outbound se sabía (espera los consentimientos que marca Ramón), pero el **matching
  semanal es producto vendido** y no consta que estuviera parado. Ojo al matiz: "en lo retenido"
  depende de `EXECUTIONS_DATA_MAX_AGE` de esa instancia, que no está verificado — puede ser una
  ventana corta. Confirmar antes de dar por muerto nada.
- 🟠 **Simarro repite el patrón de Clínica Zen**: `Recordatorios` con 15 ejecuciones y el nodo de
  envío sin correr ni una vez. Puede ser falta de visitas en ventana, como en CZ, o el mismo tipo
  de fallo silencioso. Es justo lo que el check está para destapar.

Lección: el primer día de una medición de efecto encuentra cosas que meses de «está todo en verde»
no encontraron. No porque nadie mirara, sino porque se miraba el indicador equivocado.
