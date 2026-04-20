---
title: supabase self-hosted — vector store para RAG
date: 2026-04-20
source: claude-md-migration
tags: [supabase, rag, pgvector, n8n]
---

# Supabase self-hosted (vector store para RAG)

- Schema estándar LangChain: tabla `documents` con columnas `id`, `content`, `metadata` (jsonb), `embedding` (vector 1536)
- Requiere extensión `pgvector` habilitada (`create extension if not exists vector`)
- Función `match_documents(query_embedding, match_count, filter)` — la que usa n8n para búsquedas por similitud coseno
- Índice `ivfflat` con `lists = 100` para rendimiento en búsquedas vectoriales
- En n8n se conecta vía nodo **Supabase Vector Store** (no Postgres directo) — necesita `SUPABASE_URL` (interno: `http://supabase-kong:8000`) + `SERVICE_ROLE_KEY`
- **Google Service Accounts y política de org**: orgs Workspace modernas aplican `iam.disableServiceAccountKeyCreation` por defecto. Antes de proponer SA al cliente, verificar que tenemos rol `orgpolicy.policyAdmin` o que el cliente puede hacer el override. Si no, OAuth2 como fallback
