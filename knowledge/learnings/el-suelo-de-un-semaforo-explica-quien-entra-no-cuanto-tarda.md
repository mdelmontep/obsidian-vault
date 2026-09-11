---
title: el suelo de un semáforo explica quién entra, no cuánto tarda
date: 2026-09-11
source: facturaia
tags: [rendimiento, gates, medicion, atribucion]
---
Un pre-push de 70 min con la máquina a load 17. Cuatro explicaciones, tres caídas:
contención de CPU, el suelo `running < MIN` de `fia-gate` (la línea 260 admite sin mirar
`vm.loadavg`), y «no hay cola, la espera máxima fue 1 s».

**Esa tercera era mía y era falsa: medí la cola en el lado equivocado.** El semáforo
envuelve DOS capas distintas y solo miré una. Los segmentos internos del pre-push entran
con el `KIND` por defecto (`cpu`) y no tienen exclusión: 14 segmentos, **1 s** de espera
total. Pero cada comando de la sesión de Claude Code va envuelto con `FIA_GATE_KIND=mem`,
y ahí la línea 259 **sí muerde** — un `mem` no entra si ya hay otro corriendo: 54
segmentos, **219 s**, con un único `git push` esperando **218 s**. Filtré por rama del
repo, que es justo el campo que los segmentos del envoltorio no llevan, y la cola se
volvió invisible.

Doble lección: (1) antes de concluir «no hay cola», comprueba que tu filtro alcanza a
TODAS las capas que piden slot — el envoltorio también hace cola; (2) no sumes los
`Duration` que declaran las herramientas (de 11 etapas, 2 los declaran, y las que más
pesan hacen red y no publican tiempo): mide `running→done`.
Referencia del gate: 398-419 s limpio, 478 s cargado. Tell de vivo: `stat -f %m <log>`.
Ver [[el-suelo-de-carga-de-una-maquina-compartida-no-lo-ponen-las-sesiones]].
