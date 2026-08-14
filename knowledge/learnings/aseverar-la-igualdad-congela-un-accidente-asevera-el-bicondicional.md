---
title: aseverar la igualdad congela un accidente; asevera el bicondicional
date: 2026-08-14
source: claude-code-session
tags: [tests, invariantes, diseno]
---

Dos pools de frases elegían **siempre el mismo índice** porque compartían clave de hash y tamaño
(medido: 6/6 en el golden y 200/200 en cargas arbitrarias). El candado tentador:

```ts
expect(poolA.length).toBe(poolB.length)   // ← congela un acoplamiento que NADIE ha decidido
```

La historia decía lo contrario: `git show` de su commit fundacional mostraba **dos pools naciendo en
el mismo hunk con tamaños distintos**, y el tercero llegó ocho días después por otro issue. O sea que
el repo ya trata «cuántas variantes tiene un estilo» como decisión **por estilo**.

Fix: aseverar el **bicondicional** — *van en bloque **si y sólo si** comparten tamaño*. Es propiedad
del selector, no de los pools, y **sobrevive a que los tamaños se separen**. Contrafáctico que valida
la decisión: añadir una variante a UN solo pool → **verde a propósito**; el atajo lo habría bloqueado.

🪤 Y la trampa fina: mi mutación para romperlo saló el hash con `variants.length` y salió `SIN VÍCTIMA`
— porque los dos pools **tienen hoy el mismo tamaño**, así que sumaba lo mismo a ambos. El
acoplamiento se cuela hasta en el instrumento que intenta romperlo. Salar por **contenido**, no por
tamaño. Ver [[asevera-la-relacion-no-la-presencia-de-los-tokens]].
