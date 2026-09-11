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
- **PATCH a un custom field `select` con un valor que no sea EXACTAMENTE una de sus opciones (como string) rechaza el `custom_fields_values` ENTERO del payload** con 400 genérico — no solo ese campo. Si mandas otros campos válidos (texto/numérico) en la misma llamada, también se pierden. Confirmar tipo real con `GET /leads/custom_fields` antes de escribir, nunca asumir por el nombre. Caso real Simarro: campo "Habitaciones" es `select` (`1`,`2`,`3`,`4`,`5+`), no numérico — mandar `2` (número) tumbaba zona y precio también
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

## WhatsApp Cloud API — conectar el canal y leer sus IDs

- **El "ID" que Kommo enseña bajo «Cuenta de WhatsApp Business» NO es el WABA ID, es el `phone_number_id`.** Confundirlos lleva a concluir que la integración apunta a una cuenta inexistente. Para comprobar qué es un ID de Meta: `business.facebook.com/latest/settings/whatsapp_account?...&selected_asset_id=<ID>&selected_asset_type=whatsapp-business-account`. **Nunca lo verifiques metiéndolo en `business_id=`**: si no corresponde, Meta no da error — hace *fallback silencioso* al portfolio por defecto y parece que el ID pertenece a otro cliente (me pasó con Laserys: casi mando ese diagnóstico falso a soporte).
- **El asistente de conexión se queda colgado en el spinner «estamos conectando tu número…» indefinidamente, pero la conexión SÍ se completa por detrás.** No es que la sesión te expulse. Esperar >2 min, recargar Kommo y reabrir el canal: aparece Conectado. Reintentar el asistente solo encadena spinners.
- Tras reconectar, si la ficha del canal sigue mostrando `unknown` en nombre de cuenta/negocio, «Límite de mensajes: Desconocido» y «Método de pago: No añadido», Kommo **no está leyendo los datos de la WABA** aunque el número figure Conectado — señal de que tampoco recibirá los webhooks de `messages`. Ver [[incidents]] 11-sep Laserys.
- **Sin plantillas aprobadas en la WABA el negocio no puede iniciar conversación nunca**, y sin ventana de 24 h abierta Kommo ni siquiera pinta el compositor de WhatsApp en el contacto (solo «Nota») → no hay forma de hacer un test de saliente. Comprobar el contador de plantillas en Meta antes de planificar cualquier prueba.
- Error **3123** («Vuelve a conectar tu número de teléfono a la integración») al enviar: es el síntoma genérico de canal desalineado, no dice nada de la causa.

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
- 87873 — Seguimiento post-visita +48h (además mueve el lead a Post-visita `107269815`)

Cada uno puede tener múltiples pasos; auditar por UI antes de cualquier debug.

**Qué etapa habla y cuál no** (medido 10-sep-2026 creando leads reales y mirando `/api/v4/events`):

| Etapa | ¿Bot al crear el lead ahí? |
|---|---|
| `105137095` Lead Caliente | **SÍ** — `outgoing_chat_message` 1 s después de `lead_added` |
| `107269819` En seguimiento / VISITA | no |
| `104515787` Pendiente de Asignar | no |
| `105358027` Visita valoración programada (embudo Valoraciones) | no |

Una integración que crea leads elige su etapa de destino **también por esto**, no solo por semántica.
Si hace falta una etapa garantizada muda, crear una nueva: nada puede estar atado a una etapa que no
existía. Ver [[el-inventario-de-automatismos-no-esta-solo-en-el-orquestador]].

## API REST v4 — quirks de escritura (jun 2026)
- **Vaciar un CF**: `values: null`, NO `values: []` (Kommo rechaza con `TooFew: should contain exactly 1 element` y tumba TODO el PATCH).
- **CF multiselect no refresca en vivo en la ficha** tras escritura por API: el panel muestra "Elegir" (vacío) aunque el valor SÍ está (verificable por API + activity log). Recargar la página. Texto/número/select-simple sí refrescan.
- **GET `/leads/{id}` único** requiere el **long-lived token** (cred `kommoLongLivedApi`); el Bearer "amojo" (scope chats) devuelve la **página de login HTML** (no autentica la API v4 REST).
- **`filter[id]=X` es inválido** (devuelve `{}`); usar `filter[id][]=X` o `/leads/{id}`.
- **No hay filtro por campo personalizado.** Solo `query` (texto libre sobre toda la entidad). Una importación masiva NO puede comprobar "¿ya existe esta ref?" contra Kommo: idempotencia por `request_id` + fichero propio de avance. Ver [[sin-filtro-por-campo-personalizado-la-idempotencia-va-por-request-id]].
- **PATCH a los `enums` de un CF los REEMPLAZA.** Para añadir un valor hay que reenviar los existentes **con su `id`**; mandar solo el nuevo borra el resto (y con ellos el dato de las entidades que lo usaban). Instancia de [[put-objeto-completo-borra-campos-no-mapeados]].
- **No se pueden BORRAR leads por API** (medido 10-sep-2026 en Laserys): `DELETE /api/v4/leads/{id}` y `DELETE /api/v4/leads` con cuerpo devuelven **405**, y `POST /api/v4/leads/delete` **404**. El borrado es solo desde la interfaz → los leads de prueba de un E2E se quedan; aparcarlos en el status de perdido y renombrarlos `ZZ TEST…` para que alguien los borre a mano.
- **Kommo NO deduplica al crear por API** — su control de duplicados es solo para leads entrantes. La deduplicación es del integrador.
- **`created_by: 0` no identifica la integración**, solo dice "no fue un usuario en la UI"; una creación por API con tu propio token sale igual. Quien delata la cuenta es `responsible_user_id`. Ver [[un-created-by-0-no-atribuye-el-control-es-crear-la-entidad-tu-mismo]].
