---
title: "stripe: resolver el item de una suscripción por price, nunca por índice items.data[0]"
date: 2026-07-07
source: claude-code-session
tags: [stripe, billing, suscripciones, add-ons, gotcha]
---

Una suscripción Stripe con plan base + add-ons (p.ej. "empresa extra") tiene varios `items.data`, y **Stripe NO garantiza el orden** del array. Coger `sub.items.data[0]` a ciegas para "el item del plan base" puede pillar el add-on → al hacer `subscriptions.update items[0][price]=<nuevo plan>` sobrescribes el price del ADD-ON y dejas el plan base sin cambiar. Facturación corrupta, silenciosa.

Fix: resolver por price siempre —
`sub.items.data.find(it => it.price?.id && esPriceDelPlanBase(it.price.id))`.
En FacturaIA se extrajo a `findBasePlanItem(items, isBasePrice)` (helper puro, testeable sin cache). Bug real: `change-plan` era el único que usaba `[0]` mientras empresa-extra y el reconciliador del webhook ya resolvían por price (PR #777).

Regla general: cualquier lectura de "el item X" de una sub multi-item = por price/lookup, nunca por posición.

El add-on se sincroniza por su propio item: `empresas_extra = addonItem.quantity` (0 si el item ya no está). Al comprarlo, subscription item con quantity en el MISMO ciclo que el base + `proration_behavior=always_invoice`; update optimista local + webhook reconcilia (caso F3b, PR #144). Hermano de [[stripe-subscription-deleted-resolver-por-sub-id-no-por-kind]].
