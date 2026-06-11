---
title: Clientify — gotchas y API quirks
date: 2026-06-11
source: elphis-doctoralia-email-sync smoke tests
tags: [clientify, crm, api, elphis]
---

# Clientify

CRM usado en Centro Elphis. API base: `https://api.clientify.net/v1/`. Auth: `Authorization: Token <key>`.

## Gotchas API

### `GET /v1/deals/?contact=<ID>` ignora el filtro de contacto
El parámetro `contact` se acepta sin error pero **devuelve todos los deals del pipeline**, no los del contacto. Filtrar client-side:
```javascript
const contact_id = String(ctx.contact_id);
const mine = deals.filter(d => {
  const c = String(d.contact || '');
  return c === contact_id || c.endsWith('/' + contact_id + '/');
});
```
Clientify devuelve el campo `contact` como URL (`https://api.clientify.net/v1/contacts/ID/`), de ahí el check con `.endsWith`. Ver [[elphis-doctoralia-email-sync-2026-06-11]]

### Campo `description` del deal: sin HTML, sin saltos de línea
Clientify strips etiquetas HTML y newlines. Solo renderiza texto plano continuo. No usar `<b>`, `<br>`, `\n`. Separador de campos legible: ` · ` (punto medio). Ejemplo: `Origen: Doctoralia · Fecha: 18/06/2026 a las 10:00h · Servicio: Primera visita`.

## Modelo de datos (Elphis)

- `contact` → paciente o familiar. Campos: `id, first_name, last_name, emails[], phones[], tags[], custom_fields[]`.
- `deal` → oportunidad/cita. Campos: `id, contact (URL), name, pipeline, pipeline_stage, status (1=open/2=won/3=lost), description`.
- `tags` y `custom_fields` embebidos en cada objeto. No hay endpoint `/v1/tags/` ni `/v1/customfields/` (404).

## Pipeline Centro Elphis (`56886`)

| Stage ID | Nombre | Cuándo |
|---|---|---|
| `243847` | Entrada Lead Nuevo | bot detecta interés |
| `243848` | Cliente contactado | bot ya conversó |
| `260088` | Volver a contactar | fuera horario / callback |
| `243914` | Cliente a contactar Profesional | handoff humano |
| `243849` | 1ª Visita Programada | cita agendada |
| `243850` | 1ª Visita Realizada | equipo mueve manualmente |

## Notas adicionales

- **Webhooks**: sin firma HMAC documentada → proteger endpoint n8n con token en query + IP allowlist.
- **Custom fields** se envían por ID interno, no por nombre.
- **Phone matching**: normalizar a E.164 antes de buscar; URL-encode el `+`.
- **Throttle**: lookup primero contra `paciente_cache` (Postgres), fallback a API. Backoff exponencial.
