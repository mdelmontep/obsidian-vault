---
title: la impersonación de superadmin no sirve para QA de UIs org-scoped
date: 2026-06-22
source: claude-code-session
tags: [facturaia, qa, impersonation, gotcha]
---
QArear features org-scoped (listas RLS + feature gating) **impersonando** como superadmin engaña:

1. **Caduca a la hora** (cookie de impersonación TTL deslizante ~1h). Tras horas: sidebar colapsa a lo mínimo, banners gated dejan de pintar — sin error visible, el banner "MODO VISTA" sigue ahí.
2. **El proxy `/api/admin/impersonate/query` reimplementa solo parte de PostgREST** → las **listas paginadas** (bandeja, recibidas, conciliación: usan `.range()`/count) vuelven **vacías**, aunque haya datos. El SSR-seed muestra algo y el refetch lo vacía = **parpadeo**.
3. Mezcla traicionera: un endpoint API propio (con `?org_id`+service-role, p.ej. el banner de muestreo) SÍ ve los datos → el banner aparece pero la lista de la página no → "algo va mal" que no es bug.

**Fix de QA**: probar como **usuario real** de la org (login directo o magic link / `generateLink`), no impersonando. Playwright headless logueando con un user real de la org test = verificación fiable. Caso 2026-06-22: horas perdidas creyendo que el muestreo fallaba; como usuario real, 100% OK.
