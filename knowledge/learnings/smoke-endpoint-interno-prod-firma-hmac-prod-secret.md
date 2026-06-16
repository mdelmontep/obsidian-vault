---
title: smokear un endpoint /api/internal/* en prod exige firmar hmac con el secreto de prod
date: 2026-06-16
source: claude-code-session
tags: [facturaia, n8n, hmac, smoke, seguridad]
---

Para smokear server-to-server un endpoint `/api/internal/*` (auth HMAC v2) contra prod:

- **Payload firmado**: `${t}.${METHOD}.${pathWithSearch}.${sha256_hex(body)}` → `hmac_sha256_hex(secret, payload)`. Header: `X-Service-Signature: t=<unix>,v1=<hex>`. Tolerancia ±5 min. `pathWithSearch` = path + query (sin host). Body firmado = body enviado, byte a byte.
- **El secreto es el de PROD** (`FACTURAIA_SIGNING_SECRET` en Dokploy env del compose / 1Password), NO el de `.env.local` (ese es dev) → si te equivocas, `401 {reason:"bad_signature"}` silencioso, fácil de confundir con bug de código.
- **Mutaciones de prod**: el clasificador de Claude Code bloquea POSTs que mutan datos reales con target elegido por el agente (regla "IDs fuera de rango"). Para acciones destructivas: usar org sandbox (`is_test=true`) + recurso que el usuario confirme, o que el usuario lance el script con `!`.

Caso: smoke de "marcar cobrada" (copiloto Fase 2). Ref `src/lib/internal/auth.ts` (`buildSignatureHeader`).
