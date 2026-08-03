---
title: un límite por ip que cuenta todas las peticiones anula el límite por credencial
date: 2026-08-03
source: claude-code-session
tags: [rate-limit, seguridad, api, diseño]
---

Topes típicos: 600/min por clave de API, 60/min por IP. Si el contador por IP cuenta TODAS
las peticiones, el de 600 es inalcanzable: una integración legítima detrás de un NAT se come
un 429 a las sesenta, y las otras 540 que su plan le permite no las ve nunca.

El límite por IP es un control ANTI-FUERZA-BRUTA: su sujeto son los **intentos fallidos**,
no las peticiones. Se consulta/incrementa **cuando la autenticación falla**. Así el tráfico
bueno no lo toca jamás y el que prueba credenciales lo gasta en cada intento — que es a quien
va dirigido, porque quien nunca autentica no llega a ningún contador que dependa de la
organización.

Y al agotarse, contestar el 429 y no el 401: al que está probando le sirve más «para» que
«esa credencial no vale», que le confirma que puede seguir.

Regresión real (TuCRMIA, 3-ago): desplegada y corregida el mismo día. El smoke E2E la habría
cazado en dos minutos —hace ~600 peticiones autenticadas y habría muerto en la 60—, pero se
corrió DESPUÉS del push. Un cambio en el pipeline de una API pide el smoke antes.
Ver [[traefik-dokploy-client-ip-x-real-ip-o-ultimo-xff]].
