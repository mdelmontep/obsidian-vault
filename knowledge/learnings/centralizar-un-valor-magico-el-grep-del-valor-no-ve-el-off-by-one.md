---
title: al centralizar un valor mágico, el grep del valor no ve el off-by-one
date: 2026-09-17
source: ecobox
tags: [refactor, css, metodo]
---
Altura del header (80px) repetida en nueve sitios → token `--header-h`. El barrido fue
`grep 80px` y dejó viva una décima copia escrita como **`top: 79px`**: el borde inferior del
header, o sea el mismo valor menos uno. Al meter una barra encima, el header bajó 40px y esa
línea se quedó cruzando el logo por la mitad, en producción.

Un valor mágico no se copia solo tal cual: se copia **±1** (bordes, solapes), en `calc()`, y
partido (`40` + `40`). El grep del número literal no ve ninguna de las tres.

Al centralizar, grepear también `valor-1`, `valor+1` y la mitad, y leer los aciertos: si el
número aparece en un contexto donde el token explica *por qué* ese número, es una copia
aunque no coincida. Barato: la lista de candidatos cabe en un `grep -nE "(79|80|81|40)px"`.
