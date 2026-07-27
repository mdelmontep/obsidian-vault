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

⚠️ **El "deadline real" solo existe si alguien pone la variable (auditoría 2026-07-27).**
Dos meses después, `SIGNING_LEGACY_UNTIL` seguía sin fijarse en Dokploy → `if (!until)
return true` mantiene la ventana ABIERTA indefinidamente, y como el legacy **no ata
método, path ni body**, el HMAC v2 queda cosmético: un secreto filtrado sirve contra
cualquier ruta interna, que es justo el replay horizontal que v2 vino a cerrar.
El patrón no falla, falla no cerrarlo. Al implementarlo: (1) crear ya la tarea de
cutover con fecha y dueño, no "cuando migremos"; (2) **persistir** cada uso de legacy
en una tabla consultable (`admin_audit_log`), no solo `console.warn` — sin ese dato no
se puede cerrar con seguridad, porque los emisores (n8n, schedules) viven fuera del
repo y no hay forma de saber desde el código si alguien sigue usándolo; (3) el código
evolucionó a fail-**closed** ante fecha mal formada, pero sigue fail-**open** ante
variable ausente: son casos distintos y conviene saberlo.

Secrets distintos (no derivar el nuevo del viejo): un compromiso de la key vieja no permite firmar peticiones nuevas. Cada secret se rota independiente. `openssl rand -hex 32` para el nuevo.

Anti-replay del nuevo formato: tolerancia ±5min sobre `t=<unix>` (mismo modelo que Stripe). HMAC sobre `${t}.${sha256(body)}` — el cuerpo no es manipulable.

[[2fa-telefono-solo-para-canal-que-lo-usa-no-gate-global]]
