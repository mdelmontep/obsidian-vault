---
title: Stripe Tax aplica reverse charge mirando el NIF del cliente, no si TÚ estás en el ROI
date: 2026-08-14
source: claude-code-session
tags: [stripe, fiscal, iva, espana, vies]
---

Stripe Tax decide la inversión del sujeto pasivo por la presencia de un NIF-IVA válido del
**cliente** y las jurisdicciones implicadas. No comprueba que el **emisor** esté dado de
alta como operador intracomunitario. Resultado: puede dejar una venta B2B europea a 0 % de
IVA que a ti no te corresponde facturar así.

Comprobar el NIF propio en VIES antes del primer cobro europeo, con un GET simple:

    curl "https://ec.europa.eu/taxation_customs/vies/rest-api/ms/ES/vat/<NIF sin ES>"

(`POST` responde «Request method not supported»). `isValid: false` significa que no consta
en el ROI: hace falta el modelo 036, casilla 582, o revisar si hay errata en el NIF.

Caso real: AgentesiaLab S.L., `B27602085` → `isValid: false` el 14-ago-2026, con el
producto ya listo para cobrar y la UI preparada para rotular reverse charge.

El tipo de tax ID que se da de alta en Stripe también depende de esto: sin ROI va
`es_cif`, no `eu_vat`. Ver [[stripe-sin-account-tax-ids-la-factura-sale-sin-nif-del-emisor]]
