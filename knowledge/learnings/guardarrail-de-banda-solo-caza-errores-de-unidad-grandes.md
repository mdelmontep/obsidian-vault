---
title: un guardarraíl de banda solo caza errores de unidad con factor grande
date: 2026-09-27
source: facturaia
tags: [stock, unidades, validacion]
---
Patrón: coste = cantidad × precio, con la cantidad en una unidad (cajas del albarán) y el precio en otra (ostras de la factura).
Gotcha: el guardarraíl «fuera de 1/3–3× la mediana» paró el caso real porque el factor era 24. Con un factor 2 (media caja, kg frente a caja) el coste falso entra sin aviso, y los tests verdes solo tienen casos en la misma unidad.
Fix: comprobar que las dos cifras están en la misma unidad antes de multiplicar (unidad del papel frente a la de stock). Si no se puede convertir, NO calcular y dejar traza con motivo. Nunca ensanchar la banda.
Caso: facturaia mig 949 `stock_revalorizar_compra_albaran`, issue #3013 (factura de 48 ostras a 1,90 € casada con 2 cajas de 24).
Relacionado: [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]]
