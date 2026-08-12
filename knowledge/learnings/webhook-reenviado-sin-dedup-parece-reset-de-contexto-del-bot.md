---
title: un webhook de mensajería reenviado sin dedup por message.id parece un reset de contexto del bot
date: 2026-08-12
source: claude-code-session
tags: [n8n, kommo, whatsapp, webhooks, idempotency]
---
Chatbot de WhatsApp (n8n + Kommo + AI Agent): en medio de una conversación avanzada, el bot de
repente saludaba de nuevo ("Hola, soy Ana...") como si empezara de cero. Parecía memoria/sesión del
LLM corrompida.

Causa real, confirmada con los logs de ejecución: Kommo/WABA reenvió el mismo evento
`message[add][0][id]` ~70s después del original. El workflow no dedupeaba por ese id — solo tenía
Redis para agrupar mensajes fragmentados por `lead_id` (debounce), nada para descartar un evento ya
procesado. El "Hola" duplicado se coló como turno nuevo, y por pura coincidencia de timing su
respuesta aterrizó justo después del turno real del cliente, pareciendo que el bot había perdido el
hilo.

Diagnóstico rápido: antes de sospechar de la memoria del LLM (Postgres Chat Memory, session id),
comparar `message[add][0][id]` + `created_at` del turno "raro" contra los mensajes anteriores de la
misma conversación — si coinciden con uno ya procesado, es reenvío, no reset.

Fix: guard de idempotencia con el mismo Redis que ya usa el workflow — GET por `message.id` antes de
procesar; si existe, `NoOp` y cortar; si no, `SET` con TTL corto y seguir. No hace falta SETNX
atómico si el reenvío llega minutos después (no hay carrera real entre el original y el duplicado).
