---
title: voz streaming (retell) — dedup de turnos por firma del transcript, pero re-emitir la voz sobre el response_id actual
date: 2026-07-04
source: claude-code-session
tags: [retell, voz, dedup, agentes-codigo, agh-iberica]
---
Retell (custom-LLM WS) reemite el MISMO turno (barge-in sin palabras nuevas, resend del keepalive con `auto_reconnect`, un «sí,» corto) con `response_id` NUEVO pero transcript idéntico → si corres el pipeline por evento, los efectos secundarios se duplican (push cross-canal, writes HITL).

- **Clave de dedup = firma sha256 del transcript COMPLETO**, no el `response_id` ni el último utterance. El transcript crece monótono → un turno posterior genuino difiere; un reemit colisiona. Barge-in-safe y «sí»-safe (dos «sí» que confirman propuestas distintas tienen transcript creciente entre medias).
- **Gotcha (casi bug real):** NO descartes el turno entero. Retell aplica *latest-wins* → una respuesta al `response_id` superado se descarta → el caller se queda MUDO justo en el caso que arreglas. Fix: cachea el texto de voz por turno y **re-emítelo sobre el `response_id` ACTUAL**; el brain y el push corren 1×.
- **Retry-safe:** no marques «visto» hasta que el turno complete OK; un fallo transitorio debe dejar que el reemit reintente (`finally` libera la reserva in-flight; el `has`+`add` síncrono antes del `await` protege la race entre eventos concurrentes del mismo socket).
- Un handler por conexión = por llamada → dedup en memoria, sin durabilidad cross-proceso (a diferencia del dedup de webhooks WhatsApp por wamid en Postgres, que sí cruza procesos).
- Asunción a validar con payload real capturado (túnel a Retell): si el reemit reusa el mismo id o trae uno nuevo — el diseño cubre ambos.

Relacionado: [[hash-dedup-necesita-indice-secuencial-para-movimientos-repetidos]] · [[dedup-key-no-debe-incluir-contenido-volatil]] · [[copiloto-turn-lock-concurrent-llm-calls]]
