---
title: router.refresh no remonta los client components y deja datos de la org anterior
date: 2026-07-29
source: claude-code-session
tags: [nextjs, rsc, multi-tenant, frontend]
---

Cambiar de organización/tenant con `router.refresh()` actualiza solo lo que se
pinta en el servidor. Los client components **no se remontan ni re-disparan sus
efectos**, así que todo lo que carga con `fetch` dentro de un `useEffect` de
montaje conserva su `useState` con los datos del tenant anterior.

Síntoma: el sidebar y las cifras del RSC cambian, la tabla no. Se lee como fuga
de datos entre tenants y no lo es — el endpoint filtra bien por `org_id`; es
estado cliente rancio. Mide el alcance antes de creer que es un caso aislado:
en FacturaIA eran ~106 componentes con ese patrón.

Fix: recarga dura del documento (`window.location.reload()`) en el switch y en
el listener de `BroadcastChannel` que avisa a las otras pestañas. Alternativa
`key={orgId}` en el shell: mantiene la SPA y remonta el árbol, pero no cubre
estado fuera de React (SSE, timers, caches de módulo).

Aplica a cualquier cambio de identidad global: tenant, idioma con datos
servidos, impersonación. Ver [[impersonacion-superadmin-no-sirve-para-qa-de-ui-org-scoped]].
