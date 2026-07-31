---
title: un checker que se pone rojo por la razón equivocada es peor que no tenerlo
date: 2026-07-31
source: claude-code-session
tags: [testing, e2e, gate, verificacion, metodo]
---
Complemento del gemelo conocido ("un checker que no puede ponerse rojo no es un checker").
Este SÍ se pone rojo, y por eso es peor: da una señal falsa que se aprende a ignorar.

Caso: `E2E_BASE_URL` apuntaba a un puerto sin nada escuchando y Playwright no levanta el
servidor. Cada spec agotaba su timeout de navegación y la tanda acababa en "9 de 13 rojos"
tras media hora. Eso se lee como "el código está roto", así que nadie miraba los rojos
concretos, y así llevaba meses: el gate de cierre sacó la dimensión `smoke` en reservas en
**3 de los últimos 8 cierres** por esta causa.

Regla: **una precondición del entorno tiene que fallar en el arranque, en claro, no a través
de los asertos**. Una comprobación de tres líneas al principio del setup ("¿hay alguien
escuchando?") con un mensaje que diga qué levantar. Si la precondición no se cumple, el
checker no debe correr: debe abortar diciendo por qué.

Y al arreglarlo, mide antes de acusar: la primera tanda concluyente destapó 8 rojos, de los
que 2 eran contención de CPU (pasan aislados) y 1 era **preexistente**, comprobado
levantando un worktree del commit anterior y viéndolo fallar igual. Sin esa comparación, los
8 se le habrían colgado al cambio más reciente. Caso real: FacturaIA, `qa-035`.
