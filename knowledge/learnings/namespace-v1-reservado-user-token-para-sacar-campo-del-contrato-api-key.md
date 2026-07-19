---
title: namespace /api/v1 reservado a user-token (api_key→404) saca un campo del contrato genérico api_key
date: 2026-07-19
source: claude-code-session
tags: [facturaia, api, mcp, oauth, seguridad]
---
Problema: un integrador externo (api_key `fia_*`) consume el contrato genérico `/api/v1/*`; hay un campo/recurso (`obra_id`, módulo Obras) que NO debe verse por esa vía, blindado por un test de contrato. Pero sí quieres exponerlo al agente MCP (user-token OAuth).

El test de contrato NO prohíbe el recurso en v1: prohíbe que el campo toque el contrato genérico api_key. Vía limpia: **namespace nuevo reservado a user-token**, con guard de 3 capas EN ESTE ORDEN:
1. `principal.kind !== 'user'` (api_key) → **404** (no 403, para no filtrar que el namespace existe), sin tocar BD.
2. sector/módulo ausente → 404 (mismo criterio, no filtrar existencia por org).
3. scope ausente → 403.

Clave: el wrapper NO pasa `requireScope` al middleware genérico (si no, devuelve 403 a api_key ANTES del guard → filtra existencia). El scope se re-valida server-side dentro. Reutiliza funciones puras compartidas web↔v1 para no duplicar query (sin regresión). Añadir tools MCP cambia el hash de `tools-manifest` → el servicio MCP (`autoDeploy=false`) necesita redeploy manual (`compose.deploy`, verificar `/health` count/hash).

Para ESCRITURA el mismo patrón: el wrapper pasa `requireWrite` pero TAMPOCO `requireScope` — así la fase auth deja pasar al api_key (sin 403) y el guard le da 404 primero. Ojo: la escritura MCP suele ir sobre un slice READ ya mergeado; si tu worktree se creó antes de esos merges (y de ramas paralelas), **rebasa sobre origin/main antes del PR** o `git diff` muestra deleciones fantasma y revertirías trabajo ajeno. Ver [[facturaia]].
