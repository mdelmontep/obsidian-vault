---
title: "stripe: el CLI --live puede ir a otra cuenta que la sk_live de la app → 'No such price' es falso positivo"
date: 2026-07-07
source: claude-code-session
tags: [stripe, cli, billing, gotcha, auditoria]
---

Los IDs de objeto de Stripe **llevan el sufijo de la cuenta**: `price_1Tm…GgQMT2aOqB` (cuenta `acct_1Td5cc…GgQMT2aOqB`) vs `price_1T…QY4tV8FMxQ` (cuenta `acct_1TJrQv…QY4tV8FMxQ`). Si `stripe login` te autenticó a una cuenta y la `STRIPE_SECRET_KEY` de la app es de OTRA, `stripe prices retrieve <id> --live` devuelve **"No such price"** aunque el price exista perfectamente — está en la cuenta de la app, no en la del CLI.

Gotcha real (FacturaIA 2026-07): casi reporto "Plus no comprable / precios rotos" en una auditoría; eran de la cuenta equivocada. Además reencuadra bloqueos de Connect: si montas Connect/KYC vía el CLI pero el cobro en prod usa `sk_live` de otra cuenta, estás configurando la cuenta que no es.

Fix: verifica SIEMPRE contra la cuenta de la app, no la del CLI:
`curl https://api.stripe.com/v1/account -u "$SK:"` (con la sk_live real de la app) para ver el `acct_` de verdad, y `curl .../v1/prices/<id> -u "$SK:"` para comprobar existencia/importe. Ver [[stripe-connect-signup-gotcha-crear-cuenta-conectada]].
