---
title: Simarro Properties — Snapshot estado 2026-06-08
date: 2026-06-08
source: sesion-claude-code
tags: [simarro, n8n, kommo, retell, estado, snapshot]
---

# Simarro Properties — Estado real al 2026-05-28

> Source of truth completo: `/Users/manueldelmonte/simarro/CLAUDE.md`. Este doc es snapshot resumen para retomar rápido.

## Hecho ✓

### Kommo Simarro (cuenta `simarro.kommo.com`)
- **Pipeline principal `13546071`** "Embudo de ventas" con 9 status (incluye Lead Caliente `105137095`, Agente Asignado `105137099`, Cancelado, Derivado Humano, etc.)
- **4 pipelines nuevos** para forms web (Borja approach):
  - `13652227` Valoraciones (4 status custom)
  - `13652231` Capacidad de compra
  - `13652235` Personal Shopper
  - `13652239` Inversión
- **13 custom fields del lead** (IDs `1373283`-`1373307`): Tipo vivienda, Zona, Superficie, Habitaciones, Estado vivienda, Plazo venta, Situación compra, Ingresos, Ahorro, Precio objetivo, Presupuesto inversión, Property reference, Notas form
- **Custom field `Agente asignado`** (`1373105`) creado, tipo texto
- Renombrado `Próxima cita` → `Día de visita` (mismo ID `1330871`)
- **6 plantillas WhatsApp HSM aprobadas por Meta** (template IDs `72341`-`72645`):
  - Formulario, Confirmación cita, Recordatorio 24h, Agente asignado, Plantilla 4 horas, Valoración, Solicitud_recibida
- **8 salesbots Kommo** (IDs `87861`-`88575`) mapeados 1:1 con plantillas

### n8n Simarro (`n8nsimarro.agentesia.madrid`)
- **Workflow `OFGGroWlifA88YFN` Formulario web reescrito** desde cero arquitectura production-pragmatic:
  - Webhook UUID `80f01ee4-5e87-4d2d-9eeb-3786cfb18fbd`
  - Bearer token check (`simarro_Z2O40v...`)
  - Respond 200 inmediato (web async)
  - Code Map+Build con MAPPING dinámico por formType (6 tipos)
  - Postgres dedupe 15min (tabla `form_submissions` creada con índices)
  - Kommo `/leads/complex` (lead+contact+CFs en 1 llamada)
  - Salesbot dinámico: `contacto_propiedad` → 87869 (Formulario), resto → 88575 (Solicitud_recibida)
  - IF Kommo OK → Postgres update `done` o `kommo_failed` (recovery hook)
  - **Fix doble disparo WhatsApp (2026-05-04)**: Borja añadió 88575 como automation del status "Nuevo lead" de los 4 pipelines de form. El nodo `Salesbot Run` lo invocaba de nuevo via `/salesbot/run` → 2 plantillas idénticas. Solución quirúrgica: nodo `IF contacto_propiedad` entre `Update kommo_ok` y `Salesbot Run`. Solo `contacto_propiedad` (bot 87869, sin automation) sigue invocando el bot por API; los 5 con bot 88575 saltan al email final
  - **Notas form simplificadas (2026-05-04)**: campo Notas en Kommo dejó de ser JSON crudo. Ahora solo `notasAdicionales` + extras útiles (`tipoIngresos`, `antiguedad`, `tipoCompra`, `propertySlug`) si tienen valor. Vacío si no hay nada. La traza técnica completa (UTM, IP, userAgent, timestamps) sigue en `form_submissions.envelope` jsonb
- **Workflow `QLfRT9AWmV1HLMZs` Chatbot reescrito**:
  - Variable `clinica` renombrada a `mensaje` (5 sitios + grep pre/post para 0 residuos)
  - Think description completo Simarro (eliminado "Clínica Zen", horario L-V partido 10-14/17-20, lógica fin-de-semana → Derivar_agente)
  - Vector Store description corregida ("informacion de la clinica" → "Simarro Properties")
