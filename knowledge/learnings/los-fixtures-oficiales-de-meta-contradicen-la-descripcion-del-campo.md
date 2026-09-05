---
title: los fixtures oficiales de Meta contradicen la descripción del campo
date: 2026-09-05
source: mandadm
tags: [meta, instagram, webhooks, fixtures]
---

En los webhooks de Instagram, `entry.time` se describe como segundos, pero **los cuatro ejemplos de
payload de las páginas oficiales lo traen en milisegundos**. Los `messaging[].timestamp` del mismo
sobre también son ms. Si parseas por la descripción, las fechas salen a 1970.

No se arregla eligiendo una unidad ni marcando el campo por endpoint (llegan mezclados en el mismo
sobre): **se normaliza por magnitud** en la frontera de entrada, una sola vez, y el resto del sistema
ve siempre lo mismo.

Regla general, no solo de Meta: cuando la prosa de una API y sus ejemplos discrepan, **manda el
ejemplo** —es lo que el emisor genera de verdad— y el parser tiene que aguantar los dos.

Otros dos que costaron aquí, del mismo proveedor:
- `refresh_access_token` devuelve el error **plano** (`{error_type, code, error_message}`), no anidado
  bajo `error` como el resto de la Graph API. Un clasificador que solo entiende la forma anidada lee
  «permiso retirado» como fallo pasajero y reintenta hasta que el token caduca solo.
- Ninguna de las 18 páginas dice **con qué secreto firma Meta `X-Hub-Signature-256`** en una app de
  Instagram Login. Solo se sabe capturando un POST real.

Ver [[extract-error-objeto-anidado-en-apis-modernas]] · [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]]
