---
title: un background bash io-bound se mata solo sin causa visible — reintentar, no diagnosticar
date: 2026-07-22
source: claude-code-session
tags: [claude-code, run_in_background, evals]
---

Un `run_in_background` de larga duración puede llegar como `killed`/salida vacía SIN contención de
CPU/memoria (visto con `npm run evals:check`, proceso I/O-bound esperando red al modelo, CPU~0%).
Distinto del gotcha de builds paralelos (ahí la causa es real: CPU/mem agotada) — aquí no hay causa
visible, parece un límite del harness sobre cuántos backgrounds concurrentes tolera, agravado por
apilar varios `sleep N && echo done` de "polling" en paralelo con el proceso real.

Fix que funcionó: relanzar el MISMO comando tal cual — a la 2ª/3ª tentativa termina bien. No perder
tiempo diagnosticando la muerte; reintentar primero. Y no lanzar timers de espera si ya vas a recibir
la notificación real del proceso — cada uno de más compite por el mismo límite.

Caso: AGH Ibérica 2026-07-22, evals ×3 de dos PRs (#567/#569), `evals:check` matado 2 veces seguidas.
