---
title: el gating de visibilidad/acceso de un módulo duplicado por página deriva inconsistente — centralízalo
date: 2026-06-05
source: claude-code-session
tags: [arquitectura, gating, feature-flags, admin]
---
Caso real (TuFacturaIA, control de disponibilidad de módulos oculto/proximamente/
beta/activo): el gating server estaba copiado en cada página de módulo y había
DIVERGIDO — `/inventario` miraba disponibilidad + add-on, pero `/cashflow` y
`/fiscal` solo `orgHasFeature` (ignoraban disponibilidad) → un módulo en
`proximamente` era accesible por URL. Síntoma típico de regla de acceso repetida.

Fix: un helper único (`getModuleAccess(orgId, featureId): 'allow'|'upsell'|'redirect'`)
como single source of truth de la matriz, y todas las páginas lo llaman. Si una
regla de acceso vive en >1 sitio, asume que ya divergió.

Trampa del flag global "beta": debe respetarse en las CUATRO capas — página
(`getModuleAccess`), UI embebida (`moduleEnabled`, no `hasFeature`), **endpoint**
(`checkFeatureGate`) y **tools del copiloto** (`registry.ts`, otra superficie de la
feature). Olvidar una rompe el módulo en beta de forma SILENCIOSA: beta activaba
UI+página pero `/api/stock/*` daba 403 (oculto por `if(!res.ok) return` en el
`useEffect`); y el copiloto usaba `orgHasFeature` crudo → daría 403 en beta. Fix:
helper boolean único `orgCanUseFeature(orgId,featureId)=disponibilidad==='beta'||
orgHasFeature` compartido por endpoint + copiloto (+ `moduleEnabled` espeja en UI).
Cobertura: un smoke con el add-on DADO no valida beta puro — prueba el flag real.

Update 2026-06-10 (audit 349): apareció una 5ª capa olvidada — `/api/fiscal/*`
sin `requireFeature` (cualquier sesión llamaba al cálculo sin el módulo). Y el
smoke del 403 es IMPOSIBLE con cuenta superadmin: `withApiAuth` bypasea el gate
→ hace falta cuenta E2E sin `is_superadmin`.

Patrón hermano (vista admin): cuando el superadmin debe VER todo pero también
previsualizar como cliente, no cambies el default — añade un toggle
`effectiveIsAdmin = isAdmin && !previewAsCustomer` (solo presentación, localStorage;
permisos reales intactos, siempre hay forma de volver). Relacionado:
[[role-gate-endpoint-debe-contemplar-superadmin]].

Update 2026-07-11 (cuadres 390): trampa al ENLAZAR entre páginas con familias de
gating distintas. `getModuleAccess` devuelve `redirect` para 'proximamente' a
no-superadmin, pero las páginas de DETALLE (`/fiscal/{ej}/{modelo}/{periodo}`)
gatean con `orgHasFeature` y SÍ renderizan. Resultado: un enlace desde una página
que renderiza (detalle) al hub `/fiscal/{ej}` (getModuleAccess) rebota a `/` justo
para los usuarios que ven el detalle → CTA muerto silencioso. Regla: antes de
enlazar entre páginas, comprueba que comparten familia de gating; si no, el destino
puede botar. Fix del 390 ("Resolver aquí"): enlazar al detalle del 303 (misma
familia orgHasFeature), no al hub. [[componentes-que-duplican-feature-check-se-desincronizan-del-provider]]
