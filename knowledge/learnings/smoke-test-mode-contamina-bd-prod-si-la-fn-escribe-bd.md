---
title: smoke en test-mode contamina la bd de prod si la función también escribe en bd
date: 2026-06-27
source: claude-code-session
tags: [stripe, testing, supabase]
---
Una función que acopla una API externa (modo según la key) + ESCRITURA en BD de
prod (ej `createPriceForTarget` → crea price en Stripe + fila en `plan_prices`)
contamina prod en un smoke "de test": Stripe TEST mode NO aísla la BD, que sigue
siendo la única (prod). Un price de test acabaría bajo un plan real → checkout
roto.

Fix (doble protección):
1. Guard duro: el script rehúsa `sk_live`/`rk_live` (exit 1) → solo corre con
   `sk_test_*`.
2. Dato SENTINEL desechable que NINGÚN consumidor de runtime resuelve (ej
   `target_id='__smoke_007__'`), crea su propio producto de test y limpia en
   `finally`. Aunque corra contra la BD prod, solo toca filas sentinel.

Regla: si la fn bajo smoke escribe en una BD compartida, aísla por DATO
(sentinel) o por ENTORNO (BD staging) — no basta el modo de la API externa.
Relacionado: [[stripe-price-id-en-env-vs-precio-bd-editable-derivan]]
