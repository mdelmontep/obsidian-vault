---
title: la cabecera Accept dice qué formatos sirve una API, sin adivinar URLs
date: 2026-09-05
source: facturaia
tags: [api, integraciones, metodo, facturadirecta]
---
Para saber si una API de terceros sirve un formato que su documentación no menciona (PDF, CSV, XML), la vía barata **no** es probar sufijos y rutas a ciegas. Un `406` bien hecho enumera lo que el servidor sí acepta.

Caso real (FacturaDirecta, 4-sep-2026): doce tanteos de URL —`/{uuid}.pdf`, `/pdf`, `?format=pdf`, `/document`, `/print`, `/render`, `/download`, `/preview`, `/export`, `/original`— todos 404, que no distingue «no existe aquí» de «no existe en ninguna parte». Una sola petición con `Accept: application/pdf` cerró la pregunta:
`406 {"message":"Server accepts application/json,text/plain,application/octet-stream,application/javascript"}`.

Corolarios del mismo tanteo: un `related=` (o `expand=`, `include=`) que responde **400 enumerando los valores válidos** es la otra fuente gratis de la superficie real; y un 404 en una API REST bien construida es sobre todo información sobre el enrutador, casi nunca sobre la capacidad.

Vale igual para verbos: preguntar por `OPTIONS`/`Allow` antes de asumir que un recurso es de solo lectura. Ver [[un-catalogo-de-capacidad-de-un-tercero-escrito-a-mano-miente-en-silencio]]
