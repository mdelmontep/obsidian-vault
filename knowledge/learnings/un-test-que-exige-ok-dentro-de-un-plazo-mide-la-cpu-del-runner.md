---
title: un test que exige «ok» dentro de un plazo de reloj mide la cpu del runner
date: 2026-09-14
source: agh-iberica
tags: [testing, ci, flaky, concurrencia]
---
Un test de **cupo/cola** que además exige que todas las tareas acaben `ok` dentro de un `timeoutMs` real depende del reloj, aunque su comentario diga lo contrario.

- **Local (10 núcleos):** verde, y siguió verde con la CPU saturada con `yes`.
- **Actions (2 vCPU, todas las suites a la vez):** las últimas de la cola agotan el plazo y el test sale rojo. Las duraciones del test (1.030 y 2.015 ms) coinciden exactamente con los plazos: esa es la firma.

Caso: agh-iberica #1738, `extract-isolated.test.ts`, 5 y 10 extracciones con 1–2 s.

Fix:
- En los tests que miden un **límite** (cupo, tope de cola), el plazo no puede ser alcanzable: 60 s, con el timeout del test por encima.
- El plazo se prueba en su propio test, en la dirección segura: un plazo diminuto siempre pierde.
- Aserción que enseñe el valor (`toEqual(["ok",…])`), no `every(...) === true`.
- Comprobar con mutación que el test sigue discriminando el límite.

No reproducirlo en local no descarta nada: basta con quitar la dependencia.
