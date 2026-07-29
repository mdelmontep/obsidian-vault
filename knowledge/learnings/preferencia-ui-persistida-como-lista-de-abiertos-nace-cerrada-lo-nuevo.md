---
title: una preferencia guardada como "lista de abiertos" hace nacer cerrado todo lo que añadas después
date: 2026-07-29
source: claude-code-session
tags: [frontend, ux, localstorage, facturaia]
---

Patrón habitual: guardar en localStorage el set de secciones ABIERTAS de un menú, con default "todo abierto" cuando no hay preferencia. Funciona hasta que añades una sección nueva: para todo usuario con preferencia guardada, la sección nueva NO está en la lista, así que se restaura plegada. Justo la que quieres que se vea.

La ausencia en el payload es ambigua: no distingue "el usuario lo cerró" de "no existía cuando guardó".

Fix (sin perder preferencias, que es lo que haría bumpear la clave): versionar el payload — `{ v: N, s: [...] }` — y un mapa `SECCIONES_AÑADIDAS_EN[version]`. Al restaurar, unir a lo guardado todo lo introducido en versiones > la guardada. La siguiente escritura ya persiste con la versión nueva, así que si el usuario la cierra, se queda cerrada.

Mismo agujero en cualquier preferencia guardada como lista de "activos" (columnas visibles, filtros, features de onboarding vistas). Guardar la lista de CERRADOS invierte el problema pero no lo quita.

Caso: sidebar de TuFacturaIA, Obras promovida a familia propia. Ver [[facturaia]].
