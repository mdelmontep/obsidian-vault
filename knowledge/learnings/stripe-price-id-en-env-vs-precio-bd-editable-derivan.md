---
title: stripe price (lo que cobra) vive en env, no en el precio editable de la bd
date: 2026-06-26
source: claude-code-session
tags: [stripe, pricing, billing, saas]
---

Dos fuentes para "el precio" → drift silencioso:
- **Mostrado**: `plans.precio_mes`/`precio_anual` en BD, editable desde /admin.
- **Cobrado**: `STRIPE_PRICE_ID_*` en el env (objeto price de Stripe, **inmutable**:
  no se puede editar `unit_amount`).

Editar el precio en admin cambia la UI pero NO lo que Stripe cobra → la UI dice
14€ y el checkout cobra 19€. Para cambiar el cobro real: crear un price NUEVO en
Stripe + rotar la env var + redeploy. Suscripciones existentes conservan su price.

Fix de fondo (single source): guardar el `price_id` en la fila de `plans` y que
admin, al cambiar el precio, cree el price en Stripe vía API y persista su id.

Mientras sigan separados: sincronizar a mano siempre que se toque el precio.
