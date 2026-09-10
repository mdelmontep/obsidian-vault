---
title: dos locales del mismo negocio van en un @graph con branchOf, no como dos fichas
date: 2026-09-10
source: ecobox
tags: [seo, schema-org, json-ld, clientes-locales]
---
Cliente con dos sedes que comparten teléfono. Publicar **dos `LocalBusiness`
sueltos** le dice a Google «dos negocios distintos con el mismo número» —el
patrón exacto de los directorios de spam— en vez de «dos locales del mismo
negocio».

Forma correcta: un `@graph` con una `Organization` (la que lleva el CIF) y una
ficha por local, cada una con `branchOf: {"@id": <id de la organización>}`. Los
`@id` estables y legibles (`#taller-majadahonda`), porque son la dirección del
nodo dentro del grafo: si cambian, las referencias quedan colgando en silencio.

Y el dato que no tienes se **omite**, no se aproxima: sin coordenadas de la
segunda sede, `geo` fuera. Las del centro del municipio dejan el pin en otra
calle y el cliente llega a otro sitio. `geo` es opcional; la dirección postal
ya identifica el local.

Lo que de verdad mueve el pack local no es esto: es la **ficha de Google Business
Profile por local**, que solo puede verificar el titular. El JSON-LD dice qué eres
y cuántos locales tienes; la ficha pone el pin y recoge reseñas.
