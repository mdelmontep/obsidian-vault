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

Trampa del flag global "beta/lanzamiento": un estado de disponibilidad global
(visible+usable sin add-on) activa el sidebar y el gating de la página propia, pero
NO las **integraciones embebidas del módulo en OTRAS páginas** si esas usan
`hasFeature(id)` (que el flag global no toca). Caso real: en beta `/inventario` se
veía pero la sección de líneas de stock en `/ingesta` (gateada por `hasFeature('stock')`)
no aparecía. Fix: helper `moduleEnabled(id) = disponibilidad==='beta' || hasFeature(id)`
y usarlo en los gating de UI que deciden mostrar/usar un módulo (no en sub-features).

Patrón hermano (vista admin): cuando el superadmin debe VER todo pero también
previsualizar como cliente, no cambies el default — añade un toggle
`effectiveIsAdmin = isAdmin && !previewAsCustomer` (solo presentación, localStorage;
permisos reales intactos, siempre hay forma de volver). Relacionado:
[[role-gate-endpoint-debe-contemplar-superadmin]].
