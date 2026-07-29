---
title: antes de optimizar latencia, mide tu tramo y réstalo del e2e
date: 2026-07-29
source: claude-code-session
tags: [observabilidad, langfuse, latencia, voz, retell]
---
Un p50 e2e alto en voz (aquí 3,8 s, objetivo conversacional ~1,5 s) invita a tocar el prompt o el brain. Antes de eso, **parte el número en dos**: tu tramo medido y el resto por diferencia.

Caso real (agh-iberica #591): las trazas traían `metadata.latencyMs` por turno → nuestro tramo **p50 1.038 ms** contra los 3.780 ms que medía Retell. **El 72% del p50 se iba fuera del código propio** (STT + TTS + red), y el 27% restante ya incluía la llamada al gateway del LLM. Conclusión: optimizar el brain no arreglaba esa latencia — dato que cambió el issue, no que lo confirmó.

Dos cosas que conviene saber antes de prometer un desglose fino:
- **Un `EVENT` por turno no permite desglosar nada.** Si la instrumentación no emite **spans/generations** (con `start_time`/`end_time`), no existe el tramo «brain» separado del «LLM»: no es mirar mejor, es que no se emite. Instrumentar spans es trabajo previo, no parte del análisis.
- **Compara canales**: el mismo brain daba p50 ~1 s en voz y 2-3,4 s en WhatsApp (máx 13,3 s un día malo). Un canal mucho peor que otro con el mismo núcleo señala el canal, no el núcleo.

Con Langfuse self-hosted, la vía práctica es su **ClickHouse** (`traces` / `observations`), no la API: `quantile(0.5)(toFloat64OrNull(metadata['latencyMs']))` agrupado por `intent` da el desglose en una consulta.
