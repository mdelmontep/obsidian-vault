---
title: un catch best-effort sin señal persistente hace indistinguible el fallo del no-disparo
date: 2026-09-02
source: facturaia
tags: [llm, observabilidad, ocr, degradacion]
---
El reintento escalado del OCR (facturaia #2385) salió con gate verde, tests y 25/25 evals — y muerto en
prod: gpt-5.2 rechaza `max_tokens` con un 400 («Use 'max_completion_tokens'») y el `catch` best-effort
se quedaba el resultado barato con solo un `console.warn`. Tres verdes falsos a la vez: los tests
mockean el fetch, el arnés de evals comparte `buildOcrRequestBody` pero no `route.ts` (nunca ejercita
el disparo), y el propio fallback hace su trabajo — el sistema «funciona» sin la feature. Lo destapó un
smoke real: 3 subidas con 1 fila de audit donde tocaban 2.
Fix y patrón (#2388):
- Un parámetro nuevo hacia una API externa se valida con UNA llamada real barata ANTES de cablearlo
  (curl de 50 tokens); el contrato del proveedor cambia entre familias de modelo.
- Todo camino degradado escribe una señal PERSISTENTE (anomalía, fila de audit), no solo log efímero:
  «degradar es degrada + AVISA». Sin ella, «falló siempre» y «nunca hizo falta» son la misma medición.
