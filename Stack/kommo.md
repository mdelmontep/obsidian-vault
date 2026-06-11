---
title: stack kommo — gotchas y patrones
date: 2026-05-03
source: claude-md-migration
tags: [kommo, crm, whatsapp, salesbots, api]
---

# Stack Kommo

## API REST

- **Long Lived Token**: integraciones privadas → Keys and scopes. Hasta 5 años sin refresh
- **Subdominio cuenta**, NO `api-c.kommo.com` (aunque el JWT diga lo contrario en `api_domain`)
- `amojo_id` por cuenta — distinto al `account_id`. Sacar con `GET /api/v4/account?with=amojo_id`
- DELETE de leads NO permitido vía API (devuelve 405). Tampoco contactos ni tareas. Para "borrar" hay que mover a status `Closed - lost` (id `143` global) o eliminar a mano en la UI. Implicación tests E2E: todo lead/contacto creado en un test real requiere limpieza manual en UI — anotar IDs durante el test
- Status terminales globales por account: `Closed - won` (`142`), `Closed - lost` (`143`). Aparecen en CADA pipeline automáticamente
- Pipeline POST requiere campos `is_main`, `is_unsorted_on`, `sort` o devuelve 400
- Pipeline al crearse genera además un status `Incoming leads` (type=1) que normalmente no se usa en flujos n8n
- Custom field IDs ÚNICOS por account, no por pipeline. Una vez creado, el ID sirve en cualquier pipeline
- Custom field `select` requiere `enums: [{value: "..."}]` en POST
- Task types NO se crean vía API, solo UI Kommo (Settings → Tasks)
- Users: `GET /api/v4/users` da `id, name, email`. El user "principal" del cliente es el que se usa como `responsible_user_id`

## Templates WhatsApp (Kommo es el BSP)

- **NO se crean en business.facebook.com**. Se crean **dentro de Kommo** (Robots → Plantillas WhatsApp). Kommo las envía a Meta para aprobación automáticamente
- En Kommo el editor muestra placeholders con NOMBRE legible (`[Nombre del contacto]`, `[Día de visita]`, `[Especialista asignado]`) basado en los custom fields del LEAD que existen en la cuenta
- **Si el custom field no está creado en Kommo, el placeholder no aparece en el dropdown**. Crear primero los campos custom, luego la plantilla
- Internamente Kommo traduce los nombres a `{{1}} {{2}} {{3}}` al enviar a Meta
- Listar templates aprobados: `GET /ajax/v4/chats/templates?limit=25` (consola navegador en la cuenta Kommo, requiere sesión)
- El name visible vs el name interno snake_case pueden diferir — el ID es lo que importa
- Categoría Marketing por defecto. Confirmación de cita puede ir como Utility (más barata, a veces Meta la rechaza y hay que reenviar como Marketing)

## WhatsApp Cloud API + Salesbots Kommo (limitación clave)

- **Ventana 24h**: si el destinatario no escribió a la business en últimas 24h, **solo se entregan plantillas HSM aprobadas**. Un mensaje libre devuelve `wamid` exitoso pero NO llega al destinatario (Meta lo descarta sin error visible)
- **Salesbot que envía mensaje libre** (tipo "Chatbot IA" con campo custom como contenido) NO funciona si cliente no escribió antes. Para clientes que vienen de form web sin chat previo: NO disparar el salesbot conversacional directo
- **Patrón correcto para forms web → WhatsApp**:
  1. Form rellenado → crear lead en Kommo
  2. Disparar salesbot que envía **plantilla HSM aprobada** (ej. "Formulario gracias", "Solicitud_recibida")
  3. Si cliente responde al WhatsApp → window de 24h abierta → ya pueden enviarse mensajes libres y el chatbot conversacional toma la conversación
- **Tener templates distintos por contexto evita mensajes raros**:
  - Template invitando a responder (ej. "cuéntanos más para ayudarte mejor") → solo para forms breves tipo `contacto_propiedad` donde el cliente dio poca info
  - Template solo confirmación (ej. "hemos recibido, te contactamos en 24-48h") → para forms largos cualificables (valoración, capacidad) donde pedir "más info" es insultante porque ya rellenaron 8 campos

## Doble disparo salesbot — n8n + automation pipeline

