---
title: payment link con importe congelado en su creación — revalidar el pendiente al conciliar, no confiar en el importe fijado
date: 2026-07-05
source: claude-code-session
tags: [stripe, cobro, conciliacion, fintech]
---

Un Stripe Payment Link (o cualquier enlace de cobro) fija su `unit_amount` en el
momento de crearse (típicamente `total - Σ pagos ya conciliados`). Si entre esa
creación y la confirmación async del pago (webhook) entra un cobro parcial por otra
vía (banco conciliado, otro canal), el pendiente real baja pero el link sigue
cobrando el importe antiguo (mayor) → el cliente paga de más y el webhook, si solo
hace un flip binario a "cobrada", no lo detecta.

Fix: al conciliar (webhook), recalcular el pendiente actual con la misma fórmula
que al crear el link y compararlo contra `session.amount_total`. Si no coincide, no
bloquear la marca de cobrada (el dinero ya se cobró de verdad) — dejar constancia en
un campo de observabilidad (`last_error` o similar) para revisión manual del
sobrecobro. Bloquear sería peor: dejaría un cobro real sin reflejar en el estado de
la factura.

Aplica a cualquier flujo "genera importe fijo ahora → confirma en otro momento":
payment links, facturas Stripe, links de pago genéricos con TTL.
