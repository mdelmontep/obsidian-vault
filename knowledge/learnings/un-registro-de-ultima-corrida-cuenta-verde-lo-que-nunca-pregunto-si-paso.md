---
title: un registro de «última corrida» cuenta verde lo que nunca preguntó si pasó
date: 2026-08-14
source: claude-code-session
tags: [harness, gates, loop, metricas, fallo-silencioso, tucrmia]
---
Todo arnés acaba teniendo un registro de «cuándo se comprobó esto por última vez»
(`verificaciones.json`, `recorridos.json`, una tabla de `last_run`). El campo del resultado
suele ser **prosa libre**, y el contador sólo mira que no esté vacío.

Efecto: una corrida **roja** cuenta igual que una verde, con la única condición de que alguien
escriba la crónica del fallo — que es justo lo que hace bien quien encuentra un bug. Caso real
(TuCRMIA, 14-ago): dos entradas cuyo texto empieza por «ROJO — la importación no escribe ni una
ficha» y «no ejercible (parcial)» contaban como recorridos **cubiertos**.

Las condiciones que sí suele haber —¿existe?, ¿es reciente?, ¿sigue probando el código de hoy?—
son todas sobre la VIGENCIA, ninguna sobre el VEREDICTO.

**Fix**: un booleano explícito (`verde: true|false`) y **la ausencia cuenta rojo**. Un campo que
sólo penaliza cuando alguien se acuerda de ponerlo a `false` es una casilla marcada a ojo. Y no
se deduce de la prosa: la palabra «verde» aparece dentro de «la primera mitad salió verde».
Endurecer una métrica así SUBE el número — por eso no choca con la regla de no tocar la meta.

Ver [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[ejecucion-en-verde-no-prueba-el-efecto]]
