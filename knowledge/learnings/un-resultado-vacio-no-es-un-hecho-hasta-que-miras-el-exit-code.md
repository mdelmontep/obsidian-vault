---
title: antes de la hipótesis grave, descarta la aburrida — suele estar ya medida en tu propia pantalla
date: 2026-08-24
source: facturaia
tags: [debugging, sesgo, verificacion, procesos]
---
Maté un `git push` colgado con `pkill -f` y, en la misma orden, imprimí el recuento de procesos
vivos. Salió **`1`**. Lo leí como ruido porque la línea siguiente confirmaba lo que yo esperaba.
Ese `1` era un `git push` que sobrevivió al `pkill` y que **completó la transferencia dos horas
después, él solo**. De ahí construí una hipótesis grave y falsa —un gate que imprime «bloqueado»
y no bloquea— y llegué a montar un experimento para probarla.

Dos reglas, y la segunda es la cara:

- **Tras matar algo, la verificación es que el recuento llegue a CERO**, no que se vea el efecto
  esperado. `pkill -f` no garantiza el árbol entero.
- **Antes de enunciar la hipótesis grave, descarta la aburrida** («un proceso mío seguía vivo»,
  «lo borré yo hace diez minutos»). Casi siempre ya está medida y el dato está en pantalla; lo
  que falla no es la instrumentación, es que la conclusión llega antes que la lectura.

Corolario del día: de nueve fallos, ninguno se arregló añadiendo una medición nueva. Todos
tenían el dato delante. Y los dos únicos que se escaparon del todo fueron **los dos que nadie
revisó** — no se arregla con más disciplina, se arregla con que mire otro.

Ver [[push-que-falla-por-red-imprime-everything-up-to-date-al-final]] ·
[[semaforo-que-envuelve-un-comando-que-vuelve-a-pedirle-slot-se-interbloquea]].
