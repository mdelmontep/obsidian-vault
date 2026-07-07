---
title: un Coupon de Stripe no es tecleable por el cliente, hace falta un PromotionCode aparte
date: 2026-07-07
source: claude-code-session
tags: [stripe, billing, coupons]
---

Crear un `Coupon` vía API (`POST /v1/coupons`) NO da al cliente nada que pueda
escribir en el campo de código de Checkout (`allow_promotion_codes:true`). Hay
que crear además un `PromotionCode` (`POST /v1/promotion_codes`, `{coupon, code}`)
— el `code` es el texto humano-legible, el Coupon es solo la regla de descuento.
Vía Dashboard esto se hace junto en un solo flujo, así que el gap solo aparece
si se automatiza por API cruda.

Dos gotchas más de la misma familia:
- `discounts[]` y `allow_promotion_codes:true` son **mutuamente excluyentes**
  en una Checkout Session — Stripe rechaza si van los dos.
- Para aplicar un descuento a una **suscripción ya existente** (retención,
  no alta nueva) es `POST /subscriptions/{id}` con `discounts[0][coupon]`,
  no la Checkout Session — API distinta, y hay que leer `sub.discount` antes
  para no duplicar si ya tiene uno (idempotencia).
- "Bloquear" un cupón propio en tu tabla NO desactiva el PromotionCode en
  Stripe — si el cliente lo aplica él mismo (código manual), hay que togglear
  `active` en el PromotionCode real o el bloqueo es una mentira en el panel.
