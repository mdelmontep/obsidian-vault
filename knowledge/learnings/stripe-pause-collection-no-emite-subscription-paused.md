---
title: stripe — pausar el cobro no emite customer.subscription.paused
date: 2026-08-15
source: claude-code-session
tags: [stripe, webhooks, billing, facturaia]
---

Stripe tiene dos "pausas" y solo una emite `customer.subscription.paused`:

- `status = 'paused'` — sí lo emite. Solo pasa al acabar un trial sin método de
  pago (`trial_settings.end_behavior.missing_payment_method = 'pause'`). Raro.
- `pause_collection != null` — **no lo emite**. La suscripción sigue `active` y
  llega un `customer.subscription.updated`. Es la pausa que se usa de verdad
  desde el dashboard.

La doc lo dice literal (`stripe docs api customer.subscription.paused`): «Only
applies when subscriptions enter status=paused, not when payment collection is
paused». Enganchar la suspensión al evento `paused` deja al cliente con acceso
completo mientras no se le cobra.

Para distinguir "acaban de pausar" de un `updated` cualquiera, mirar
`event.data.previous_attributes` (presencia de la clave `pause_collection`), NO
comparar contra el estado en base: comparando, cualquier `updated` posterior
vuelve a disparar el efecto, y en el sentido de reanudar eso reactiva cuentas
suspendidas por otra cosa.

Ver [[00-home/facturaia]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]
