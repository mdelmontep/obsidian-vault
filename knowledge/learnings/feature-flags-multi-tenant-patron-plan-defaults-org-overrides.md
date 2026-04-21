---
title: feature flags multi-tenant patron plan defaults org overrides
date: 2026-04-21
source: claude-code-session
tags: [saas, supabase, feature-flags, arquitectura]
---

Patrón para feature flags en SaaS multi-tenant con planes:

## Modelo de datos

- `features` — catálogo global (id, nombre, category, core, activo)
- `plan_features` — defaults por plan (plan, feature_id, enabled)
- `org_features` — overrides por organización (org_id, feature_id, enabled)
- `feature_dependencies` — dependencias entre features (feature_id, depends_on)

## Resolución

Orden de prioridad: override org > default plan > false.

```sql
CREATE FUNCTION org_has_feature(p_org_id UUID, p_feature_id TEXT) RETURNS BOOLEAN AS $$
  -- 1. Core features siempre activas
  -- 2. Override org_features si existe
  -- 3. Default plan_features
  -- 4. False
$$ LANGUAGE sql SECURITY DEFINER;
```

## Client-side (React)

`FeatureProvider` carga features via Supabase client:
- **Fail-open**: si falla el fetch, `Set<string>` vacío → nada oculto (mejor mostrar de más que de menos)
- **Polling 5min** + `visibilitychange` reload (cuando el usuario vuelve a la pestaña)
- `useFeature(id)` devuelve `{ enabled, ready }`
- `<Feature id="x">children</Feature>` wrapper component

## Billing state machine

trial → grace_period → expired → active/suspended/cancelled

**Lazy expiration** (sin cron): el server layout evalúa `trial_ends_at + grace_days` en cada request. Si expiró, transiciona automáticamente via `change_billing_status()` RPC.

## Admin

`createAdminClient()` con `SUPABASE_SERVICE_ROLE_KEY` bypasses RLS. Doble barrera: middleware redirect + server layout `isSuperadmin()` check. Superadmin via `SUPERADMIN_EMAILS` env var o `profiles.is_superadmin` flag.
