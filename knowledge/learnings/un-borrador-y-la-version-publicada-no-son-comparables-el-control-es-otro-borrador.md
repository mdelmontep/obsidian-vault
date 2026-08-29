---
title: un borrador y la versión publicada no son comparables, el control es otro borrador
date: 2026-08-29
source: centro-elphis
tags: [retell, medicion, agentes-de-voz, metodo]
---
Midiendo v30-v36 del agente de voz contra la v29 **publicada**, un caso de la suite (línea
ininteligible) caía del 83 % al 57-62 % en **seis** combinaciones de parches distintas — incluida una
que solo tocaba una línea del global_prompt. Seis mecanismos distintos con el mismo efecto es la señal
de que el efecto no lo causan los parches.

Prueba que lo zanja: crear un borrador **sin ningún parche**, byte a byte idéntico a la publicada, y
correr la misma suite. Dio 64 %, no 83 %. El sesgo lo aportaba la comparación borrador↔publicada, no
el cambio.

- Toda medida de un borrador se compara contra **otro borrador no-op**, nunca contra lo que sirve el número.
- Cuesta una llamada a `create-agent-version` y ahorra horas: aquí contaminó cuatro y me hizo
  descartar el único parche que sí mejoraba.
- Corolario: un "empeora" que aparece igual en variantes que no comparten causa es un artefacto del
  arnés hasta que se demuestre lo contrario.

Ver [[regresion-en-suite-tras-bump-verificar-contra-main-limpio-antes-atribuir]] y
[[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]].
