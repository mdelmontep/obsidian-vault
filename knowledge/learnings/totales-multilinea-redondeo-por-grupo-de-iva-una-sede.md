---
title: totales multi-línea deben redondear la cuota por GRUPO de iva, no por línea, con una sola sede
date: 2026-07-13
source: facturaia auditoría Fable5 totales #869
tags: [fiscal, iva, redondeo, verifactu, arquitectura]
---

Al agregar totales de un documento con varias líneas, la cuota de IVA debe redondearse a 2 dec UNA vez por GRUPO de tipo (0/4/10/21…), no por línea. Sumar cuotas redondeadas por línea deriva ±1 céntimo por tipo respecto al XML VeriFACTU (que agrupa por (iva_pct, exención) y hace `round(Σ round(cuota_grupo))`). Ejemplo: 5×0,99€ @21% → por grupo `round(4,95·0,21)=1,04` (total 5,99); por línea `5×round(0,2079)=1,05` (total 6,00).

Segundo gotcha: si el cálculo vive en 3 sitios (UI, backend, worker XML) sin una sede única ni test que los ate, divergen en silencio. Fix: una función `calcularTotales` compartida (UI la consume, backend la persiste con `round2`, worker replica el criterio) + test de propiedad con N líneas aleatorias deterministas (PRNG sembrado) que asserte backend == réplica-XML EXACTO.

Distinto de [[numeric-precision-drift-bruto-neto-iva]] (bruto↔neto) y [[sembrar-base-desde-total-con-iva-pierde-centimo]] (seed desde total): aquí el eje es la AGREGACIÓN entre líneas. Aplica a cualquier app de facturación multi-línea + registro fiscal XML.

Recurrencia (#871, 2026-07-13): el `subtotal` NETO por línea persistido en `lineas_factura` es OTRO de esos sitios — el worker XML lo suma crudo por grupo y redondea una vez. `createDocument` (`buildLineasFactura`) lo persistía sin redondear (correcto) pero el editor de borrador (`PATCH /api/facturas/[id]`) lo redondeaba por línea (drift). Fix: exportar `subtotalLinea` y usarlo en ambos caminos. Regla: un campo con >1 camino de escritura → misma sede o diverge.
