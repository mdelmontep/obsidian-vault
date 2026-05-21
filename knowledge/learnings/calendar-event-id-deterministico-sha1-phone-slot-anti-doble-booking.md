---
title: calendar event id determinista sha1 phone+slot evita doble booking
date: 2026-05-22
source: claude-code-session
tags: [google-calendar, idempotency, voice-agent]
---

Voice agents reintentan webhooks de tools si el endpoint tarda más del timeout (Retell: 2x retries automáticos). Sin idempotency → 2 ejecuciones simultáneas → 2 eventos en Google Calendar.

**Patrón**: pasar `id` explícito al crear evento con valor determinista derivado de los argumentos:

```js
const crypto = require('crypto');
const event_id = crypto.createHash('sha1')
  .update(`${phone}${slot_iso}`)
  .digest('hex').slice(0, 32);
// Google Calendar acepta id custom alfanumérico minúsculas, max 1024 chars
// Si ya existe → 409 nativo, no duplica
```

Ventaja sobre Redis lock: cero estado externo, idempotency garantizada por Google. Si el retry pasa, falla con 409 limpio (capturable con `onError: continueRegularOutput`).

Combinable con Redis SETNX adicional `reservar:${call_id}:${matricula}` TTL 1h para devolver `confirmation_text` cacheado al cliente sin tocar Calendar dos veces.

Caso real: EcoBox 2026-05 — workflow `Reservar_cita`.
