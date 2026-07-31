---
title: un límite de peticiones en el healthcheck no puede responder 429
date: 2026-07-31
source: claude-code-session
tags: [infra, traefik, dokploy, rate-limit, seguridad]
---
`/api/health` era anónimo y hacía dos consultas a Postgres por petición: amplificador de carga
gratis. El arreglo obvio (rate limit por IP que devuelve 429) **tira la producción**: quien sondea
ese endpoint es Traefik/Dokploy, desde la red interna y con la misma IP para todos los sondeos. Un
429 se lee como "no sano" y el balanceador deja de enrutar tráfico al contenedor.

Lo que sí funciona, por orden de valor:
1. **Caché de proceso muy corta** (5 s). Aplana una ráfaga de miles de peticiones a dos consultas
   cada 5 s, y queda muy por debajo de cualquier intervalo de healthcheck, así que no retrasa la
   detección de una caída real.
2. Límite por IP que, al superarse, **sirve la última respuesta conocida con su código de estado**,
   nunca un 429. Quien abusa no consigue carga; quien vigila sigue recibiendo el estado real.

Generalizable: antes de meter un guard en un endpoint, pregunta **quién lo llama de verdad**. En los
de infraestructura el llamante legítimo es un robot que interpreta el código de estado como un
veredicto sobre tu servicio. Caso real: FacturaIA `qa-015`.
