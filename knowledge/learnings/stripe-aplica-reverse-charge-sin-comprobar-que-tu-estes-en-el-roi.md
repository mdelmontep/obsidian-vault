---
title: Stripe Tax aplica reverse charge mirando el NIF del cliente, no si TÚ estás en el ROI
date: 2026-08-14
source: claude-code-session
tags: [stripe, fiscal, iva, espana, vies, roi]
---

Stripe Tax decide la inversión del sujeto pasivo por el NIF-IVA del **cliente** y las
jurisdicciones implicadas. No mira si el **emisor** está en el ROI. Comprobado emitiendo
factura real en sandbox: cliente alemán con VAT → 99 € sin IVA y «Tax to be paid on reverse
charge basis» al pie, con el emisor español fuera del ROI.

**Y resulta que eso es correcto.** DGT V1275-17: el servicio a un empresario de otro Estado
miembro «no se entenderá realizado en el territorio de aplicación del Impuesto», y añade
«con independencia de que la consultante se encuentre dada de alta en el Registro de
Operadores Intracomunitarios». La no sujeción es objetiva; el ROI no la condiciona.

Lo que sí falta sin ROI es **censal**: la AEAT exige el alta para «prestar servicios que
se entienden realizados en el territorio de otro Estado miembro» (036, casilla 582), y de
ahí cuelga el modelo 349. Incumplirlo es infracción formal (art. 198 LGT: 20 €/dato,
mínimo 300 €, mitad si regularizas sin requerimiento), no una liquidación de IVA.

**Trampa de diagnóstico**: `VIES → isValid: false` sobre tu propio NIF **no indica errata**.
VIES solo publica los inscritos en el ROI, así que el `false` es lo esperado si no has
pedido el alta. Pedirla no es inmediato: hasta 3 meses, **silencio negativo** y posible
comprobación censal con visita, así que se solicita antes de tener el cliente, no cuando
aparece. Ver [[stripe-sin-account-tax-ids-la-factura-sale-sin-nif-del-emisor]]
