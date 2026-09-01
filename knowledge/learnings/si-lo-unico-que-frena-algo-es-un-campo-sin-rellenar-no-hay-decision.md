---
title: si lo único que frena algo peligroso es un campo sin rellenar, no hay decisión
date: 2026-09-01
source: facturaia
tags: [diseño, guards, billing]
---
Una barrera que consiste en «ese dato todavía no está puesto» no es una regla: es un descuido que
aguanta. El día que alguien rellene el campo por rutina —crear el precio, poner la env, subir el
límite— la barrera desaparece sin que nadie haya decidido nada ni haya nada que revisar en un diff.

Caso real (1-sep, facturaia #1704): dar de alta un complemento en `borrador` hizo que el checkout
dejara de dar 404 y llegara hasta la comprobación del precio. Lo único que lo frenaba era no tener
`plan_prices` ni `STRIPE_PRICE_ID_*`; con cualquiera de las dos, se cobraba por algo que la UI no
enseña y cuyo recorrido no funciona.

- El fix es una guarda que exprese la decisión (`estado !== 'publicado'` → rechazo) y que vaya
  **antes** de la comprobación accidental, o el test cae en el error equivocado y parece cubierto.
- El test que la mide tiene que rellenar el campo a propósito: con el precio puesto, lo único que
  puede rechazarlo es el estado. Si no, no discrimina.
- Señal para buscarlo: la frase «hoy no puede pasar porque no hay X configurado».
