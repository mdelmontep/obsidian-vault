---
title: un prompt es una superficie con localidad — dónde pones la regla y qué ejemplo usas cambian el resultado
date: 2026-08-04
source: claude-code-session
tags: [llm, prompt, evals, agh]
---
Dos efectos medidos el mismo día (AGH, n=25 entrelazado por variante), los dos invisibles
leyendo el diff:

**1 · La posición no es cosmética.** La MISMA regla dentro de la viñeta de su target se
aplica (25/25); movida a una nota de frontera **posterior** a la viñeta, no se aplica **en
absoluto** (0/12). Si añades una regla de routing, va DENTRO de su viñeta.

**2 · Un literal JSON con valor concreto en una viñeta de READ sangra al esquema de WRITE.**
Poner `"client":"Odeon"` como ejemplo hizo que una consulta se emitiera como *write*
(`{"kind":"write","writes":[{"kind":"client.detail","fields":{"args":{…}}}]}`): 1/25. No es «peor routing»: es otra categoría — una lectura inocente entrando en el camino de
confirmación. Tercera reincidencia de la misma causa en ese repo. Los ejemplos van en prosa;
las declaraciones de esquema (`"campo":"<placeholder>"`) sí pueden llevar comillas.

**3 · El ejemplo que elijas compite con los casos vecinos.** Un ejemplo de superficie casi
idéntica a otra pregunta («¿qué tengo en cada cliente?» vs «qué tengo con el cliente X») tira
del vecino: 96 % → 48 % en el vecino. Y no siempre hay salida: allí, toda redacción fuerte
para comprar la capacidad costaba el vecino, y toda redacción suave no compraba nada.

**4 · QUITAR un bloque grande mueve reglas que no has tocado** (4-ago, n=25 por lado). Sacar el
catálogo de lecturas del prompt (−2.483 tok, −17,8 %) degradó dos reglas lejanas: un guardarraíl de
anáfora (15/25 → 1/25) y un batch de tres writes que empezó a repetir el sobre dentro de `fields`. **No
era el modo `strict`** —contrafáctico: 1/25 vs 4/25, indistinguible—: era la posición de todo lo que
venía después. Al mover o quitar un bloque, presupuesta el contraste de las reglas LEJANAS, que son
las que se rompen. Y cuando la regla degradada sea decidible, arréglala en código:
[[una-regla-de-prompt-que-el-modelo-cumple-a-medias-suele-ser-decidible-en-codigo]].

**5 · No es solo DÓNDE está la regla: es A QUÉ la atas** (9-sep, Centro Elphis, caso 06). La regla
correcta ya estaba escrita —«si te hace una pregunta, RESPÓNDELA»— pero al final del paso 4 y atada
a un objeto: «nunca ignores lo que te pregunta *para insistir con el nombre*». El fallo ocurría en el
paso 3, cuyo texto ordena lo contrario («dedícale un turno a entenderlo **antes de pedirle nada**») y
**sugiere de ejemplo la frase exacta** que salía en el transcript. La regla se cumplía: el agente no
ignoraba preguntas por el nombre. Ignoraba preguntas por otra cosa. Al auditar un prompt no basta con
buscar si la regla existe: mira a qué objeto está anclada y si ese es el que la incumple.
