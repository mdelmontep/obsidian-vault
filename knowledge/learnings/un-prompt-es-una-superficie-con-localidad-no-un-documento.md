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
Poner `"client":"Odeon"` como ejemplo hizo que una consulta se emitiera como *write*:
```
got {"kind":"write","writes":[{"kind":"client.detail","fields":{"args":{"client":"Odeon"}}}]}
```
1/25. No es «peor routing»: es otra categoría — una lectura inocente entrando en el camino de
confirmación. Tercera reincidencia de la misma causa en ese repo. Los ejemplos van en prosa;
las declaraciones de esquema (`"campo":"<placeholder>"`) sí pueden llevar comillas.

**3 · El ejemplo que elijas compite con los casos vecinos.** Un ejemplo de superficie casi
idéntica a otra pregunta («¿qué tengo en cada cliente?» vs «qué tengo con el cliente X») tira
del vecino: 96 % → 48 % en el vecino. Y no siempre hay salida: allí, toda redacción fuerte
para comprar la capacidad costaba el vecino, y toda redacción suave no compraba nada.
