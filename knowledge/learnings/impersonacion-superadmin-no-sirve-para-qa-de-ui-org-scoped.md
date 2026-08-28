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
4. **En su forma extrema la página entera da 404** (07-ago-2026): impersonando a IET, las rutas `/obras/*` responden "Esta página no existe" mientras el sidebar las enlaza y `GET /api/obras/settings` devuelve la org correcta. Sidebar y API resuelven la org impersonada; la página no. Como usuario real de una org con Obras cargan bien. Corolario: un 404 impersonando no prueba que la ruta esté rota para el cliente, hay que rehacerlo como usuario real antes de abrir un bug.

**Fix de QA**: probar como **usuario real** de la org (login directo o magic link / `generateLink`), no impersonando. Playwright headless logueando con un user real de la org test = verificación fiable. Caso 2026-06-22: horas perdidas creyendo que el muestreo fallaba; como usuario real, 100% OK.

5. **Y para ESCRIBIR no sirve en absoluto, con el candado en la mitad cómoda** (28-ago-2026): el interceptor de cliente (`src/lib/impersonate-client.ts`) veta los métodos de escritura del navegador, pero la misma API acepta la escritura del superadmin por `?org_id=`. Resultado: no protege la vía peligrosa y bloquea la única útil, que es **rehacer el gesto del cliente** cuando un bug le dejó el dato a medias. La vía limpia es la que el producto ya tiene: darse de alta como miembro de su org (`POST /api/admin/orgs/[id]/members`, `mode:'create'` reutiliza el auth user y no manda email ni cambia la contraseña), actuar por su propia UI —mismas RPC, mismo `audit_log`— y darse de baja con `PATCH {action:'remove_member'}` al terminar. Ojo: al cambiar de org con `POST /api/auth/switch-org` se **borra la cookie `impersonate_org`**, que es justo por lo que este camino escapa del bloqueo de solo lectura. Caso real: ticket 159, dos facturas de un cliente reparadas así en prod.
