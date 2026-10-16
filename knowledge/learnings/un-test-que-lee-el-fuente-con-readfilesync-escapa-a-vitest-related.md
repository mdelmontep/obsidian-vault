---
title: un test que lee el fuente con readFileSync escapa a vitest related
date: 2026-10-15
source: facturaia
tags: [vitest, tests, pre-push]
---
`vitest related <ficheros>` elige los tests siguiendo el grafo de **imports**. Un test que
lee el fuente como texto (`readFileSync('src/.../x.sql')`, candados de forma de migraciones,
trinquetes que barren el árbol) no importa ese fichero, así que no sale como relacionado. Tocas
el fuente, el pre-push corre `related`, sale verde, y el candado que lo vigila no se ha ejecutado.

Fix: si tocas un fichero que un test lee por ruta, córrelo a mano por nombre. Para encontrarlos:
`git grep -l "readFileSync" -- '*.test.ts' | xargs grep -l "<nombre del fichero>"`. Lo cazó
facturaia-39 en el tren 4 del albarán de venta (15-oct).

Dos disparadores obligan al barrido: crear una ruta con `[id]` (hay candados que barren
`src/app/api`) y MOVER lógica de fichero (el candado sigue leyendo el de origen). Los specs de
Playwright `e2e:layout` que leen el JSX tampoco salen: si tocas componentes, córrelos. Tres rojos
de una sola rama en el tren 11 (#3585, 16-oct); desde #3593 el pre-push lo hace solo.

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]].
