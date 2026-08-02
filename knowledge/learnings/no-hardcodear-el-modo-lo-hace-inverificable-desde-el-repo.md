---
title: la regla de "no hardcodear el modo" lo vuelve inverificable desde el repo
date: 2026-08-02
source: claude-code-session
tags: [deploy, dokploy, verificacion, produccion, riesgo]
---

Sacar del repo la variable que decide el modo de ejecución (`TRADING_MODE`, `DRY_RUN`,
`SANDBOX`, `NODE_ENV`) es higiene correcta. El efecto secundario es que **el repo deja de
ser evidencia de en qué modo corre nada**, y un checklist pre-deploy que la comprueba en el
compose o en el `.env.example` da verde leyendo una plantilla.

Es peor que un env normal: un modo mal puesto no da 401 ni rompe el arranque. Ejecuta
perfectamente la cosa equivocada, y en la dirección irreversible (dinero, emails, borrados).

Regla: el ítem del checklist no es "el compose no lo hardcodea", es **leerlo del sistema
vivo** — `/health` que devuelva el modo, `docker exec printenv`, o el endpoint que exponga
el efecto. Si nada lo expone, ese es el arreglo previo.

Caso real (cryptobruj, 01-ago): compose limpio y `.env.example` con `paper`; el bot llevaba
32 h en `mode: live` con −1.613 USDT realizados y expectancy −0,244R. Se descubrió por
`curl /health` justo antes de desplegar, no por el checklist.

Ver [[verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado]] ·
[[webhook-hmac-pass-through-verificar-env-real-no-solo-codigo]]
