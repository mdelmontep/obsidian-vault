---
title: ADR-042 — `base` es la base imponible NETA en todos los tipos; presupuestos conservan el descuento en cabecera y facturas lo reparten en líneas
date: 2026-07-27
status: accepted
tags: [adr, facturaia, fiscal, verifactu]
---

## Contexto

`facturas.base` guardaba la base NETA (decisión H1: descuento global repartido en las líneas, `descuento_global_pct = 0` en cabecera) pero `presupuestos.base` guardaba la BRUTA con el total ya descontado. Toda derivación `total − base` daba una cuota falsa, negativa con descuentos ≳17,4 %, y la conversión a factura propagaba el descuadre a un documento fiscal.

## Opciones consideradas

- **A — Paridad total con facturas**: repartir también en presupuestos y poner `descuento_global_pct = 0`. Un solo modelo, pero **destruye el dato**: el editor y el PDF pierden el "Descuento 20 %" y solo se recupera infiriéndolo de Σneto/Σbruto.
- **B — `base` NETA en todos los tipos, presupuestos conservan líneas brutas + el % en cabecera**. Invariante cumplido y desglose intacto; obliga a recrear las columnas generadas de la mig 559, que reconstruían la neta desde la bruta.
- **C — Arreglar solo los ~6 sitios que derivan `total − base`**. Barato y sin tocar datos, pero deja la cabecera incoherente consigo misma y el siguiente consumidor vuelve a caer.

## Decisión

**B**. `base` significa lo mismo en las dos tablas: base imponible. Es lo que dice LIVA art. 78.Tres.2 y el desglose de Facturae/EN-16931 (bruto → descuento → base imponible → cuota → total), así que el estándar ya resuelve la aparente contradicción de "líneas brutas con base neta".

La asimetría que queda es deliberada: **facturas reparten el descuento en las líneas porque VeriFACTU serializa el desglose por tipo de IVA leyendo `lineas_factura.subtotal`**. Un presupuesto no se declara a AEAT, así que conserva el dato. La conversión presupuesto→factura es el punto exacto donde se cambia de modelo (mig 576).

## Consecuencias

- `base + cuota = total` es invariante para todos los tipos y se comprueba en la composición, abortando antes del INSERT.
- Ningún INSERT puede volver a leer la base bruta: se lee siempre de `baseReportada`.
- Se renuncia a "un único modelo para todo": quien toque la conversión debe entender que ahí cambia la representación.

Migs 575/576 · PRs #1250/#1252 · Ver [[base-persistida-debe-ser-la-imponible-o-total-menos-base-miente]] · [[facturaia]]