- **Workflow `YGnefIXAKNJMZTw3` Agente Asignado**: Code JS búsqueda por `field_name == 'Día de visita'` (corrigió de "Dia preferencia cita"). Placeholders `TASK_TYPE_ID_TODO` → `2` (Meeting), `RESPONSIBLE_USER_ID_TODO` → `15113339` (user Simarro Properties / Ramón)
- **Workflow `0eVxjZJXPU8hj6qq` Voz_buscar_viviendas (creado 2026-05-04)**: wrapper webhook para que el agente Retell "Ana" use el catálogo de viviendas. Webhook `/webhook/voz_buscar_viviendas` (sin auth, mismo patrón que el resto de tools voz) → ExecuteWorkflow → `Buscar_viviendas_catalogo` (5NRXALN9lBVE9fTs, sub-workflow intacto, lo sigue usando el chatbot WhatsApp) → Format For Voice → Respond. Devuelve máximo 2 viviendas con mensaje breve hablable (solo zona + precio); detalles (habitaciones, m², descripción) van en `results` del context para que el LLM los lea bajo demanda. Mensaje fallback hablable cuando 0 resultados. `alwaysOutputData: true` en los nodos posteriores al ExecuteWorkflow (sin esto, RPC vacía → ningún output → body vacío al webhook)
- **Retell LLM `llm_ee8778e55dc4eaf29b38b5110ae2` (Ana, agent `agent_7b02aa7680b8798ea033fab2c2`)**: tool `Buscar_viviendas` añadida (apunta a `/webhook/voz_buscar_viviendas`, params: `query` requerido + `municipality, max_price, min_rooms, min_size` opcionales, `speak_during_execution: "Déjame mirar el catálogo un momento"`). System prompt editado en 3 puntos quirúrgicos: bloque de instrucciones de la tool (lee TAL CUAL `message`, detalles bajo demanda desde `results` sin re-llamar), bullet en "Inferencias automáticas" (cliente con criterios concretos → ejecutar Buscar_viviendas en vez de saltar a cierre), reescrita la FAQ "Propiedades disponibles". Sigue `is_published: false`
- **Workflow `Oa1lSQuDgEZvZCNS` Recordatorios**:
  - SALESBOT_ID_PLACEHOLDER reemplazados (87861 para 4h, 87871 para 24h)
  - **Fix TypeError cada 30min (2026-05-04)**: el nodo `Filtrar y evitar duplicados` estaba escrito para Google Calendar (`evento.start.dateTime`, regex sobre `summary`) pero recibía Kommo tasks (shape `_embedded.tasks[].complete_till`, `entity_id`, `task.id`). Code reescrito iterando `_embedded.tasks` con campos correctos. Bonus: limpieza automática `staticData.enviados` cada 48h (constante `LIMPIEZA_48H` declarada y nunca usada antes)
  - **Auth profesional (2026-05-04)**: HTTP nodes "WhatsApp Recordatorio 24h/4h" tenían `Authorization: Bearer TOKEN_CZ`/`TOKEN_CY` literales (placeholders nunca sustituidos en la replicación inicial). Migrados a `predefinedCredentialType: kommoLongLivedApi` igual que el workflow Formulario
- **Workflow `NsGM8vyXxV08cuoO` Buscar_base_de_datos**: field_id `355122` (CZ) reemplazado por `1330871` (Simarro)

### Web Simarro (`github.com/AgentesIA-MAdrid/simarro_web`)
- **PR #1 abierta** documentando que `N8N_WEBHOOK_TOKEN` es required en producción
- Endpoint `/api/form-submit` ya envía `Authorization: Bearer ${N8N_WEBHOOK_TOKEN}` automático

### Postgres Simarro (cred `NbSEPfQRe9htaaYm`)
- Tabla `form_submissions` creada con schema completo (audit + dedupe + recovery por status)
- Índices: phone+submitted_at, status pending

