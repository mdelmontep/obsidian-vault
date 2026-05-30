---
title: stripe subscription.deleted handler debe resolver por sub.id no solo por metadata.kind
date: 2026-05-30
source: claude-code-session
tags: [stripe, webhook, saas]
---

Si una org tiene varias subs (e.g. `base_stripe_subscription_id` + `fiscal_stripe_subscription_id`), el handler `customer.subscription.deleted` NO puede ramificar solo por `metadata.kind`:

- Stripe Customer Portal emite `subscription.deleted` SIN garantizar metadata (Dashboard manual la pierde).
- Si solo procesas `kind === 'fiscal_addon'`, las cancelaciones del plan base pasan silenciosas (`skipped: 'kind_mismatch'`) y la org queda `billing_status='active'` con sub borrada — cliente sigue usando Pro gratis.

Pattern correcto: leer las dos columnas de binding, comparar `sub.id` contra cada una, ramificar. `metadata.kind` solo como hint para casos sin binding (ambas null + sub recién creada). Caso real TuFacturaIA: handler ignoraba P0 hasta audit cross-PR 2026-05-30 (PR #112). Ver [[bot-multi-accion-fallback-activo-silencia-routing]] (patrón análogo en bot WA).
