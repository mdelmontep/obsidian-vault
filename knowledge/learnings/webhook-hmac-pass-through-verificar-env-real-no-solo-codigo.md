---
title: validación HMAC de webhook con pass-through de seguridad exige confirmar el env real, no solo leer el código
date: 2026-07-23
source: claude-code-session
tags: [n8n, seguridad, webhooks, dokploy]
---

Patrón defensivo común en nodos Code de n8n que validan firma de webhook (Meta, Stripe, etc.):
`if (!secret) return $input.all(); // pass-through — secret no seteado`. Esto es correcto como
fallback de arranque, pero significa que **ver el código de validación no prueba que esté activa**.

Antes de dar por buena una validación HMAC:
1. Leer el nodo (vía API n8n, `GET /workflows/:id`) para confirmar la lógica real.
2. Cruzar contra el env REAL del contenedor desplegado (Dokploy `compose.one` → campo `env`, o
   `docker exec printenv` por SSH) — no contra el `.env` local del repo, que puede estar desincronizado.

Caso real: Centro Elphis, `wa-inbound-bridge` / nodo `Validate HMAC Meta` — confirmado
`META_APP_SECRET` presente en el compose real de Dokploy, así que el pass-through nunca se activa
y la firma sí se verifica. Sin este cruce, una nota "HMAC pendiente" heredada de un audit viejo
casi queda repetida sin verificar.
