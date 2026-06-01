---
title: stripe tax en españa por api — tax_behavior exclusive + registro ue con place_of_supply_scheme
date: 2026-06-01
source: claude-code-session
tags: [stripe, facturaia, iva, billing]
---

Para cobrar "precio + IVA" con Stripe (no IVA incluido) y que Tax lo calcule:

- **Precios** con `tax_behavior=exclusive` (importe SIN IVA; Stripe añade el % en checkout). `inclusive` = IVA dentro.
- **Checkout Session** necesita `automatic_tax[enabled]=true` + `billing_address_collection=required` + (customer existente) `customer_update[address]=auto`. Para NIF/VAT B2B: `tax_id_collection[enabled]=true`.
- **Activar Tax por API**: `POST /v1/tax/settings` (`defaults[tax_behavior]`, `head_office[address][country]=ES`) — puede requerir aceptar términos en Dashboard.
- **Registro fiscal** (sin él NO calcula IVA del país): `POST /v1/tax/registrations` con `country=es`, `country_options[es][type]=standard` Y el subcampo obligatorio **`country_options[es][standard][place_of_supply_scheme]=standard`** (UE lo exige; sin él da error "requires standard to be specified"). `standard` = IVA solo a ventas en ese país.
- **Trampa bash**: `curl` sin `-f` devuelve 0 aunque Stripe responda 4xx → un `&& echo OK` da falso positivo. Verificar el JSON (`.status`/`.error`).
- Verificar todo sin cobrar: `POST /v1/tax/calculations` (19€ ES → 22,99€, 21%).
