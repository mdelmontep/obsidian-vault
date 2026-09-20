---
title: el gate no se calla — responde a OTRA pregunta, y su «no aplica» convalida una evidencia caducada
date: 2026-09-20
source: agh-iberica
tags: [gate, ci, metodo, agh]
---
El paso `ui:evidence` sólo se exige si el diff toca `dashboard/web`. Una PR que toca
`dashboard/scripts` obtiene `ui: no aplica` y `✓ VERDE` **con una corrida de navegador
de otro día pegada en el cuerpo**. Y no era la misma medida con otra fecha:
`70 cruces · 676 controles · 4 conocidos` pasó a `80 · 868 · 22` al re-correrla,
porque había cambiado `main` por debajo.

La primera formulación —«el gate se calla»— es cómoda y **manda al arreglo
equivocado**, que es hacerle decir más cosas. El diagnóstico correcto:

> **El paso responde con VERDAD a una pregunta distinta de la que se le lee.**
> Contesta «¿tu diff toca la vista?» y el cuerpo de la PR lo lee como «¿está medida
> la UI de esta PR?». El instrumento no miente, no se calla y no falla.

El agujero es que **dos preguntas comparten una casilla del resumen y un mismo
veredicto**. Mientras `ui: ok — 60 cruces` y `ui: no aplica` ocupen el mismo sitio y
produzcan el mismo verde, cualquiera de las dos convalida el cuerpo.

Es **el mismo modo de fallo que `mergeStateStatus=CLEAN`**: también responde con
verdad a «¿git sabe combinarlo?» y se lee como «¿el diff es el mío?». Y en los dos
casos **el modo peligroso es el que NO te para** — un rojo se investiga, un verde se
pega en la PR y se mergea.

Arreglo que sí cierra: (a) toda medida cara pegada en un cuerpo lleva **el SHA sobre
el que se tomó**, y algo lo compara con la punta antes de mergear; (b) `no aplica` y
`ok` **no pueden producir el mismo veredicto legible** — si el paso no se ejerció, el
resumen dice que esta PR **no tiene evidencia propia**, no que esté bien.

⚠️ Y el candado tiene que morder: si pasa igual con una evidencia caducada en el
cuerpo, no mide. Se comprueba envejeciendo el informe a mano.

Ver [[evidencia-fechada-por-reloj-muere-en-un-rebase]] y
[[un-test-de-paridad-por-muestreo-no-discrimina-la-copia]].