## Decisiones arquitectónicas tomadas

- **Approach Borja para forms web**: 4 forms cualificables → pipelines propios; `contacto_propiedad` → embudo principal en Lead Caliente porque dispara salesbot WhatsApp inmediato (más caliente)
- **Salesbot diferenciado por intención**: `contacto_propiedad` recibe template "Formulario" (invita a responder, tiene sentido porque cliente dio poca info); resto recibe template "Solicitud_recibida" (solo confirmación, no invita a responder porque cliente ya rellenó form detallado)
- **Opción 1 (atajo) para fin-de-semana**: chatbot ejecuta `Derivar_agente` (apaga IA) cuando cliente pide visita fuera horario oficina o fin de semana. Limitación: bot deja de responder otras consultas. Mejora futura `Solicitud_confirmacion_visita` documentada en canvas Slack F0B088P9P5K (POSIBLES AMPLIACIONES)
- **Mirar_disponibilidad sigue Google Calendar (decisión 5C híbrida aplazada)**: migración a Kommo tasks como source of truth + GCAL espejo aplazada al canvas. Es trabajo grande (~45 min en 2 workflows) y tiene sentido hacer cuando Ramón tenga GCAL re-autorizado

## Hecho desde 2026-05-04 ✓ (sesión 2026-05-28)

### Routing por agente + E2E voz
- **Google Calendar re-autorizado**: flujo de citas funcional (cred `d3uDK7X9ZflAoumq`).
- **Routing por agente implementado y testeado**: `resolve_property_calendar(idealista_id)` → calendario del agente. Migraciones SQL `003` y `004` aplicadas en Supabase.
- **WA confirmación de cita funciona para voz** ✓: mecanismo = Digital Pipeline Kommo bot 87865 al entrar en Lead Caliente. Fix: teléfono de contactos voz ahora se guarda en E.164 (`+34XXXXXXXXX`) en `Create new contacts1`.
- **Bugs Retell corregidos**:
  - Ana no pregunta "¿mañana o tarde?" si el cliente ya dio hora concreta
  - Ana no improvisa preguntas RGPD en el step de consentimiento
  - `Mirar_disponibilidad` ahora recibe `idealista_id` → consulta el calendario del agente correcto (fix en state machine BUSCANDO del prompt)

## Pendientes bloqueantes (orden)

1. **Ramón añade `agente:` a descripciones de Idealista** — actualmente `properties.agent = NULL` en TODAS las viviendas → el routing por agente siempre cae a fallback (calendario general). Sin esto, las citas van al calendario equivocado.
2. **Correr sync tras punto 1**: `Lanzar scrape Simarro (manual)` (workflow `3zBDpPwBYLZgMink`) → poblar `properties.agent`.
3. **Test E2E routing**: llamada voz → vivienda con agente real → verificar en n8n que `RPC Cal Disp source=agent` y evento en calendario del agente.
4. ✅ **Agente Retell PUBLICADO** (v29, 2026-05-31). Método correcto = `POST /publish-agent-version/{id}` `{version}` (el `PATCH update-agent is_published` anotado antes era OBSOLETO, no funciona en esta instancia con versioning).
5. **Crear cred SMTP Gmail** en n8n con App Password de `simarroproperties@gmail.com`. Cred actual `oKRmYFhljczyvzV8` es fantasma → cero emails enviados.
6. **Limpiar restos de test**: leads test Kommo de la sesión 2026-05-31 (`32260874` "Lead voz" + `32260174`/`32260184`/`32260262`/`32260290`/`32260318`/`32260370` "TEST…BORRAR" + el de "Ramon Demo" tel 600999888) desde UI; más legacy `28211029`/`28211091`/`28211167`.

