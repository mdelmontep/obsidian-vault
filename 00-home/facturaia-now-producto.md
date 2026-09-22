---
title: FacturaIA — NOW Producto y UI
updated: 2026-09-22
tags: [facturaia, now, producto]
---

# NOW — Producto y UI

Extraído del dashboard de [[facturaia]] el 22-sep-2026: el NOW tenía 59 frentes y 22 KB,
la mitad del arranque de cada sesión. Aquí viven los 13 de esta área, íntegros.

Vuelve al hub: [[facturaia]]

- 🔴 **El trailer `Ticket-feedback:` cierra y avisa al cliente ANTES de que el arreglo esté vivo — arreglo listo sin mergear (#2773)** — pasó con el 181: cerrado y correo enviado 2 s tras el merge, con la migración sin aplicar. El merge pasa a SELLAR (`cierre_diferido_*`) y lo consuma el vigía con dos condiciones (ventana cerrada **y** proceso arrancado después del merge). **Bloqueado por el vigía**: sin schedule, sella y nadie consuma. **Tuyo**: elegir entre provisionar las dos variables en Dokploy (#2530) o una RPC `SECURITY DEFINER` que lea `schema_migrations` desde la app. #2774 (tipos + fuera los shims) es mergeable ya.
- 🟠 **Cabos del 26-ago, todo lo demás en prod** — agéntica `categorias`: cobertura de lo que escribe solo (**#2227**) y 22 circulares de `_parts` (**#2228**), OCR en shadow · albaranes: falta el smoke que ejerza el guard del doble conteo · PSD2 sigue sin integrar por coste, y es decisión, no avería. → [[facturaia-historico-snapshot-2026-08-30]]

- 🔴 **`brand-tokens.ts` deriva la marca personalizada por el SUELO (28-ago, sin issue)** — una org con marca propia recibe 10-13 Lc MENOS que la de fábrica, sin aviso. Preexistente; no entra en #2272.

- 🟠 **Las filas de `/admin/feedback` no se pueden abrir con teclado ni por rol, sin issue (10-sep)** — `<tr>` con `onClick` sin `role`/`tabIndex`: fuera del árbol de accesibilidad, sin cobertura E2E, y responder hubo que hacerlo por el `fetch` del propio panel. → [[una-fila-clicable-sin-rol-no-la-abre-ni-un-lector-ni-un-agente]]
  Y el mismo ticket sigue en `resuelto` (`manual`, 8-sep) con el hilo vivo el 9 y el 10 y una petición recién salida: el estado y la conversación van por libre.
- 🔴 **Dos cabos del ticket 159, sin issue (28-ago)** — (1) `/admin/orgs` en «Cargando…» es **hidratación, no la API**: decidir si es defecto o artefacto de QA → [[una-vista-en-cargando-con-su-api-en-200-esta-sin-hidratar]]; (2) el OCR **no aprende línea→producto** y ese cliente arrastra 17 recibidas sin aprobar.

- 🟠 **Espejo de facturación en prod, sin verificar por otros ojos (#2119, mig 751)** — **queda** los cinco tracks de lectura de `PROMPT-continuacion-23-ago.md`. → [[un-trinquete-por-fichero-absuelve-al-que-ya-importa-el-helper]]
- 🟠 **#1776**: se reduce a `preferred_locales:['es']` y cierra con el encendido de #1778 (0 customers reales).
- 🟠 **#1778: PR 1-3 en prod, flag `FACTURAS_SUSCRIPCION_PROPIAS` apagada (20-ago)** — **queda**: PR 4 (encender + smoke), PR 5 (devoluciones/disputas) y modelar N2 (#1994). Sin urgencia: 1 cliente live y es ES. → [[facturaia-historico-detallado]] · [[codigo-de-exencion-no-expresa-una-operacion-no-sujeta]]
- 🔴 **En una org suspendida, Ajustes → Empresa guarda la mitad y descarta la otra sin avisar (#2100, smoke del 22-ago)** — el `settings` persiste (endpoint de servidor, bypasea RLS); las columnas de `organizations` chocan con `is_billing_readonly` (mig 323) y devuelven **204 = éxito** con cero filas. Mismo clic: `epigrafe` guardado, `direccion` perdida. **Decidir**: si no puede editar su ficha, tampoco su `settings` por la puerta de al lado. → [[update-que-afecta-cero-filas-no-devuelve-error-en-postgrest]]
- 🟠 **Skeletons de carga: arreglados y SIN COMMITEAR desde el 04-ago** — `<SkeletonTable>` en 18 ficheros, gates verdes. **Tuyo: revisar y commitear.** → [[nombre-de-clase-css-modules-como-string-global-es-selector-muerto-sin-error]]
- 🟠 **Dígitos invertidos al teclear: arreglado en prod (01-ago, #1446). Queda el hueco vecino** — si la app reescribe el valor de un campo enfocado sigue el mismo camino; anterior a #1443 y NO arreglado. Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]]
- 🟡 **`perf-001` — CLS: queda el banner de billing (#1258, #1305)** — **decisión de diseño**: `.billing-banner` empuja 36 px tras el primer render → resolver en servidor o reservarle hueco. Residual: `useOrgRole` da `role: null` mientras carga y el rail mete 7 secciones después; el hook ya expone `loaded` y nadie lo mira. → [[facturaia-historico-snapshot-2026-08-01]] · [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]]
- 🔴 **Cobro con tarjeta (#1704): el webhook de Connect funciona en prod; ahora bloquea la KYC (20-ago)** — endpoint LIVE creado, declarado en el compose y probado con la sonda de firma. **Tuyo**: completar la KYC de plataforma en `acct_1Td5cc`. Runbook → `docs/architecture/cobro-stripe-connect-runbook.md`
