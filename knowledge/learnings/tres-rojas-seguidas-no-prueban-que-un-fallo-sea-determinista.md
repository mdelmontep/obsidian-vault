---
title: tres rojas seguidas no prueban que un fallo sea determinista
date: 2026-09-17
source: agh-iberica
tags: [testing, gate, flakes, medicion]
---
Un test cayó en tres corridas seguidas del gate, **siempre el mismo fichero y siempre con la
misma firma**. Lo filié como rojo determinista de `main` y lo escribí así en el issue, en la
PR y en el canal. La cuarta corrida salió verde: era intermitente.

El error de razonamiento es reutilizable. «Los ficheros en rojo **cambian** entre intentos»
discrimina la firma de máquina cargada, pero su negación —*siempre el mismo*— **no** prueba
determinismo: tres repeticiones de un fallo de probabilidad alta son lo esperable. Y las dos
conclusiones mandan a colas distintas: un rojo estable se lee como «`main` está roto», un
intermitente como «hay que arreglar el arnés».

Patrón: decir el **conteo** (`3 de 4`), nunca el adjetivo. Y separar lo que no depende del
conteo — la **no atribución medida por contenido** (el diff no toca el test ni su sujeto, así
que son byte a byte los de `origin/main`) seguía en pie con la cuarta verde, porque nunca
dependió de qué corrida saliera cómo.

Corolario incómodo: un intermitente es **peor** que un estable. Tiene la cara de una
regresión ajena en cada PR, y no se descarta re-corriendo sin normalizar «pues vuelve a
tirarlo». Ver [[un-rojo-de-gate-ajeno-con-la-cara-de-uno-propio]].
