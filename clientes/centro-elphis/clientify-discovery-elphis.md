---
title: Centro Elphis — Discovery Clientify
date: 2026-05-18
source: API discovery contra api.clientify.net/v1/ con API key de Elphis
tags: [elphis, clientify, crm, ids, discovery]
---

# Discovery Clientify · Centro Elphis

Hecho contra `https://api.clientify.net/v1/` con `Authorization: Token <key>`. Credenciales en memory: [clientify-elphis-api](~/.claude/projects/-Users-manueldelmonte/memory/clientify-elphis-api.md).

## Volumen actual

- **1.807 contactos** · **1.334 deals** activos. CRM en uso real, no sandbox.
- Implicación: integramos con cuidado quirúrgico para no contaminar datos existentes.

## Pipeline operativo

**ID 56886 «Centro Elphis»** (no usar el 54955 «Por defecto»):

| Stage ID | Nombre | Rol en flujo IA |
|---|---|---|
| 243847 | Entrada Lead Nuevo | Estado inicial. Bot crea el deal aquí al detectar interés. |
| 243848 | Cliente contactado | Bot ya conversó con el lead. |
| 260088 | Volver a contactar | Fuera de horario o callback solicitado. |
| 243914 | Cliente a contactar Profesional | Handoff humano: recepción debe llamar. |
| 243849 | 1ª Visita Programada | Bot agendó primera visita con Enrique. |
| 243850 | 1ª Visita Realizada | Equipo lo mueve manualmente tras la cita. |

Estado del deal (`open`/`won`/`lost`) es independiente del stage. Cancelaciones → `lost` con motivo en custom field.

## Users relevantes

| ID | Usuario | Rol |
|---|---|---|
| 133648 | Kike (Enrique) Sanz · enriquesanz@centroelphis.com | Director, firmante DPAs, único profesional que atiende primera visita |
| 135909 | Alba Orgaz · alba.orgaz@centroelphis.com · +34 687 448 210 | Contacto operativo, admin |
| 351566 | Borja Chivite · bgchivite@agentesia.madrid | Owner por defecto de deals creados por el bot |
| 134549 | Olga González · hola@centroelphis.com | Cuenta general centro |
| 337983 | Pablo Rubio · pablo.ruma@gmail.com | Admin |
| **320983** | **Laura Spiroox · meta@spiroox.com** | **Externo, agencia Spiroox, admin** |
| **319787** | **Pepe Framis · pepe.framis@spiroox.com** | **Externo, agencia Spiroox, admin** |
| 128446 | Jorge Pérez Gusano | Clientify support |
| 136598 | Cristina Osuna | Clientify support |

> **Heads up Spiroox**: dos admins externos con acceso completo. Antes de crear campos custom o tocar el pipeline, confirmar con Alba si tienen automatizaciones activas que no debamos pisar. Ver [[bloqueantes-elphis]].

## Limitaciones técnicas (vs Kommo)

- **Sin endpoint público para webhooks** (`GET /v1/webhooks/` = 404). Se configuran desde panel UI · Configuración · Webhooks. Sin firma HMAC documentada, protegemos endpoints n8n con token en query + IP allowlist.
- **Sin endpoint para listar custom fields ni tags**. Vienen embebidos en cada `contact`/`deal`. Crearemos los necesarios desde panel y anotaremos IDs.
- **Sin motor de bots tipo salesbot Kommo**. Los mensajes WhatsApp salen vía Chatwoot API o WA Cloud directo desde n8n.
- Auth: API key con header `Authorization: Token <key>`. Sin OAuth público. Rate limit no documentado, asumimos ~60 req/min con backoff exponencial.
- Phone matching: normalizar a E.164, URL-encode el `+` (gotcha clásico).
- Custom fields se envían por ID interno, no por nombre. Cachear `GET /custom-fields/` desde panel.

## Modelo de datos

**Contact campos top-level**:
`id, first_name, last_name, emails[], phones[], tags[], custom_fields[], addresses[], company, owner, gdpr_accept, gdpr_acceptance_date, status, contact_source, channel, medium, last_contact, ...`

**Deal campos top-level**:
`id, contact, name, amount, currency, pipeline, pipeline_stage, status, tags[], custom_fields[], deal_source, expected_closed_date, owner_name, ...`

## Custom fields que vamos a necesitar crear

Pendiente con Alba antes de tocar nada:

- En contact: `relacion_paciente` (paciente/familiar/conocido), `gdpr_canal` (WhatsApp/voz), `bot_intent_final`, `audio_url_ultima_llamada`.
- En deal: `sustancia_o_conducta`, `urgencia` (alta/media/baja), `tipo_consulta` (primera_visita/ingreso/info/callback), `transcript_resumen`, `motivo_no_visita`, `gcal_event_id`.

## Relacionado

- [[index|Centro Elphis HUB]]
- [[arquitectura-elphis]]
- [[bloqueantes-elphis]]
