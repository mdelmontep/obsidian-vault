---
title: el número que se reporta se lee del disco, no de la memoria de la sesión
date: 2026-09-13
source: centro-elphis
tags: [medicion, arnes, retell, voz, evals, metodo]
---

El 12-sep cerré una comparación de dos versiones del agente de voz de Elphis con «v46 89/96,
v47 92/96 → publicar v47». El 13-sep, antes de publicar, releí las corridas guardadas en
`runs/`: **v46 114/119, v47 102/119**. No es que el margen fuera estrecho: el ganador estaba
invertido, y v47 empeoraba justo los casos de crisis (`CR · duda — NO transfiere` 10/10 → 6/10;
`CR · harto de vivir asi` 7/10 → 4/10).

Las 20 corridas están en disco, en dos tandas (`-r1..r6` de las 12:44 y `-c1..c4` de las 13:03).
**En las dos por separado gana v46** (70/72 vs 64/72, y 44/48 vs 38/48). Ningún subconjunto da
92/96 a v47, y `96 = 8 × 12` no corresponde a ninguna de las dos. Es decir: el número que
reporté no salía de los ficheros que yo mismo había escrito.

Lo que falla no es el arnés, que guardaba el crudo correctamente. Falla el paso de leerlo.
Una tabla construida a mitad de sesión y luego arrastrada por el contexto es una afirmación sin
respaldo en cuanto pasa una compactación, un descanso o dos tandas más.

**Regla:** el número que se reporta se lee del disco **en el momento de reportarlo**, con el
script que agrega todas las corridas de la rama — no las que uno recuerda haber corrido. En este
arnés eso es `tabla.py`, y agrega por prefijo, así que incluye las tandas que uno ya había
olvidado (`-c*` además de `-r*`).

Corolario del mismo día: sin un sello del artefacto medido, la reconstrucción a posteriori es
imposible — la etiqueta la pone la mano que lanza el comando. `medir.py` sella desde el 12-sep el
sha256 del flow leído del servidor justo antes de crear el batch (`flow_sha` en el fichero de la
corrida); las 20 corridas de esta comparación son anteriores y salen todas como `(sin sello)`.

Y el precio de no releer: estuve a un `publish-agent-version` de desplegar a producción la versión
peor, con la comparación ya guardada en disco diciendo lo contrario.

Ver [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]] y
[[una-medicion-correcta-puede-tener-el-alcance-de-mas]].
