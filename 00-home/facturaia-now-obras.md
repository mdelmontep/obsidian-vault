---
title: FacturaIA — NOW Obras
updated: 2026-09-22
tags: [facturaia, now, obras]
---

# NOW — Obras

Extraído del dashboard de [[facturaia]] el 22-sep-2026: el NOW tenía 59 frentes y 22 KB,
la mitad del arranque de cada sesión. Aquí viven los 6 de esta área, íntegros.

Vuelve al hub: [[facturaia]]

- 🔴 **Cabo del #1550: la recepción de albarán rotulaba «Material» en casi toda recepción real** — arreglado y con guard, pero **no sabemos qué usuarios validaron albaranes a ciegas** (el modal traía el catálogo paginado: 50 de 11.595). Preguntar a IET antes de cerrarlo. → [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]]
- 🟠 **Impersonando a un cliente, las rutas `/obras/*` dan 404 (07-ago)** — las 15, con el sidebar enlazándolas y `GET /api/obras/settings` devolviendo la org correcta: sidebar y API resuelven la org impersonada, la página no. Como usuario real cargan bien, así que es del modo Vista cliente. **Hoy no puedes ver el módulo Obras de IET desde tu panel**, que es justo el cliente que lo usa. Sin issue abierto. → [[impersonacion-superadmin-no-sirve-para-qa-de-ui-org-scoped]]
- 🔴 **«Actualizar precios» multiplica el precio al cliente si al material le falta el descuento, y no lo dice (02-ago)** — medido en un presupuesto real: total de 1.583 € a 5.999 € (**×3,8**). La aritmética es correcta y no es bug de la mig 626; el daño es que lo aplica **en masa, sobre un presupuesto ya hecho y en silencio**. El modal enseña el delta pero no que N partidas no tienen descuento — en el catálogo de Natalia, la mayoría. Arreglo propuesto (necesita mig, no hecho): contador `lineas_sin_descuento` en la RPC + aviso. **Decisión suya.** → [[facturaia-historico-eventos]]
- 🟠 **Unidad de obra desde el presupuesto: queda el paso 3, editar la copia.** → [[facturaia-historico-snapshot-2026-08-30]]
- 🟠 **Dos issues abiertos por el bloque de obras (01-ago)** — `ocr-001`: el desglose de una factura larga da **entre 2 y 41 líneas según la pasada** sobre el mismo PDF, sin truncado de tokens; toca 303, libro de IVA y stock, y es preexistente. `ui-001`: el `autoFocus` de los modales nunca llega al campo (`<Modal>` enfoca el diálogo en un efecto posterior); afecta a todo el repo.

- 🔴 **Dos defectos de datos, medidos en prod (03-ago, `issues/obras-097` y `-098`)** — (1) **121 líneas con snapshot 0,00 € y catálogo > 0**; el modal ya avisa y no se recalcula al copiar (traería el inflado ×3,8). Queda decidir si se barren. (2) **3.120 pares (presupuesto, material) con dos precios** para la misma referencia, p95 ×22,6: vienen de la carga de WAPI, no de nuestro motor. **Bloqueado en Natalia**: si en su ERP es intencionado, no hay bug.
