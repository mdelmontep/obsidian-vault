---
title: collector de alertas admin debe emitir dismissKey de 2 partes
date: 2026-06-12
source: claude-code-session
tags: [facturaia, admin, alerts, testing]
---
El dismiss de `/admin/alerts` construye su Set como `${alert_type}:${org_id}`
(2 partes, `src/app/api/admin/alerts/route.ts`). Un collector nuevo que emita
un dismissKey con más partes (`tipo:org:key`) nunca casa → la alerta reaparece
para siempre tras dismissar.

Fix/patrón: la granularidad extra va embebida en el `alert_type`
(`quota_warn_<key>`), nunca como sufijo del dismissKey.

Gotcha de testing: el test del collector puede pasar con un mock que inyecta
el formato inventado — los contratos implícitos entre módulos hay que
verificarlos contra el código real del otro lado, no contra el mock.
Caso: PR #213 TuFacturaIA, dismiss roto de fábrica.
