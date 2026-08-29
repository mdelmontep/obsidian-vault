---
title: facturaia — poda del NOW a 2026-08-30
date: 2026-08-30
tags: [cliente, facturaia, historico]
---

Entradas retiradas del NOW del hub [[facturaia]] el 30-ago-2026, al cerrar el super test V2. Lo que seguía vivo de cada una quedó en el hub condensado a una línea; aquí está el detalle completo.

- 🟢 **Super test V2 CERRADO: 93 de 94, y el que falta está nombrado (30-ago, #2281→#2283, migs 768-772, ADR pendientes ninguno)** — de los 66 hallazgos del barrido, **dos tercios no eran hallazgos** (33 ya cerrados, 7 «no era», 4 descartados), y ~21 de los cierres reales fueron borrar endpoints huérfanos sin efecto visible. Los P0 que sí valían **no salieron del barrido** sino de aplicar la migración y bajar a producción: el objetivo de cobro líquido (770), los tipos de BD que mentían y el cuarto sitio que asentaba el bruto (772). **M1 sigue `parcial` a propósito**: `admin` son 185 ítems que exigen superadmin sobre 24 orgs, 9 de ellas clientes reales. Registro en `docs/qa/cierre/registro.jsonl` (94 filas). → [[el-candado-audita-la-clase-no-la-lista-que-alguien-escribio]] · [[ausencia-de-consumidor-no-es-ausencia-de-funcion]]
- 🟢 **La «salida A» del albarán, EN PROD (30-ago)** — cruzar antes de aprobar: migs 768-771 aplicadas y verificadas por catálogo, casación previa ejercitada en producción **con un par real** (2 pares, cantidades correctas, incluida la equivalencia `mm2`/`mm²`) y rastro devuelto. La migración que «no había parseado nunca Postgres» ya la parseó. → [[puntero-por-indice-a-un-array-jsonb-se-rompe-al-borrar]] · [[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]]
- 🟢 **Ticket 156 cerrado: manda la cabecera, no el cuadro de IVA (29-ago, #2274→#2280, migs 764-767, ADR-032)** — 40 albaranes valorados recolocados con copia forense, marcha atrás desde la bandeja, canario en el sweep, y `merge_proveedor` ya no borra albaranes, lotes ni tarifas. La proforma tampoco entra ya en recibidas (deducía el IVA dos veces), y lo que lo sostiene es la POSICIÓN de su viñeta en el PASO 0.0. **Queda solo la respuesta del cliente.** → [[quitar-el-flag-de-defecto-aceptado-sin-quitar-su-explicacion]]
- 🟢 **IA agéntica: `categorias` en `activo` en prod (26-ago, #2221→#2234, migs 755/761)** — **queda**: cobertura de lo que escribe solo (#2227) y 22 circulares de `_parts` (#2228). OCR sigue en shadow: es acumulación, no código. → [[facturaia-historico-detallado]] §26-ago · [[facturaia-prompt-continuacion-26-ago]] · [[un-gate-abierto-con-la-metrica-caducada-no-vuelve-a-cerrarse]] · [[una-linea-roja-que-un-toggle-de-informes-puede-levantar-no-es-una-linea-roja]]
- 🟢 **Las 22 llamadas al modelo, en prod (25-ago, #2185→#2192)** — **queda** el eval de `doc-extract` (pide corpus de extractos ficticios). → [[facturaia-historico-detallado]]
- 🟢 **OCR: arnés `eval:ocr` y webhook sin pérdidas, en prod (25-ago, #2180→#2183)** — **queda** el gap `multi-albaran-multipagina`. → [[facturaia-historico-detallado]]
- 🟢 **El cuerpo de un error, cerrado (#2131 + #2138, prod)** — el candado de 6 aserciones no ve el estado de un componente de cliente. → [[el-atajo-del-escaner-excluye-la-forma-que-nadie-penso-medir]]
- 🟢 **El 303 ya no deduce IVA que no existe (24-ago)** — cerrado. **3T vence 20-oct.**
- 🟢 **Unidad de obra desde el presupuesto, en prod** — queda el paso 3: editar la copia. → [[facturaia-historico-detallado]]
