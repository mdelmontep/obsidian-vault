---
title: una etiqueta nacida de un caso concreto sobrevive a su contexto y acaba midiendo otra cosa
date: 2026-08-01
source: claude-code-session
tags: [observabilidad, testing, metricas, agh]
---
Tres casos el mismo día, todos con la misma forma: un nombre correcto cuando se escribió, leído después como si midiera lo que su nombre sugiere.

- `intent: interpretation.kind` medía **lo que el LLM dijo que era el turno**, no el resultado. Su barra «clarify=32,8%» se leía como «cuántas veces no entendió»: agregaba 4 conductas y excluía 5 caminos que también preguntaban, incluido el bueno (el agente pidiendo el dato que falta).
- `expect(result.signals).toBeUndefined()` en un test titulado «no emite ESTA señal»: se pone **rojo** al añadir cualquier señal de otra familia, y el rojo llega a quien no tiene contexto.
- Un arnés A/B con `if (out.kind === "write") fallos++` cableado al caso que se investigaba esa noche, con la columna titulada «fallos»: con otro turno presentó **100% de aciertos como 100% de fallos**.

Regla: **toda etiqueta que se muestre a un humano declara su criterio en el mismo sitio donde se muestra.** Y si el criterio depende del caso, se pasa como argumento obligatorio que mata el proceso si falta — no un default.

Corolario de detección: los tests unitarios no lo ven **por construcción** (cubren la estadística, no el criterio). Los tres salieron al ejercitar el camino real: uno recorriendo los 9 caminos del brain, otro añadiendo una señal nueva, el tercero con la primera corrida real de llamadas.

Corolario medido: una cifra que se escribe **a mano** en cada entrega falla en las **dos** direcciones el mismo día — `59 ficheros` cuando eran 49 (un proyecto sumado dos veces) y `20` cuando eran 39 (un `ls test/*.pg.test.ts` que no bajaba a los subdirectorios). Si un número se pega en una PR, que lo **emita la herramienta**.

Primo cercano: [[banner-cuenta-pares-vs-pestana-cuenta-entidades-misma-palabra]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]]
