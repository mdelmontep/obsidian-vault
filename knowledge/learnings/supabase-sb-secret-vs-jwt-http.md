---
title: supabase sb_secret no funciona como bearer token en http directo
date: 2026-04-28
source: claude-code-session
tags: [supabase, n8n, auth, api]
---

El nuevo formato `sb_secret_*` de Supabase funciona con el SDK JS (lo convierte internamente a JWT), pero NO como Bearer token en peticiones HTTP directas (n8n HTTP Request, curl, fetch manual).

**Síntoma**: 401 Unauthorized en n8n o cualquier cliente HTTP que use la key directamente.

**Fix**: usar el JWT legacy (`eyJ...`) para HTTP directo. Obtenerlo en Supabase → Settings → API → Legacy anon/service_role keys. Verificar que "Legacy JWT" esté activo (toggle visible en esa misma página).

**Patrón seguro para n8n**: guardar como `$env.SUPABASE_SERVICE_ROLE_KEY` (JWT), nunca hardcodeado en jsCode. Requiere `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` en el compose.
