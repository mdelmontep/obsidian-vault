---
title: seed RSC de la 1ª página solo es seguro con guard contra estado que solo existe en cliente
date: 2026-07-22
source: claude-code-session
tags: [nextjs, rsc, react, hooks]
---
Patrón: `page.tsx` (server) precarga la 1ª página de un listado con los defaults del View y la pasa como prop `initialX`; el hook/View la siembra en el primer render y salta su fetch inicial para matar el waterfall bundle→efecto→fetch.

Riesgo: si algún filtro/orden/pageSize puede venir de `localStorage` o de la URL (deep-link), el servidor NO puede saber su valor real en ese request. Sembrar ciegamente pinta datos que no corresponden al estado real del usuario.

Fix: comparar el estado EFECTIVO del primer render (incluyendo lo que resuelve `localStorage`/`searchParams` en cliente) contra los defaults asumidos por el server-fetch, en el propio componente/hook. Si coincide exacto → usar el seed. Si diverge → tratar el seed como `undefined` y dejar que el fetch cliente normal corra — nunca mostrar el seed cuando no se sabe si es correcto. Mismo criterio que "pasar `undefined` en error de carga, no `[]`": ante la duda, degradar al camino ya probado, no fingir un dato.
