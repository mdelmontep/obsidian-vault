---
title: el atajo de rendimiento de un escáner decide en silencio qué NO se mide
date: 2026-08-23
source: facturaia
tags: [testing, candados, mutacion, arnes]
---
Un candado que barre `src/` empieza por un atajo para no leer ficheros
irrelevantes. Ese atajo es una segunda regla de alcance, escrita donde nadie la
revisa: si está mal, el escáner sale a cero **porque no mira**, no porque no
haya nada.

Caso (#2138): la aserción medía cuerpos HTTP y arrancaba con
`if (!/\b(message|error)\s*:/.test(fuente)) continue` — la forma de clave de
literal de objeto. Pero la frase también viaja por POSICIÓN
(`errorJson(frase, status)`, `new ApiError(status, code, frase)`), así que un
fichero cuyo único emisor era posicional, sin un solo `error:` en todo el
archivo, salía por el atajo antes de medirse. Lo destapó `mutate`: la mutación
del emisor posicional dio **SIN VÍCTIMA** con el candado en verde.

Regla: el atajo se prueba con una mutación DE CADA FORMA que el candado dice
cubrir, no de una. Y la forma en que un valor llega al sink (clave de objeto vs
argumento posicional) es parte del alcance, no un detalle de implementación.
Emparenta con [[un-trinquete-por-fichero-absuelve-al-que-ya-importa-el-helper]]
y [[lo-que-un-barrido-omite-no-puede-darse-por-recuperado]].
