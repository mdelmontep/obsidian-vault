---
title: n8n a Supabase self-hosted Dokploy = REST API por default
date: 2026-05-03
source: claude-code-session
tags: [n8n, supabase, dokploy, networking]
---

Para conectar n8n con Supabase self-hosted en Dokploy: usar **REST API + service_role key**. No intentar Postgres directo via Docker network como primer approach.

## Por qué

En Simarro probamos 4 nombres de network (`dokploy-network`, `supabase-c0ca_default`, `supabase_default`, `simarro-pre0225supabase-ktgdfs_default`) — todos fallaron por DNS o aislamiento entre stacks. REST API funcionó al primer intento.

## Patrón

- HTTP Request node → `https://<subdomain>/rest/v1/<table>`
- Headers: `apikey: <service_role>`, `Authorization: Bearer <service_role>`, `Content-Type: application/json`
- Upsert: `Prefer: resolution=merge-duplicates`
- RPC: `POST /rest/v1/rpc/<function_name>` con body JSON

Postgres directo solo si el caso lo requiere (transacciones multi-tabla, COPY, RLS bypass complejo).
