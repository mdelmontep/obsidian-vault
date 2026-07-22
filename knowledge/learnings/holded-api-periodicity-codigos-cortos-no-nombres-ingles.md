---
title: Holded API v2 (recurring-invoices) — periodicity usa códigos de una/dos letras, no monthly/yearly
date: 2026-07-22
source: claude-code-session
tags: [facturaia, holded, integraciones, api-externa]
---
El campo `periodicity` del recurso `recurring-invoices` de Holded v2 NO usa nombres en inglés (`monthly`/`quarterly`/`yearly`) como cabría asumir por analogía con otras APIs de facturación — usa códigos cortos: `d`=daily, `w`=weekly, `bw`=biweekly, `m`=monthly, `bm`=bimonthly, `q`=quarterly, `ba`=half-yearly, `a`=yearly. Confirmado en doc oficial (`holded.com/developers/api-reference/recurring-invoices/create-a-recurring-invoice`) y contra datos reales (129 recurring-invoices de una cuenta real: 94 `m` + 35 `a`, ningún `monthly` en crudo).

Un mapeo escrito a ciegas contra los nombres largos falla el 100% de las filas sin ningún error visible (cae al branch "cadencia no soportada"), no un bug ruidoso. Antes de mapear un enum de una API externa que no se ha tocado antes, volcar el payload real (`payload::jsonb` o log crudo) y mirar el valor tal cual llega, no fiarse de lo que "sonaría lógico" por el nombre del campo.