## Sesión 2026-05-31 — disponibilidad con buffer real + go-live voz
- **Bug del buffer resuelto**: el LLM ofrecía horas que invadían el margen entre visitas. Causa: `Mirar_disponibilidad` devolvía prosa y delegaba el cálculo al LLM. Fix: el webhook devuelve `slots` (lista pre-computada), sub-workflow `Calc_Disponibilidad` (`kSgDVB8miWnvQFOJ`) single source of truth, ventana de lectura GCal al día completo, recheck fail-open en `Reservar_crm`. Ana exige nombre completo. Detalle en [[routing-citas-por-agente]].
- **Ana Retell publicada v29.** Chatbot WhatsApp actualizado al formato `slots`.
- **E2E verificado** (simulación sin mock → flujo real): lead Kommo + evento Google Calendar. Confirmado por Ramón viendo la reserva en `consultingsimarroproperties@gmail.com`.
- **Bloqueante real para routing por-agente sigue siendo**: Ramón añade `agente:` en Idealista (mientras tanto TODO cae en el calendario general).

## Sesión 2026-06-08 — Automatizaciones P4/P5 + email post-visita

### Kommo — nuevos stages en "Embudo de ventas" (`13546071`)
- **`Post-visita`** (`107269815`, verde) — el lead entra aquí automáticamente 48h después de la visita
- **`En seguimiento`** (`107269819`, amarillo) — para uso manual cuando se activa una alerta de inactividad

### P4 — Seguimiento post-visita 48h (HECHO)
- **`Oa1lSQuDgEZvZCNS` Recordatorios modificado**: añadido tercer caso al switch — detecta tareas Meeting cuyo `complete_till` fue hace ~48h (ventana ±15min). Dispara:
  1. Salesbot 87873 (plantilla `valoracion_servicio`, botones WA ¡Muy buena / No muy buena)
  2. Email HTML post-visita a `info@simarroproperties.com` si el lead tiene email en CF `1372575`
  3. Mueve lead a etapa **Post-visita** (`107269815`)
- Email post-visita diseñado: fondo `#0F1715`, bloques verdes, dos botones mitad/mitad — verde ♥ "Ha ido genial → Google Reviews" y oscuro ✉ "Podría mejorar → Cuéntanos". **PENDIENTE**: meter URL real de Google Reviews de Simarro (placeholder `GOOGLE_REVIEWS_URL_PLACEHOLDER` en el nodo `Build email post-visita` de Recordatorios).

### P5 — Alertas inactividad (HECHO)
- **Nuevo workflow `Alertas_inactividad`** (`Xh2miozB7LvwQKia`) — activo, schedule diario 08:30 + webhook `POST /webhook/alertas_inactividad`.
- Detecta leads sin actividad según umbral: Post-visita → 3d, Lead Caliente → 2d, Buscando vivienda (3 pools) → 14d.
- Crea tarea Follow-up (`task_type_id:1`) al `responsible_user_id` del lead: *"Sin actividad hace X días — revisar lead"*, fecha límite mañana.
- Dedupe 7 días vía `staticData.alertados`.
- Stage "En seguimiento" (`107269819`) disponible para mover manualmente.

### Workflow Especialista Asignado — DESACTIVADO
- `YGnefIXAKNJMZTw3` desactivado 2026-06-08. El agente ya se asigna solo vía campo `agente:` en Idealista. Salesbot 87867 y plantilla `agente_asignado` (72401) sin uso.

### Automatizaciones y Emails — estado (sobre los 5 requisitos originales)
| # | Requisito | Estado |
|---|---|---|
| P1 | Confirmación al cliente al enviar formulario | ✅ HECHO (WA + email desde `OFGGroWlifA88YFN`) |
| P2 | Confirmación visita por WA + email | ✅ HECHO (salesbot 87865 + email `iMoTKZWxYLymGuHF`) |
| P3 | Aviso interno al equipo (visita agendada) | ⏳ PREPARADO, SIN ACTIVAR — espera emails reales de 8 agentes |
| P4 | Seguimiento post-visita 48h | ✅ HECHO (Recordatorios + email post-visita) |
| P5 | Alertas por inactividad | ✅ HECHO (`Alertas_inactividad`) |

