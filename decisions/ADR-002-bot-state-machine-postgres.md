---
title: ADR-002 — State machine bot WhatsApp en Postgres chat_state
date: 2026-05-18
status: accepted
tags: [adr, facturaia, bot, n8n]
---

## Contexto
Bot WhatsApp necesitaba contexto estructurado entre turnos: UUIDs de `last_listado`, `draft` actual, idempotencia doble-tap. Memoria LangChain (`n8n_chat_histories`) guarda transcript pero no estado tipado.

## Opciones consideradas
- **A — Solo LangChain memory** — re-parsear lista desde transcript. LLM olvida UUIDs, sin idempotencia ni TTL granular.
- **B — Redis externo** — TTL nativo rápido. Container nuevo en Dokploy, sin observabilidad SQL.
- **C — Tabla `chat_state` Postgres Supabase** — PK `(phone_user, phone_receptor, org_id)`, JSONB + `expires_at`, RLS service-role.

## Decisión
**C**, porque persiste tras restart n8n, accesible desde múltiples nodos vía REST, observable con SQL, sin nueva dependencia, race guard + sanitize server-side en un solo punto.

## Consecuencias
Endpoint `/api/internal/voice/chat-state` queda contrato estable n8n↔backend. TTL diferencial por `current_view` server-side. Cron `chat-state-purge` diario. Migrar a Redis si futura latencia lo exige sería >1 día.
