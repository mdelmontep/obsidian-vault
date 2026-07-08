---
title: en confirmaciones de voz, no fusiones un batch multi-write en una sola frase hablada si cada línea lleva verificación propia
date: 2026-07-08
source: claude-code-session
tags: [retell, voz, tts, agh-iberica]
---

Tentador para sonar más natural en voz: cuando hay varios writes en un batch, unirlos en una
frase fluida ("vale, voy a hacer esto: X y esto: Y. ¿te lo confirmo?") en vez de una línea por
write. Rompe si cada línea lleva su propio dato-crítico dosificado (deletreo de un nombre nuevo,
lectura pausada de un email) — la fusión colapsa esa dosificación por-línea en un batch sin forma
de distinguir a qué write pertenece cada deletreo.

Regla: el fraseo conversacional (envoltorio) se aplica al caso de UN SOLO write; un batch de
varios mantiene el formato por-línea de siempre. La "naturalidad" del envoltorio nunca debe tocar
el contenido determinista por-línea — la frontera ya existente en el código (tono = wrapper, nunca
los hechos) también aplica a la estructura de líneas, no solo al texto de cada una.

Caso real AGH (#202 vs #201): probar la fusión rompió el test de dosificación de deletreo (2
writes, cada uno con su "se escribe X" propio) — se revirtió antes de mergear.
