---
title: el proxy de next trunca el body a 10mb en silencio y rompe firmas hmac
date: 2026-08-21
source: facturaia
tags: [nextjs, hmac, proxy, uploads]
---
El proxy/middleware de Next 16 clona y buffera el body de TODA ruta que su
`matcher` intercepta, con techo de 10 MB (`experimental.proxyClientMaxBodySize`).
Por encima **trunca sin fallar el request**: el handler recibe el body cortado,
su hash SHA-256 ya no casa con la firma HMAC del caller → `401 bad_signature`
intermitente (solo payloads grandes; los pequeños de la misma tanda pasan).
Caso real: 5 runs del productor de vídeo (15-19 ago), ~5,40 € quemados por run
con el dinero de la generación ya gastado antes de subir.
Fix en el origen: excluir la ruta firmada del `matcher` (su auth es el handler,
no el proxy) + guard test que compila el matcher con el path-to-regexp del
propio Next. Cinturones: re-firmar en CADA reintento y preflight barato (payload
>10 MB que no pasa magic bytes → 415 = camino verde) ANTES de gastar dinero.
Ojo: cualquier otra ruta de subida que siga pasando por el proxy hereda el
mismo techo aunque declare `MAX_*_BYTES` mayor (facturaia: issue #2055).
