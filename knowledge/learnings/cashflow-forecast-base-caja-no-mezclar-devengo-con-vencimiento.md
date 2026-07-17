---
title: forecast de tesorería = base caja pura; mezclar devengo con vencimiento duplica la factura
date: 2026-07-17
source: claude-code-session
tags: [cashflow, tesoreria, correctness, facturaia]
---
Una previsión de tesorería es BASE CAJA (mide cuándo se mueve el dinero), no devengo (Holded/AFP/CFI: "la fecha relevante es la de vencimiento; accrual ≠ caja"). Cada factura cuenta UNA sola vez:
- cobrada/pagada → mes de su fecha real de cobro/pago (caja ya movida, ya dentro del saldo de hoy).
- pendiente/enviada/vencida → mes de su vencimiento (ajustado por payment-pattern en emitidas).
- vencido impagado → arrastrar al mes actual (caja esperada inminente) y SÍ cuenta en los 90 días.

Anti-patrón que teníamos: meses reales por devengo (fecha de emisión) + meses futuros por caja (vto). Una pendiente con emisión pasada y vto futuro caía en AMBOS → saldo a 90 días duplicado (-4499 en vez de -2249). Es un fallo distinto al del ancla (ver [[cashflow-saldo-actual-mas-serie-historica-doble-conteo]]): aquí la MISMA factura se suma dos veces por dos criterios temporales incompatibles.

Saldo correcto = caja hoy + Σ caja esperada del horizonte. Ancla en HOY (no sembrar la caja de hoy N meses atrás). Al tocar el núcleo, grep TODOS los consumidores (web, dashboard, API v1/MCP, voz, cron alertas). Caso FacturaIA PR #986. Ver [[facturaia]].
