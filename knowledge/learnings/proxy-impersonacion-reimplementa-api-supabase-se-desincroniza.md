---
title: Proxy de impersonación que reimplementa la API de Supabase se desincroniza en silencio
date: 2026-06-15
source: TuFacturaIA PR #264 (conciliación rota impersonando org de Borja)
tags: [supabase, impersonacion, superadmin, proxy, react, facturaia]
---

En TuFacturaIA, impersonar como superadmin no usa el browser client real: `useOrgClient()` devuelve un **proxy casero** (`impersonate-client.ts`) que serializa cada query encadenada y la reenvía a `/api/admin/impersonate/query`, donde se ejecuta con service-role acotada a `org_id`.

**Bug 1 — el proxy reimplementa a mano un subconjunto de PostgREST y se queda corto.** El builder no tenía `.not()`, `select({count,head})` ni `maybeSingle()`. Conciliación (la vista con más queries) los usa → `TypeError` → carga reventaba. Las vistas que solo usan `eq/in/order` no lo notaban. Fix: **lista única compartida** de métodos de filtro que el builder expone y el servidor valida + test de paridad (no pueden divergir).

**Bug 2 — bucle infinito.** `useOrgClient()` creaba un proxy **nuevo en cada render** (el browser client de `@supabase/ssr` es singleton, por eso en sesión normal no pasa). El efecto de carga depende del cliente → re-render → cliente nuevo → re-fetch → error → bucle de toasts (y de `logAdminAction`). Fix: `useMemo([orgId, isImpersonating])`.

Regla: un proxy que duplica la superficie de un SDK es deuda silenciosa — sincronízalo con un contrato único + test, y memoiza cualquier cliente que alimente dependencias de efectos. Ver [[effect-reload-por-entidad-setters-merge-exigen-reset]] · [[supabase-errores-que-solo-afloran-contra-schema-real]].
