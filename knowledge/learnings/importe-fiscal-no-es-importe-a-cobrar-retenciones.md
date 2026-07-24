---
title: importe fiscal ≠ importe a cobrar cuando hay retenciones (IRPF, garantía)
date: 2026-07-25
source: claude-code-session
tags: [facturacion, fiscal, conciliacion, sepa, postgres]
---

`facturas.total` guarda el importe FISCAL (`base + IVA`) porque es lo que firma VeriFactu y lo que declara el 303. Pero el PDF que recibe el cliente imprime `base + IVA − retención` (IRPF art. 99 LIRPF: el pagador retiene y lo ingresa él). **Son dos números distintos y el cliente transfiere el segundo.**

Caso real TuFacturaIA: base 1.000 + IVA 21% − IRPF 15% → PDF dice 1.060 €, BD dice 1.210 €, Δ150 €.

Todo lo que compara importes con el mundo exterior usa el número equivocado:
- **Conciliación bancaria**: 150 € ≫ tolerancia (10 €) → score 0, **0% de automatización** para todo profesional que factura a empresa. Silencioso: no hay error, simplemente nunca hay sugerencia.
- **Adeudo SEPA (pain.008)**: se cobra el bruto → **cobro indebido**, con exposición a R-transaction y al mandato.
- **Recordatorio de cobro**: reclama al cliente final una cifra que no debe.

Fix: **no tocar `total`** (rompe cadena VeriFactu/303/abonos). Añadir un `importe_cobrable` derivado (columna GENERATED STORED, ver [[columna-generada-stored-para-equivalente-derivado]]) y que lo consuman conciliación, SEPA y cobros. Ojo a las fórmulas: IRPF es sobre la **base**; la retención de garantía de obra es sobre el **total con IVA**. Y cuadrar el orden de redondeo con el que ya usa el 111, o los dos divergen al céntimo.

Detección: `grep` de quién lee `total` y clasificar en "fiscal" (correcto) vs "importe a cobrar" (bug). Relacionado: [[conciliacion-multi-señal-vs-importe-bruto-falsos-positivos]] · [[sembrar-base-desde-total-con-iva-pierde-centimo]].
