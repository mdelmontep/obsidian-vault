---
title: detector de salud por ausencia larga no ve un cuelgue con cola pendiente
date: 2026-08-14
source: claude-code-session
tags: [ops, health-check, workers]
---

Un watchdog que dispara por «N horas sin actividad» (p. ej. 20 h sin claims) deja
un punto ciego enorme: un worker colgado CON trabajo en cola es detectable en
minutos — hay items `pendiente` envejeciendo y cero consumo — pero el umbral de
ausencia lo tapa durante horas. Y «contenedor `running`» no prueba nada: el
proceso puede estar wedged con Docker feliz.

La señal correcta es relativa a la cola: items pendientes con más de ~45 min y
ningún claim desde que existen → incidencia, sin esperar al umbral absoluto.
Caso real: marketing-runner de TuFacturaIA, 7 h colgado con 5 runs en cola y
`runner-salud` callado (issue #1771). Emparenta con
[[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]].
