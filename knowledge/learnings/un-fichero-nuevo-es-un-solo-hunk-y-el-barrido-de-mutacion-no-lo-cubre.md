---
title: un fichero nuevo es un solo hunk, así que el barrido de mutación le da un mutante
date: 2026-08-14
source: claude-code-session
tags: [mutacion, tests, arnes, cobertura]
---

`git diff -U0` de un fichero **nuevo** produce **un hunk**, y un arnés que muta «un mutante por hunk»
le da exactamente uno. Medido: 491 líneas nuevas → 1 hunk → 1 mutante, que además cayó en la línea 1 y
salió «arnés roto». **Cobertura de mutación efectiva cero**, y la salida no lo dice.

Dos consecuencias, y la segunda es peor:

- La PR que **construye** un candado es justo la que más necesita el barrido, y es la que recibe menos.
- Su hermana: un diff que solo toca `**/test/**` recibe *«la rama no toca ficheros de producción. Nada
  que barrer»* — que se lee como *todo en orden* cuando significa *no he mirado*.

Fix mientras no haya barrido derivado: **montar la lista a mano desde el propio fichero** (una
mutación por línea de código, con control por mutación), no desde tus hipótesis. En un caso así salieron
36 víctimas / 8 sin víctima, y **los 6 huecos reales estaban todos en el cableado** (`main()`, el guard
del entry point, los contadores) — ninguna función pura fallaba.

Y para tests que aseveran sobre producción sin importarla (CSS, fixtures), muta **el fichero de
producción**, que no está en el diff. Ver [[una-tanda-de-mutaciones-a-mano-hereda-tu-hipotesis]].
