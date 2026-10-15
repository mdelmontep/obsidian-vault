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

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]].
