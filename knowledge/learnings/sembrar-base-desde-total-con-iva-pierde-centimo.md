---
title: "sembrar base desde un total con iva incluido pierde un céntimo (≈mitad de importes redondos)"
date: 2026-06-16
source: facturaia 086 conciliación crear-doc-desde-movimiento
tags: [facturaia, iva, redondeo, conciliacion]
---

Sembrar un documento desde un importe bruto IVA-incluido: `base = round2(bruto/(1+iva))`. Al recomponer `total = round2(base*(1+iva))` NO se recupera el bruto para ~la mitad de importes redondos (100€→99,99; 10€→9,99; 50€ sí cuadra). El céntimo perdido deja la conciliación con un residual.

**Fix**: si el precio NO se muestra al usuario (modal total+IVA), guardar la base SIN redondear → `round2(baseExacta*(1+iva)) == bruto` SIEMPRE (matemáticamente exacto). Si el precio sí es visible/editable, déjalo limpio a 2 decimales y que la tolerancia de conciliación absorba el céntimo.

**Corolario (el bug real)**: la tolerancia de "conciliado" debe ser fuente ÚNICA entre BD y UI. En FacturaIA el drawer usaba `0.005` hardcoded mientras la lista (`TOL_CONCILIACION`=0,01) y la BD (`recompute_factura_estado`: `GREATEST(0,10, total*0.005)`) ya perdonaban el céntimo → botones fantasma "Registrar resto (0,01)". Exporta la constante y reúsala; no inventes umbrales por capa.
