---
title: lo que un barrido omite no puede darse por recuperado
date: 2026-07-27
source: claude-code-session
tags: [observabilidad, monitorizacion, crons, facturaia, alertas]
---

Un barrido de salud que (a) emite alertas de lo que ve en rojo y (b) resuelve las
abiertas que **no** ve, no puede empezar a saltarse fuentes por coste sin tocar
(b). Ausente-porque-no-se-mira no es recuperada.

Caso TuFacturaIA 2026-07-26. Para recortar CPU tras el incidente de la base, el
`system-health-sweep` pasó a ejecutar el colector caro (cuotas por org) una vez
por hora en vez de cada 10 minutos. El bucle de resolución siguió comparando
contra "lo que salió rojo en ESTE barrido", así que en 5 de cada 6 barridos daba
por recuperadas todas las alertas de cuota, y al reabrirlas a la hora siguiente
**volvía a emailear** — la idempotencia de email es de 5 minutos. El ahorro de
CPU abrió un agujero peor que el que cerró: una org al 100% de cuota aparecía
resuelta y el equipo recibía la misma alerta cada hora.

Cómo se cierra:

- Cada colector declara qué tipos de alerta emite, y el barrido que lo omite
  **excluye esos tipos** de la resolución.
- Ponerlo en el TIPO, no en un comentario: marcar un colector como caro debe
  obligar a declarar sus tipos (unión discriminada), o el siguiente que se añada
  repetirá el fallo en silencio.
- Devolver el conteo de lo no evaluado en el resumen del cron
  (`noEvaluadasIntactas`), para que se vea que se omitió a propósito.
- Al meter una condición de "esta vez no mires X" en un ciclo, buscar SIEMPRE el
  otro lado del ciclo: quien cierra, apaga, purga o resuelve basándose en la
  ausencia.

Ver [[vigilar-cuesta-cpu-y-puede-costar-mas-que-trabajar]] · [[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]]
