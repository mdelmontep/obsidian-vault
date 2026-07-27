---
title: la base persistida debe ser la imponible, o toda derivación `total − base` miente
date: 2026-07-27
source: claude-code-session
tags: [fiscal, modelo-datos, facturacion, verifactu]
---

Los presupuestos guardaban la base **BRUTA** (pre descuento global) con el `total` ya descontado. Media docena de consumidores derivan la cuota como `total − base` → IVA falso, y **negativo** en cuanto el descuento pasa de ~17,4 % al 21 %. Caso real: base 3.850 / total 3.726,80 → el listado pintaba **−123,20 €** de IVA.

- **LIVA art. 78.Tres.2**: los descuentos previos o simultáneos NO forman parte de la base imponible. Una columna `base` en un documento fiscal ES la imponible. El bruto es otro concepto y tiene su propio nombre en los estándares (`TotalGrossAmount` de Facturae 3.2, `LineExtensionAmount` de EN-16931).
- No hay que elegir entre invariante y dato: **líneas BRUTAS + `descuento_global_pct` en cabecera + `base` NETA** guarda el desglose entero y cuadra. Eso es exactamente el estándar (bruto → descuento → base imponible → cuota → total).
- Codificar `base + cuota = total` como invariante que **aborta antes del INSERT**, para todos los tipos de documento. Si la cabecera y las líneas divergen, que el documento no nazca.
- Lo caro no era el número feo en pantalla: al convertir a factura, el desglose por tipo de IVA —que VeriFACTU serializa desde `lineas_factura.subtotal`— declaraba base y cuota **mayores que el total de su propia cabecera**. AEAT valida eso con tolerancia de ±0,01.

Complementa [[derivar-cuota-iva-de-cabecera-contrastar-con-el-total]] (aquel es cómo derivar al LEER; este, qué persistir). Nació en TuFacturaIA, ver [[facturaia]] · [[ADR-042-base-imponible-neta-en-todos-los-tipos]].
