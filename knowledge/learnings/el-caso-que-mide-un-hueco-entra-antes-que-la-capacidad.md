---
title: el caso que mide un hueco tiene que entrar ANTES que la capacidad que lo cierra
date: 2026-07-30
source: claude-code-session
tags: [testing, evals, metricas, agh]
---

Un caso de test que **nace verde** no distingue «la capacidad funciona» de «el caso está mal
escrito»: pasa igual en los dos mundos. Solo tiene valor el que nace **rojo** y vira a verde
cuando llega la capacidad — ahí queda verificado en las dos direcciones sin trabajo extra.

Corolario de secuenciación, que es lo caro de descubrir tarde: si el caso mide un hueco que
una PR va a cerrar, **el caso va en una PR ANTERIOR**, no en la misma ni después. Caso real
(AGH #697/#689): al eje `query` le faltaba el caso de `threads.open`; si hubiera entrado
después del prompt que lo cablea, habría nacido verde y no habría probado nada. Se metió
antes, rojo, y con el motivo bueno visible (`clarify`: el modelo entiende la pregunta y no
tiene dónde rutarla).

Vale también al revés: si te encuentras un caso que nació verde, no lo des por bueno —
rómpelo a propósito una vez para ver si es capaz de fallar. Ver
[[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[test-verde-puede-codificar-el-bug-como-esperado]] · [[agh-iberica]]
