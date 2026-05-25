---
title: Cuando fallback rescata, conservar error del canal primario en audit
date: 2026-05-16
source: claude-code-session
tags: [observabilidad, fallback, retry, audit, gotcha]
---

Patrón típico de fallback automático:

```ts
const r = await sendPrimary()
if (!r.ok) {
  error = r.errorCode
  const fb = await sendFallback()
  if (fb.ok) {
    error = null  // ← BUG: pierde visibilidad del fallo primario
  }
}
```

Si solo loggeas/auditas `error` final, **nunca te enteras** de que el canal primario falla sistemáticamente — el sistema "funciona" porque el fallback rescata, pero estás pagando dos llamadas, gastando cuota dual, y arrastrando latencia extra sin saberlo.

**Fix**: variable separada para "error del canal preferente" que SIEMPRE va al audit, independiente del éxito del fallback.

```ts
let primaryError: string | null = null
let finalError: string | null = null
const r = await sendPrimary()
if (!r.ok) {
  primaryError = r.errorCode
  finalError = primaryError
  const fb = await sendFallback()
  if (fb.ok) { finalError = null }  // solo el final se borra
}
audit.insert({ error_code: finalError ?? primaryError })
```

**Caso real TuFacturaIA**: OTP WhatsApp fallaba 132001 todas las veces, email Resend rescataba, audit marcaba `start ok` con `meta_error_code: null` → invisible 3h hasta que el agente añadió `primaryChannelError`.
