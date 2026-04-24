---
title: cambiar plan debe invalidar todos los datos derivados
date: 2026-04-25
source: claude-code-session
tags: [facturaia, admin, frontend]
---

Al cambiar el plan de una org en el admin, se recargaban features pero NO limits. Los limits quedaban cacheados en React state con los valores del plan anterior (ej: enterprise 99999 → starter 50, pero la UI seguía mostrando 99999).

**Fix**: al hacer `updateOrg({ plan })`, recargar en paralelo todos los datos que dependen del plan:

```ts
if (fields.plan) {
  const [featRes, limRes] = await Promise.all([
    fetch(`/api/admin/orgs/${id}/features`),
    fetch(`/api/admin/orgs/${id}/limits`),
  ])
  setFeaturesData(await featRes.json())
  setLimitsData(await limRes.json())
}
```

**Regla general**: cualquier campo que sea FK o clave de lookup (plan, billing_status, etc.) puede afectar datos en múltiples tabs/vistas. Al cambiarlo, invalidar todos los caches dependientes, no solo el más obvio.
