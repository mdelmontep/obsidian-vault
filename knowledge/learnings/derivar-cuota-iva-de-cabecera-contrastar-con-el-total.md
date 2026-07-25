---
title: derivar la cuota de IVA de una cabecera exige contrastarla con el total, no fiarse del iva_pct
date: 2026-07-25
source: claude-code-session
tags: [fiscal, aeat, ocr]
---

412 de 426 recibidas aprobadas no tenían `lineas_factura` y el calculador del 303 las saltaba con `continue`: 136.503,94 € de base sin aportar IVA soportado, en 4 orgs. El fix es derivar UNA línea de la cabecera, pero medido: **74 de 238 cabeceras no cuadran consigo mismas** (`base + IVA − retención ≠ total`), desviación hasta 1.664,30 €. Derivar por `iva_pct` habría declarado una cuota falsa en 1 de cada 3.

- Cabecera que cuadra → cuota por `iva_pct`. No cuadra → `total − base + retención` (los dos importes **duros**). Implausible (negativa o > 27 % de la base: 21 % general + 5,2 % de recargo) → base sí, **cuota 0**, y avisar. Perder una deducción es recuperable; declarar una cuota falsa no.
- Fundamento AEAT: el IVA deducible de **operaciones interiores corrientes** (casillas 700/701 del 303) **no se desglosa por tipos**. O sea que colapsar tipos no rompe el modelo; lo que importa es que la cuota TOTAL sea correcta. Verificarlo cambió el diseño.
- Declarar lo asumido con severidad graduada (`info` si cuadra, `atención` si se derivó del total) en vez de un `info` silencioso para todo: quien firma el modelo tiene derecho a saberlo.

Nació en TuFacturaIA, ver [[facturaia]].
