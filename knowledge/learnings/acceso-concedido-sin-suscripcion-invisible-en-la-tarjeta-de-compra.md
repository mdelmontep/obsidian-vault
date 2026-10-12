---
title: un acceso concedido sin suscripción es invisible si la tarjeta de compra mira solo lo pagado
date: 2026-10-12
source: facturaia (PR #3385, Fabbros)
tags: [billing, entitlements, stripe, ui]
---
Dos fuentes dan acceso a un módulo: la suscripción (`org_complementos`, Stripe) y la
concesión a mano (`org_features` con source `manual`/`grandfathered`). La tarjeta de
Complementos derivaba «Activo» solo de la primera → a quien tenía el módulo regalado le
ofrecía «Activar» por 99 €/mes, y un clic abría un cobro real por lo que ya tenía.

Patrón: el estado que pinta una UI de compra se deriva de TODAS las fuentes de acceso.
Estado aparte (`concedido`, excluyente con `contratado`: lo pagado manda), sin «Activar»
ni «Cancelar» (no hay suscripción). Si la lectura de concesiones falla, lanzar: leer
«no concedido» por error vuelve a ofrecer el cobro.
Tell: el menú muestra el módulo y Ajustes dice que no lo tienes.
