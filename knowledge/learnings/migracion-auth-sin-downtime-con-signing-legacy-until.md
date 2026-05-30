---
title: Migración de auth sin downtime con SIGNING_LEGACY_UNTIL
date: 2026-05-29
source: facturaia Fase 2 SaaS — HMAC X-Service-Signature
tags: [auth, migracion, hmac, sin-downtime]
---

Pasar de auth estática (header con secret fijo) a auth firmada (HMAC + timestamp) requiere coordinación con callers externos (n8n, scripts de cliente). Un cambio brusco rompe producción si UN solo caller queda sin actualizar.

Patrón: aceptar AMBOS formatos durante una ventana definida por env, log warn cada vez que entra legacy, y rechazar legacy automáticamente cuando expira la ventana.

```typescript
function legacyEnabledNow(): boolean {
  const until = process.env.SIGNING_LEGACY_UNTIL  // ISO 8601
  if (!until) return true                          // sin fecha → permisivo
  const ts = Date.parse(until)
  if (!Number.isFinite(ts)) return true            // mal formato → permisivo
  return Date.now() < ts
}

if (newSignatureHeader) verifyNew()
else if (legacyEnabledNow() && legacyHeader) {
  verifyLegacy()
  console.warn('[auth] caller usa legacy — migrar antes de SIGNING_LEGACY_UNTIL')
}
else reject()
```

Beneficios sobre flag boolean `LEGACY_ENABLED=true/false`:
- La fecha aparece en logs / dashboards: "migración termina el DD/MM" es accionable.
- Si olvidas desactivar, hay deadline real, no flag eterno.
- Para tests: env con fecha pasada → rechazo limpio sin acoplar lógica de boolean.

Secrets distintos (no derivar el nuevo del viejo): un compromiso de la key vieja no permite firmar peticiones nuevas. Cada secret se rota independiente. `openssl rand -hex 32` para el nuevo.

Anti-replay del nuevo formato: tolerancia ±5min sobre `t=<unix>` (mismo modelo que Stripe). HMAC sobre `${t}.${sha256(body)}` — el cuerpo no es manipulable.

[[2fa-telefono-solo-para-canal-que-lo-usa-no-gate-global]]
