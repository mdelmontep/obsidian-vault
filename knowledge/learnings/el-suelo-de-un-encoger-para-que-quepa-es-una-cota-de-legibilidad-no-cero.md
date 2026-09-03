---
title: el suelo de un «encoge para que quepa» es una cota de legibilidad, nunca cero
date: 2026-09-03
source: facturaia
tags: [render, diseno, busqueda-binaria, degradacion, pdf]
---
Cualquier «reduce el tamaño hasta que entre» —cuerpo de letra de un rótulo, ancho de columna,
escala de una imagen— se implementa como búsqueda del mayor valor factible. Y el suelo del
intervalo **es una decisión de producto disfrazada de detalle numérico**: con suelo 0, la búsqueda
considera factibles tamaños arbitrariamente cercanos a cero, que satisfacen la restricción **por la
vía de no dibujar nada**. La restricción queda respetada y el elemento no existe. No falla nada.

FacturaIA 3-sep (reel): con un logo grande abajo, el CTA salía a `font-size:0vh` desde `alto_rel
0,135` y a 7px sobre 1920 desde 0,07 — publicado, invisible, sin error. Arreglar solo el cero
habría dejado el tramo de 7px. El suelo correcto era el cuerpo de la firma legal «Hecho con IA»:
**el texto más pequeño que la casa ya publica dando por hecho que se lee**, así que es una cota
defendible y no un número a ojo.

Y el suelo hay que **comprobarlo**, no asumirlo: si tampoco cabe, se devuelve igual y se acepta el
solape, porque por debajo no hay soluciones, solo maneras de no tener rótulo. Eso invierte una
garantía («el tope se respeta siempre») y obliga a reescribir todo lo que la afirme.
