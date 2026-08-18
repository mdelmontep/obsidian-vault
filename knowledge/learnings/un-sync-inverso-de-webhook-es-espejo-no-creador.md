---
title: un sync inverso por webhook es espejo, no creador — lo que nace en el panel del proveedor no entra
date: 2026-08-18
source: claude-code-session
tags: [stripe, webhook, sync, gotcha]
---

Un handler de `*.created|updated|deleted` que mantiene una tabla local como espejo del
proveedor suele buscar la fila por su id externo y, si no la encuentra, salir con un
`ignored_unknown`. Es correcto —no quieres que un objeto ajeno cree filas— pero tiene una
consecuencia que sorprende: **un objeto creado a mano en el panel del proveedor no aparece
en tu BD**, aunque el webhook llegue y responda 200.

Medido el 18-ago en TuFacturaIA: al **archivar** un Price desde el dashboard de Stripe, la
fila de `plan_prices` se puso `active=false` sola (existía, el espejo la reflejó). Al
**crear** el Price nuevo, no pasó nada: `syncPriceFromStripe` no lo conocía. La fila hubo
que insertarla a mano replicando lo que hace el creador del propio código
(`createPriceForTarget`).

**Regla**: si haces en el panel del proveedor algo que normalmente hace tu app, comprueba
las DOS direcciones. Y no infieras que el sync funciona porque una de ellas se reflejó.

Corolario para precios: verificar al final que importe local == importe del proveedor para
todas las filas activas, que es lo que mide un chequeo de coherencia — no basta con ver la
fila nueva.
