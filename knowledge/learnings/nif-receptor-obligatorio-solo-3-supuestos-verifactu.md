---
title: nif del receptor obligatorio solo en 3 supuestos; consumidor final no lo necesita ni con verifactu
date: 2026-06-24
source: claude-code-session
tags: [facturaia, fiscal, verifactu, facturacion]
---

RD 1619/2012 art 6.1.d: el NIF del **destinatario** en factura ordinaria es obligatorio SOLO en 3 supuestos tasados:
1. entrega intracomunitaria exenta (art 25 LIVA),
2. destinatario que es sujeto pasivo (inversión SP),
3. operaciones en TAI con emisor establecido (interpretado para destinatario empresario/profesional).

Un **consumidor final/particular** no encaja en ninguno → su NIF NO es obligatorio.

**Verifactu (RD 1007/2023) NO añade esa obligación.** Factura ordinaria a consumidor final sin NIF es válida y registrable: clave **F2** (sin identificación del destinatario), `IDDestinatario` omitido, nombre "VENTAS A CONSUMIDOR FINAL".

Gotcha: exigir NIF "porque la org tiene Verifactu activo" es MÁS restrictivo que la ley y rechaza facturas legales. No hace falta forzar factura simplificada para B2C; la ordinaria sin NIF (F2) vale.

Fuentes: [BOE RD 1619/2012 art 6](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696) · [AEAT registro Verifactu](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/cuestiones-generales/contenido-registro-facturacion-alta_.html)
