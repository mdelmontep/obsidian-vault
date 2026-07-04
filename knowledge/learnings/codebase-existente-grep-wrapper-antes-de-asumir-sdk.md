---
title: en codebase existente, grep cómo integra el SaaS antes de asumir su SDK
date: 2026-07-04
source: claude-code-session
tags: [integraciones, subagentes, stripe, arquitectura]
---
Antes de añadir una integración con un SaaS que tiene SDK conocido (Stripe, etc.)
en un repo existente: `grep` cómo YA lo llama el proyecto. Puede tener un wrapper
REST propio por decisión deliberada (sin el paquete SDK) — p.ej. FacturaIA usa
`src/lib/billing/stripe-rest.ts` (`stripeForm`/`stripeGet` sobre `fetch`, form-encoded,
sin reenviar el body de error), NO el paquete `stripe`.

Consecuencia con subagentes: instruir "reusa el patrón del repo (grep primero)",
NUNCA "usa el SDK de X". Un fork/subagente que asume el SDK construye algo que
rompe la convención (imports inexistentes, cliente paralelo) y hay que rehacerlo.
Caso real: un fork para Stripe Connect asumió `new Stripe()` y falló entero; al
reconocer el wrapper y extenderlo (header `Stripe-Account` aditivo) salió limpio.
Generaliza "imita el patrón del fichero vecino" al brief de subagentes.