Si un workflow n8n llama a `/api/v2/salesbot/run` para invocar un bot, **Y** ese mismo bot está configurado como automation del status del pipeline donde n8n acaba de crear el lead, **se dispara dos veces casi simultáneamente**. Síntoma típico: cliente recibe la misma plantilla WhatsApp dos veces en el mismo segundo.

Caso real Simarro 2026-05-04: Borja añadió bot 88575 ("Solicitud recibida") como automation del status "Nuevo lead" en los 4 pipelines de form web. El workflow `OFGGroWlifA88YFN` ya invocaba `/salesbot/run` con ese mismo bot tras crear el lead. Resultado: 2 plantillas idénticas a 0:41:00.

**Detección**: la API de eventos del lead (`/api/v4/events?filter[entity_id]=...`) NO muestra ejecuciones de salesbot, así que un test E2E con timestamp idéntico es la única forma de pillarlo.

**Patrón correcto**: elegir UNA fuente del envío.
- Opción A: bot SOLO como automation del pipeline status. n8n crea el lead y ya está. Más limpio para futuros mantenedores (config en Kommo UI, no en código).
- Opción B: bot SOLO invocado desde n8n. Útil cuando n8n necesita decidir qué bot usar (mapping dinámico por formType, etc.).
- Mixto válido (ver Simarro): IF condicional en n8n que solo invoca `/salesbot/run` para los formTypes cuyo bot NO está como automation. Los demás dependen de la automation del pipeline.

## Patrón salesbot: PATCH lead + POST salesbot/run

Para que el chatbot envíe un mensaje WhatsApp con texto dinámico, no se puede llamar directo a la API amojo. Usar:

1. **PATCH `/api/v4/leads`** con custom field "Mensaje salesbot" (textarea) cargado con el texto a enviar + status_id que dispare el bot
2. **POST `/api/v2/salesbot/run`** con `bot_id`, `entity_id` (lead_id), `entity_type: 2`

El salesbot está configurado con UNA acción: enviar mensaje WhatsApp con contenido `{{lead.cf.FIELD_ID}}`. Sin esa acción dentro del bot, el `salesbot/run` devuelve `success:true` pero no llega nada.

```json
PATCH /api/v4/leads
[{
  "id": LEAD_ID,
  "status_id": STATUS_DISPARADOR,
  "custom_fields_values": [{
    "field_id": FIELD_MENSAJE_SALESBOT,
    "values": [{"value": "Hola Manu, gracias..."}]
  }]
}]

POST /api/v2/salesbot/run
[{"bot_id": BOT_ID, "entity_id": LEAD_ID, "entity_type": 2}]
```

## Webhook Kommo → n8n

- **Tras PUT a un workflow vía API n8n, Kommo deja de mandar el webhook a ese workflow** aunque el endpoint responda OK. Bug conocido. Fix: borrar el webhook en Kommo (Ajustes → Integraciones → Webhooks) y volver a crearlo idéntico
- Webhook `status_lead` ("El estado del lead cambiado") dispara en TODOS los cambios de estado — filtrar con IF `status_id == X` después
- Webhook "Mensaje entrante recibido" SOLO trae texto del cliente. Otras acciones generan eventos sin contenido

## Salesbot IDs (sacar)

- `/api/v2/salesbot` REST devuelve 404 (es API privada)
- Sacar IDs desde el navegador con sesión activa Kommo:

```javascript
fetch('/ajax/v4/bots/?limit=100').then(r=>r.json()).then(d=>console.log(JSON.stringify(d._embedded.items.map(b=>({id:b.id,name:b.name})),null,2)))
```

## Pipelines y status — discovery completo

```bash
curl -s "https://${SUB}.kommo.com/api/v4/leads/pipelines" -H "Authorization: Bearer ${TOKEN}" \
  | jq '._embedded.pipelines[] | {id, name, statuses: ._embedded.statuses._embedded.statuses | map({id, name})}'
```

Custom fields del lead:
```bash
curl -s "https://${SUB}.kommo.com/api/v4/leads/custom_fields?limit=250" -H "Authorization: Bearer ${TOKEN}" \
  | jq '._embedded.custom_fields[] | {id, name, type}'
```

## Lecciones de replicación cliente nuevo

- Crear pipelines + custom fields ANTES de tocar workflows. Sin los IDs reales, los placeholders TODO en workflows fallan en silencio
- Los nombres de status NO tienen que coincidir entre clientes — lo que importa es el ROL en el flujo (status "donde el chatbot deja el lead antes de salesbot", status "donde Ramón recibe leads para asignar agente", etc.)
- Documentar el mapeo rol→status en CLAUDE.md del proyecto desde el día 1

