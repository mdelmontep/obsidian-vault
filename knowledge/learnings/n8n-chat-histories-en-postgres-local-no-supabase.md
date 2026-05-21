---
title: n8n_chat_histories vive en Postgres local del n8n Dokploy, no en Supabase del proyecto
date: 2026-05-21
source: claude-code-session
tags: [n8n, langchain, dokploy, supabase, smoke]
---

n8n `@n8n/n8n-nodes-langchain.memoryPostgresChat` y nodos Postgres que leen
`n8n_chat_histories` usan la credential "Postgres TufacturaIA" — apunta al
Postgres **interno del stack n8n** en Dokploy, NO al Supabase del proyecto.

Síntoma: `SELECT * FROM n8n_chat_histories` en Supabase MCP devuelve
`relation does not exist`, pero el nodo Postgres del workflow ve filas
(comprobado vía `cnt: 68` en exec data del `Check Sesion Voz Activa`).

Implicaciones smoke: para limpiar memoria conversacional del LLM no sirve
Supabase MCP. Opciones: (a) workflow temporal n8n con `DELETE` via misma
credential, (b) SSH al contenedor Dokploy + psql interno, (c) hack temporal
en IF condition para bypassar `Tiene Sesion?` (más seguro, reversible).

Ver también [[smoke-multi-org-whatsapp-clean-state]].
