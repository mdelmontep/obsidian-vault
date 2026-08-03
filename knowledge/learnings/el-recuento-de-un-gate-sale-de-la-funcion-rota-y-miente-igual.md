---
title: el recuento de un gate sale de la función rota, así que ni el número delata el hueco
date: 2026-08-03
source: claude-code-session tucrmia
tags: [gates, tooling, metodo, tests]
---

Un gate que delimita con `.exec` en vez de `matchAll` **solo mira la primera ocurrencia** del
fichero. Una segunda composición escrita debajo con la protección desactivada es invisible. Lo
que lo hace difícil de ver es que el gate **cuenta usando la misma función**, así que su mensaje
tranquilizador —«1 composición, todas enchufadas»— es tan falso como la comprobación: el número
que debería delatar el hueco lo tapa.

Caso: `G-RL-ENCHUFADO` y `G-S5` sobre el mismo objeto de dependencias. Los dos decían «1
composición» con dos delante, una con `rateLimit: async () => ({ allowed: true })`. Y no se había
visto porque el test que se llamaba «revisa todas las composiciones» las ponía **en dos ficheros**,
que es la disposición en la que el fallo no se manifiesta — el fixture probaba la forma que el
gate sí cazaba.

Reglas:
- El recuento de un gate se comprueba **plantando el caso malo**, no leyéndolo.
- Si dos gates parsean lo mismo, un solo dueño de la delimitación (D9): dos copias divergen.
- Un fixture que reparte el caso en varios ficheros suele estar evitando el caso real.

Ver [[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]] ·
[[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]]