---

## Gotchas Simarro voz (mayo 2026)

### Salesbot API v2 es PRIVADA
`/api/v2/salesbot/{id}` y `/api/v2/salesbot` (list) devuelven `{error_code: "110", error: "This is a private API"}`. Solo se pueden inspeccionar/editar desde la UI Kommo.

Implicación: si necesitas saber cuántos pasos tiene un salesbot (debug WhatsApp duplicado, etc), tienes que ir a `Setup → Salesbots → <bot_id>` en la UI. No hay vía API.

### WhatsApp duplicado tras Reservar — triage
Si tras una reserva el cliente recibe 2 WhatsApp y solo hay 1 ejecución n8n con 1 disparo a `/salesbot/run`:

1. **Salesbot tiene 2+ pasos `send_message`**: el bot, una vez disparado, ejecuta TODA su lógica interna y puede enviar varios mensajes consecutivos. Verificar UI → Setup → Salesbots → flow del bot. Si hay 2 cajas "Enviar mensaje" → borrar una.

2. **Digital Pipeline trigger** en el status al que se mueve el lead (`Lead Caliente`, `Cita programada`, etc): Kommo permite configurar "ejecutar bot al entrar en este status". Si está activo + n8n también dispara explícitamente = 2 envíos. Verificar: pipeline → click columna → engranaje → "Triggers/Automatizaciones".

n8n confirma 1 ejecución / 1 dispatch via:
```
GET /executions/{id}?includeData=true
→ runData.Send WA Confirmation Retell.length === 1
```
Si es 1 y aún recibe 2 WA → causa Kommo (1 o 2 arriba).

### Lead lookup por phone — desambiguación
`GET /api/v4/leads?query={phone}&with=contacts` devuelve TODOS los leads cuyo contacto tenga ese phone (full-text match). Si el mismo número pertenece a varios contactos (test playground con phone único, varios miembros familia, errores de captura), el primer match no es necesariamente el correcto.

**Patrón**: si la tool acepta también `name`, filtrar el array de leads devuelto por nombre del contacto antes de devolver el lead_id. Sin esto el voice agent puede operar sobre lead equivocado.

```javascript
// En Code node tras Buscar leads
let chosen = leads.find(l => l.pipeline_id === PIPELINE_PRINCIPAL && l._embedded?.contacts?.[0]?.name?.toLowerCase().includes(name.toLowerCase()))
            || leads.find(l => l.pipeline_id === PIPELINE_PRINCIPAL)
            || leads[0];
```

### Update lead sin pisar campos
Kommo PATCH `/api/v4/leads` con `custom_fields_values` SOLO actualiza los campos que envías; deja el resto intactos. Si quieres "limpiar" un campo, pasar `values: [{value: ""}]` o `values: []` según el field type — algunos requieren array vacío.

### Status IDs Simarro pipeline 13546071
Para referencia (no reusar en cliente nuevo, mapear los suyos):
- 104515783 — Incoming leads (legacy, no tocar)
- 105675587 — Lead entrante
- 105137095 — Lead Caliente (tras Reservar OK)
- 104515787 — Pendiente de Asignar
- 105137099 — Agente Asignado
- 105137131 — Derivado Humano
- 105137127 — Cancelado
- 105137103 — Formulario Web
- 142 — Logrado con éxito (success)
- 143 — Venta Perdido (fail)

### Custom fields IDs Simarro
- 1330871 — Día de Visita (`CF_SCHEDULER_UPCOMING_APPOINTMENT`, type date_time, value timestamp seconds)
- 1372567 — Motivo consulta (textarea)
- 1372569 — Fuente IA (text)
- 1373305 — Property reference / idealista_id (text)
- 1373349 — Vivienda dirección (text)
- 1373351, 1373353, 1373355, 1373357 — precio, m², habitaciones, URL (sin verificar IDs exactos en cada session)

### Bots conocidos
- 87865 — Confirmación cita Retell (WhatsApp tras Reservar voz)
- 87871 — Recordatorio 24h
- 87861 — Recordatorio 4h
- 88183 — Chatbot Simarro WhatsApp (chat asíncrono)

Cada uno puede tener múltiples pasos; auditar por UI antes de cualquier debug.
