---
title: no se verifica que una credencial es de solo lectura escribiendo con ella
date: 2026-07-26
source: claude-code-session
tags: [seguridad, credenciales, stripe, metodo, incidente-propio]
---

Error cometido 2026-07-26 en FacturaIA: para comprobar que una restricted key de
Stripe era read-only lancé `POST /v1/prices` esperando un 403. Devolvió **200**:
creó un producto y un price reales en una cuenta live. La prueba diseñada para
confirmar que no se puede escribir **fue la escritura**.

- La ausencia de permiso de escritura **no es verificable por lectura**. Se
  comprueba en la pantalla de la credencial (Stripe Dashboard → la fila de la
  key lista cada recurso con Read/Write/None), o se asume no verificada y se dice.
- Lo que sí se verifica leyendo: **a qué cuenta pertenece** (`GET /v1/account`
  devuelve el `acct_`) y que el objeto que te interesa existe (`GET /v1/prices/<id>`).
  Con eso se descartan los dos errores frecuentes sin tocar nada.
- Un 403 esperado no es una hipótesis inocente: si te equivocas, el efecto es
  irreversible en un sistema de terceros. Vale la misma cautela que un DELETE.
- Limpieza si ya pasó: archivar (`active=false`) producto y price. Stripe no
  permite borrarlos, así que el rastro queda; hay que decirlo, no taparlo.

Colateral del mismo día, que refuerza [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]]:
la key se había creado con la cuenta equivocada seleccionada en el dashboard
(AgentesIA en vez de Tufacturaia), así que el producto sonda aterrizó en la
cuenta que no era y, además, todos los `GET /prices/<id>` daban 404 legítimo. Un
`GET /v1/account` de una línea lo habría detectado antes de cualquier otra cosa.
Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
