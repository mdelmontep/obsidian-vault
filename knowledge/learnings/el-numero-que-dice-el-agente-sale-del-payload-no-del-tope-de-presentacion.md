---
title: el número que dice el agente sale del payload, no del literal ni del tope de presentación
date: 2026-09-09
source: simarro
tags: [voice, prompt-engineering, n8n, retell]
---

Un agente que enseña resultados suele decir cuántos tiene. Ese número se rompe en **dos capas distintas**, y hay que mirar las dos (Simarro, 9-sep-2026, con 3 viviendas en Villaviciosa):

- **Código**: el nodo que formatea la voz recitaba dos fichas y llevaba el literal `'Tengo dos'` fijo, aunque el payload traía `count: 2, total_in_catalog: 3`. El dato verdadero ya estaba; lo que se locutaba era el número de las que se iban a describir.
- **Prompt**: la instrucción del nodo decía "si reformulas: máximo 2 viviendas". El LLM aplicó ese tope también al **conteo** y dijo "tengo dos opciones" con tres en cartera. Preguntado ("¿cuántas has dicho?"), respondió tres.

Regla: el conteo se calcula del payload (con cardinales hablados, no cifras) y el prompt debe decir **de qué** es el tope — "máximo 2 viviendas que DESCRIBES, no el número que dices tener; el conteo del `message` se lee tal cual". Un tope escrito sin decir su unidad se aplica a la primera magnitud que el modelo tenga a mano.
