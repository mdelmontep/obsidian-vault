---
title: Retell — webhooks y agent versioning
date: 2026-05-07
source: panel-tecnocloud · feat/voice-webhook-tickets
tags: [retell, webhooks, hmac, voice]
---

# Retell — Webhooks y Agent Versioning

Aprendido implementando `panel-tecnocloud` /api/webhooks/retell con el agente Tecnocloud. Verificado contra el SDK oficial `retell-sdk@5.18.0`.

## Firma de webhooks

- Header: `x-retell-signature: v=<unix_ms>,d=<hex_64>`
- Algoritmo: **`HMAC-SHA256(api_key, body + timestamp)`** — concatenado, sin separador, sin `.` ni nada. El timestamp es el `v=` numérico (ms desde epoch) coerced a string.
- Replay window: Retell SDK acepta ±5 minutos por defecto.
- Secret: el API key del workspace (mismo `key_*` que se usa para llamar la API).
- Si tu implementación falla con `digest_mismatch` y el SDK oficial dice `Retell.verify(body, apiKey, sig) === true`, el bug es tuyo. Diferencias típicas:
  - Firmar solo `body` en vez de `body + timestamp`.
  - Comparar `digest === d` con `===` (no timing-safe).
  - Encoding del body distinto al raw bytes recibido (`req.text()` debe leer ANTES de cualquier parse).

Implementación canónica (Node):

```ts
const expected = crypto
  .createHmac("sha256", apiKey)
  .update(rawBody + String(timestamp), "utf8")
  .digest("hex")
return crypto.timingSafeEqual(Buffer.from(d, "hex"), Buffer.from(expected, "hex"))
```

## Eventos del agent webhook

`webhook_url` del agente recibe 3 eventos:

- `call_started` — al iniciar (sin transcript ni recording).
- `call_ended` — inmediato al colgar (sin recording aún, sin call_analysis).
- `call_analyzed` — post-procesado (~5-30s tras colgar). **Único que trae transcript final, recording_url, duration_ms y `call_analysis`** (summary, sentiment, etc.).

`call_analyzed` se dispara para TODA llamada conectada, no solo "exitosas". Si quieres filtrar (ej. solo crear ticket si Laura invocó cierta tool), inspecciona `call.tool_calls[]` en el payload — array con `name`, `tool_call_id`, `success`, `latency_ms`. Los `arguments` de cada tool call están aparte en `call.transcript_with_tool_calls[]` (item con `role: "tool_call_invocation"`).

Si `call_analyzed` falla en su pipeline interno (raro), no llega. `call_ended` sí. Para fiabilidad total → cron de reconciliación con `list-calls` API.

## Tools mid-call vs call_analyzed

Cuando Retell invoca una **tool** durante la llamada (POST a tu webhook con `name`, `args`, `call`), el `call_status` es `"ongoing"` y NO trae:

- `recording_url`
- `duration_ms`
- `end_timestamp`
- transcript completo (solo parcial hasta el momento del tool call)
- `call_analysis`

Para datos completos → suscribir el agent webhook a `call_analyzed` post-call. El `transcript_with_tool_calls` de `call_analyzed` SÍ incluye los args que pasaste a las tools mid-call, así que no pierdes nada.

## Agent versioning

- Cada PATCH a `update-agent` crea/actualiza una **versión draft** (incrementa `version`).
- Los **phone numbers** anclan `inbound_agent_version` explícita en su config.
- Si actualizas webhook_url vía `update-agent`, eso va a la nueva versión draft. **Pero las llamadas en vivo siguen usando la versión que tenga el phone number** — no la última.
- Para hacer efectivo el cambio: PATCH al phone con `update-phone-number/+34XXX` con `inbound_agent_version: <nueva>`.
- `is_published: false` no significa que el agente esté apagado; significa que el último draft no está publicado. La versión activa es la que el phone tiene anclada.
- `version: 0` en phone = "latest version automáticamente".

## Recording URLs

- `opt_in_signed_url: false` (default en muchas cuentas) → URLs CloudFront públicas estables. No expiran.
- `opt_in_signed_url: true` → URLs firmadas con expiración. Hay que descargar a tu storage si quieres conservarlas.
- Política conservadora: si tu app tiene RBAC para grabaciones (no todo el mundo debe escucharlas), descarga siempre a tu storage independientemente del flag.

## Gotchas operativos

- **`api.retellai.com/list-keys` y similares devuelven "Unauthorized: Invalid JWT"** — necesitan dashboard JWT, no API key. La key tiene scope limitado al SDK.
- **Endpoints en docs vs reales**: usar la base `https://api.retellai.com` con paths como `/get-agent/{id}`, `/update-agent/{id}` (PATCH), `/list-phone-numbers`, `/update-phone-number/{phone}`, `/v2/list-calls` (POST), `/v2/get-call/{id}`. Mezcla de v1 y v2 según endpoint.
- **OpenAI key hardcoded en `jsCode` de n8n**: si en un workflow Retell+n8n hay summarization, suele estar como string literal en el Code node. Mover a `$vars.OPENAI_API_KEY` o credencial.
