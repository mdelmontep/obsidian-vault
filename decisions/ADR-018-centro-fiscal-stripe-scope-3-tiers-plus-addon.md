---
title: ADR-018 — Centro Fiscal IA Stripe scope = 3 tiers FacturaIA + add-on fiscal, no solo add-on
date: 2026-05-22
status: accepted
tags: [adr, facturaia, fiscal, stripe, billing]
---

## Contexto
Tabla `plans` existe en Supabase (Starter 12€/mes / Pro 23€ / Enterprise 49€) pero ningún plan está conectado a Stripe — actualmente los clientes están en `organizations.plan` pero NADIE paga. Centro Fiscal IA add-on 14,90€ ya tiene webhook + endpoints + columnas Stripe en organizations.

## Opciones consideradas
- **A — Solo conectar add-on fiscal a Stripe**: 15 min trabajo. Quirúrgico. Plans base siguen gratis de facto hasta otro día.
- **B — Conectar 3 tiers + add-on fiscal**: 4-6h dev (mig 151 + endpoints checkout/portal + branches webhook + UI /settings?tab=plan). Más trabajo pero coherente económicamente.
- **C — Esperar a tener clientes pagando Centro Fiscal antes de invertir en tiers**: revenue solo del add-on, plans base nunca se cobran. Riesgo regalar producto base.

## Decisión
**B**. Aunque implica 4-6h dev extra antes de beta privada, evita la incoherencia de cobrar 14,90€ del add-on a clientes con Plan Pro (23€) gratis. Implementar tras validar trial sandbox (sub-opción: cobrar solo addon en sandbox interno, conectar tiers antes de invitar beta-testers externos).

## Consecuencias
Mig 151 pendiente añadir columnas `stripe_price_id_mensual/anual/stripe_product_id` en `plans` + `plan_stripe_subscription_id/plan_subscribed_at/plan_canceled_at/plan_billing_cycle` en `organizations`. Endpoints `/api/billing/tiers/checkout` + `/portal` nuevos. Webhook `stripe-webhook` extiende con branches `metadata.kind='plan_tier'`. Aplaza beta privada ~1 semana. Cuenta Stripe inicialmente en modo Test (cobros ficticios) hasta validación trial. Decisión cuenta Stripe (agencia Agentesia Madrid vs SL FacturaIA separada) sigue pendiente entidad jurídica que firma con clientes finales.
