---
title: migrar precios de un erp: congelar el neto con la aritmética del origen, no recalcular
date: 2026-07-21
source: claude-code-session
tags: [migracion, erp, precision, facturaia]
---
Al migrar presupuestos/facturas de un ERP viejo a uno nuevo, NO recalcules los precios con el
motor del destino (márgenes/descuentos/proveedor más barato del nuevo sistema) — darán números
distintos y el cliente los verá "mal". Reproduce las fórmulas del ORIGEN (incluidos sus redondeos
raros: p.ej. wapi redondea el % de descuento a 2 dec vía un param `decimal(10,2)`, y el unitario a
4 dec, antes de ×unidades) y **congela el neto ya calculado por línea**, con los descuentos del
destino a 0. Así el total es idéntico al céntimo por construcción.

Prueba de paridad = correr el motor REAL del destino sobre los datos importados y compararlo
contra el total autoritativo del origen (su propio stored proc), no "a ojo".
Huecos irreducibles del destino (p.ej. no admite líneas/cantidades negativas = las "bajas" del
origen) → son gap de producto a cubrir en el modelo, no a maquillar. Ver
[[sqlserver-cast-money-varchar-pierde-decimales]].
