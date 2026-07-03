---
title: un hilo con respuestas erróneas acumuladas ancla al llm aunque el tool dé el dato bueno
date: 2026-07-03
source: claude-code-session
tags: [llm, agentes, memoria, copiloto, whatsapp]
---
Si el historial de conversación acumula N copias de una respuesta errónea
(p.ej. QA iterativo contra un bot con memoria), el modelo la REPITE calcada
aunque el tool del turno devuelva los datos correctos — el anclaje del
historial pesa más que el tool result. Caso real FacturaIA: hilo WhatsApp con
100 mensajes repitiendo "2,100.20€ (2T)"; el mismo endpoint con hilo limpio
respondía perfecto (dual 2T+3T en español).
Fixes (ambos): (1) regla en el bloque POR TURNO del system prompt — "los
resultados de tools de ESTE turno prevalecen sobre cualquier cifra de
mensajes anteriores, incluidos los tuyos" (PR #681); (2) reset del hilo
envenenado (delete de sus mensajes).
Regla de QA: al iterar fixes contra un agente con memoria, verifica con hilo
LIMPIO o resetea entre rondas — si no, cada prueba refuerza el error anterior
y los fixes parecen no aplicar.
