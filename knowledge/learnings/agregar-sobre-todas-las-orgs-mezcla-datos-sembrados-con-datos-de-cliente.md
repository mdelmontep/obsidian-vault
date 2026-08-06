---
title: agregar sobre todas las organizaciones mezcla datos sembrados con datos de cliente
date: 2026-08-06
source: claude-code-session
tags: [multi-tenant, medicion, sandbox, falso-positivo, facturaia]
---
Midiendo el margen (venta contra coste) de presupuestos de obra salieron cifras
imposibles: dos negativas y una con coste 0. Conclusión precipitada: "el cálculo
está mal", y se apagó la funcionalidad recién entregada.

Era falso. Al **partir por organización**, el reparto era: 59.220 líneas de una
org sandbox contra 9 de la org real. Los datos sembrados mandaban por volumen y
tapaban el resultado bueno. En las orgs reales el dato era exacto al céntimo
(margen 26,5% = incremento del 36% configurado).

Regla: **toda medición de negocio en un SaaS multi-tenant se parte por org y se
excluyen las `is_test` ANTES de concluir**. Un agregado global sobre todas las
orgs no mide nada: mide el seed.

Segundo error de la misma medición: la consulta ignoraba los flags de venta y
los descuentos, así que sobreestimaba el ingreso. Al comparar magnitudes de
negocio, replicar los MISMOS filtros que usa el motor, no un `sum()` a ojo.
