---
title: turn lock por hilo para agentes llm con historial persistido
date: 2026-06-29
source: claude-code-session
tags: [copiloto, llm, concurrencia, redis]
---

Dos peticiones simultáneas al mismo thread (doble-clic, reintento de red, webhook n8n con timeout) leen el mismo historial antes de que ninguna haya escrito su respuesta. Ambas llaman al LLM, ambas persisten → mensajes intercalados, tool_use huérfanos, historial corrupto.

**Fix**: mutex por `threadId` antes del runner, release en `finally`.
- Redis disponible: `SET lock:copiloto:turn:{id} 1 NX PX 90000` (atómico, auto-expira si el proceso muere).
- Sin Redis: `Map<string, expiry>` en memoria (cubre réplica única y doble-clic mismo browser).
- TTL 90s = red de seguridad; el release explícito en finally es el camino normal.
- WhatsApp: devolver 200 `{ reply, error: 'turn_in_progress' }` en vez de 409 (n8n no gestiona 4xx del webhook).

Archivos: `src/lib/rate-limit.ts` (`acquireLock`/`releaseLock`), `src/lib/copiloto/turn-lock.ts`, ambos endpoints copiloto.
