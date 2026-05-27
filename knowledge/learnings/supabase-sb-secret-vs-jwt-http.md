---
title: supabase sb_secret requiere header apikey en http directo (no solo bearer)
date: 2026-04-28
updated: 2026-05-27
source: claude-code-session
tags: [supabase, n8n, auth, api]
---

`sb_secret_*` NO es un JWT — no pasa la validación `Invalid Compact JWS` si se manda solo como `Authorization: Bearer`.

**Fix (validado 2026-05-27)**: añadir header `apikey: <sb_secret_key>` (igual que `Authorization: Bearer <key>`). Con ambos headers → 200. Solo Bearer → 400/403. Aplica a Storage REST, PostgREST, y cualquier endpoint Supabase por HTTP directo.

**NO requiere JWT legacy** — `sb_secret_*` funciona en HTTP directo siempre que `apikey` esté presente.

**Patrón seguro para n8n**: en `additionalHeaders` del HTTP Request node (o jsCode con `this.helpers.httpRequest`), incluir `{ apikey: SUPABASE_KEY, Authorization: 'Bearer ' + SUPABASE_KEY }`. Guardar como `$env.SUPABASE_SERVICE_ROLE_KEY`.

**Síntoma original**: `{"statusCode":"403","error":"Unauthorized","message":"Invalid Compact JWS"}` → falta header `apikey`.
