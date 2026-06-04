---
title: stripe sub con add-on: resolver item por price.id, nunca items[0]
date: 2026-06-05
source: claude-code-session
tags: [stripe, webhook, saas]
---
Una sub con plan base + add-on (empresa extra, quantity) tiene VARIOS items.
En `customer.subscription.updated` NO asumas `items[0]` = plan base:
- Resolver el item base por `getPlanFromPriceId(price.id)`; el add-on por
  `isEmpresaExtraPriceId(price.id)`. Stripe NO garantiza orden de items.
- Sincronizar `empresas_extra = addonItem.quantity` (0 si el item ya no está).
- Al comprar: subscription item con quantity en el MISMO ciclo que el base,
  `proration_behavior=always_invoice`. Update optimista local + webhook reconcilia.
Caso TuFacturaIA F3b (PR #144). Hermano de [[stripe-subscription-deleted-resolver-por-sub-id-no-por-kind]].
