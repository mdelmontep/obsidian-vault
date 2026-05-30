---
title: Env con fecha mal formada → fail-closed, no fail-open
date: 2026-05-30
source: facturaia Fase 2 follow-up audit — SIGNING_LEGACY_UNTIL
tags: [auth, env, fail-closed, hardening]
---

Las env vars con fecha (cutover, expiración, deadline) que parsean a `NaN` deben **deshabilitar la funcionalidad protegida**, no extenderla por defecto "conservador". Un typo del operador en Dokploy (`2027-13-99T`, `2026-07-01` sin la `T` del ISO, etc.) no debería ampliar la ventana de un fallback inseguro indefinidamente.

Patrón:

```ts
function legacyEnabledNow(): boolean {
  const until = process.env.SIGNING_LEGACY_UNTIL
  if (!until) return true               // sin fecha → permisivo (dev)
  const ts = Date.parse(until)
  if (!Number.isFinite(ts)) {
    console.error('[auth] SIGNING_LEGACY_UNTIL no parsea — legacy DESHABILITADO', { value: until })
    return false                        // fail-closed
  }
  return Date.now() < ts
}
```

Por qué `false` y no `true`:
- Si el plan era cortar el día X y el operador mete typo, queremos que se entere YA (errores 401 en producción → alerta) en lugar de "todo sigue funcionando" silencioso.
- El `console.error` deja huella en monitoring para investigar el typo.
- El caso "sin fecha definida" sí permanece permisivo porque es señal de "todavía no estamos en migración" (entornos dev).

Contraejemplos donde sí prefieres fail-open (y por qué NO aquí):
- Flag de feature opcional → si parsea mal, mejor ignorar el flag y comportarte como default. Pero `SIGNING_LEGACY_UNTIL` no es feature flag — es cutover de auth, lado seguro = cerrar.

[[migracion-auth-sin-downtime-con-signing-legacy-until]]
