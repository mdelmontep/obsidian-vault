---
title: el suelo de un semáforo explica quién entra, no cuánto tarda
date: 2026-09-11
source: facturaia
tags: [rendimiento, gates, medicion, atribucion]
---
Un pre-push de 70 min con la máquina a load 17. Cuatro explicaciones intentadas en una
tarde entre dos sesiones, **las cuatro caídas**: contención de CPU (load real, pero no
causa), el suelo `running < MIN` de `fia-gate` (la línea 260 admite sin mirar
`vm.loadavg` — cierto, y explica quién ENTRA, no cuánto tarda), «no hay cola» (falso), y
«era la cola» (también falso).

Lo que sí quedó medido, y merece la pena por sí solo: **el semáforo envuelve dos capas y
una era invisible.** Los segmentos internos del pre-push entran con el `KIND` por defecto
(`cpu`), sin exclusión: 1 s de espera en 14. El envoltorio de cada comando de sesión va
con `KIND=mem`, donde la línea 259 sí muerde: 219 s en 54. Filtrar por rama del repo no
alcanza al envoltorio, que no lleva ese campo.

**Pero 219 s no explican 70 min, y 218 de esos 219 eran de UN push ajeno a la corrida
lenta.** Medir bien una cosa no la convierte en la causa de la otra: la tentación, después
de encontrar por fin un número real, es colgarle el misterio que tenías abierto.

La hora **sigue sin atribuir**. La sospecha viva: de 11 etapas del pre-push solo 2
declaran `Duration`, y las que más pesan (sincronía de migraciones, `gen:types:check`)
hacen RED sin publicar tiempo. Se mide instrumentando esas etapas, no el semáforo.
Ver [[el-suelo-de-carga-de-una-maquina-compartida-no-lo-ponen-las-sesiones]].