## Pendientes no bloqueantes

- **Caso 3 voz "lead pre-existente del formulario"**: cuando llaman al `+34 919 93 28 52` clientes que vienen de form `contacto_propiedad`, Ana saluda genérico aunque el lead ya tiene `property_ref` en Kommo. Solución diferida: workflow `Voz_lookup_lead` que matchea `from_number` → lead Kommo → devuelve dynamic variables (`{{nombre}}`, `{{property_interes}}`) que Retell inyecta en el prompt al inicio. Decisión Manu 2026-05-04: dejarlo para cuando Ramón vea volumen real de llamadas-formulario; ahora cubre el caso 1 (cliente describe vivienda con palabras → Buscar_viviendas la encuentra)
- Migrar `Mirar_disponibilidad` GCAL → Kommo tasks (decisión 5C completa)
- Crear sub-workflow `Solicitar_confirmacion_visita` (sustituir Opción 1 por Opción 2)
- Desplegar Supabase en Dokploy (RAG chatbot — workflow `meter info rag` inactivo hasta entonces)
- Templates email personalizados al cliente por formType (cuando SMTP funcione)
- **URL Google Reviews** de Simarro → meter en nodo `Build email post-visita` (Recordatorios) reemplazando `GOOGLE_REVIEWS_URL_PLACEHOLDER`
- **Emails reales de 8 agentes** → para activar P3 (aviso interno de visita). SQL: `UPDATE agents SET email='...' WHERE agent_key='...';` + cambiar fallback RPC a email de Ramón + activar nodos `disabled:true` en `iMoTKZWxYLymGuHF`
- **Llamadas outbound** — pendiente respuesta de Ramón (opciones B post-visita voz 4-6h y C reactivación leads fríos). Plataforma: Retell ya activo, `POST /v2/create-phone-call`

## IDs y números clave

| Recurso | Valor |
|---|---|
| n8n base | `https://n8nsimarro.agentesia.madrid` |
| Webhook forms web | `/webhook/80f01ee4-5e87-4d2d-9eeb-3786cfb18fbd` |
| Webhook chatbot | `/webhook/simarro` |
| Webhook agente asignado | `/webhook/especialista_asignado` |
| Webhook voz mirar disponibilidad | `/webhook/mirar_disponibilidad` |
| Webhook voz reservar | `/webhook/Reservar_crm` |
| Webhook voz cancelar | `/webhook/cancelar_cita` |
| Webhook voz derivar | `/webhook/derivar_humano` |
| Webhook voz buscar viviendas | `/webhook/voz_buscar_viviendas` |
| Kommo subdominio | `simarro.kommo.com` |
| Kommo account_id | `36342583` |
| Cred Kommo n8n | `xPvEqRp6NQwORUXi` |
| Cred Postgres n8n | `NbSEPfQRe9htaaYm` |
| Retell agent | `agent_7b02aa7680b8798ea033fab2c2` |
| Teléfono WhatsApp + voz Retell | `+34 919 93 28 52` |
| Teléfono móvil Ramón (transfer humano) | `+34 629 12 78 16` |

## Lessons learned aplicables a otros clientes

- **Credenciales fantasma heredadas**: ver `Stack/n8n.md` sección dedicada. Aplicable en CADA replicación
- **WhatsApp Cloud API limitación**: ver `Stack/kommo.md` sección "WhatsApp Cloud API + Salesbots"
- **Plantillas Kommo + custom fields**: el dropdown de placeholders solo muestra fields que ya existen en Kommo del cliente. Crear fields ANTES de plantillas
- **Decision approach segmentación pipelines vs tag**: 4 pipelines distintos con flujos comerciales propios > 1 pipeline + tag formType (este último colapsa naturaleza distinta de cada lead)
