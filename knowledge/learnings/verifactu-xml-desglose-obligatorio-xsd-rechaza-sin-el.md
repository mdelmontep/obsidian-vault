---
title: Verifactu XML exige bloque Desglose o AEAT rechaza por XSD
date: 2026-05-18
source: claude-code-session
tags: [verifactu, aeat, xml, fiscal, gotcha]
---

Orden HAC/1177/2024 + XSD `tikeV1.0` exigen `<Desglose>` con 1..12 `<DetalleDesglose>`. Sin él AEAT rechaza por XSD. Entorno `pre` puede no validar estricto → bug invisible hasta cutover prod.

Catálogos AEAT literales: L8A ClaveRegimen `01..20`, L9 `S1/S2/N1/N2`, L10 `E1..E6`. `CalificacionOperacion` XOR `OperacionExenta`. Si exenta → omitir `TipoImpositivo` + `CuotaRepercutida`. `BaseImponibleOimporteNoSujeto` siempre obligatorio.

Agrupar líneas por `(iva_pct, exencion_codigo)` para no exceder 12.

Ver [[verifactu-huella-encadenada-race-condition-sin-advisory-lock]]
