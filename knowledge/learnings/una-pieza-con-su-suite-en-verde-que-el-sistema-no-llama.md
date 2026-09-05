---
title: una pieza con su suite en verde que el sistema no llama
date: 2026-09-05
source: mandadm
tags: [tests, verificacion, arquitectura, subagentes]
---

Seis defectos distintos de una misma horda, todos con sus tests en verde, resultaron ser **el mismo**:
el test ejercita la pieza y **nadie comprueba que el sistema la llame**. El worker no importaba cinco
de sus jobs (tokens sin renovar, retención sin correr, alertas sin llegar); un `href` apuntaba a una
ruta inexistente; una acción se probaba por la función interna y no por la acción; la lista de
fixtures estaba a mano y se había quedado en 26 de 31.

Un test unitario prueba que la pieza *funciona*, nunca que esté *enchufada*. Y la mutación no lo
caza: borras la pieza y la suite sigue verde porque la suite la importa directamente.

**El candado tiene que descubrir, no enumerar.** Recorrer el árbol (`readdirSync` de los fixtures,
walk de `app/` siguiendo cada `href` hasta su `route.ts`, leer del registro real del worker qué jobs
declara) en vez de leer una lista que alguien tiene que acordarse de actualizar. Verificar el candado
añadiendo la pieza nueva sin registrarla: si sigue verde, enumera.

Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]] ·
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[un-gate-que-enumera-desde-el-indice-de-git-no-ve-el-fichero-nuevo]]
