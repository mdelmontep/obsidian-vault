---
title: checklist seguridad api routes nextjs
date: 2026-04-25
source: claude-code-session
tags: [seguridad, nextjs, api, checklist]
---

Checklist consolidado de seguridad para API routes en Next.js (aplicado en FacturaIA 2026-04-25).

## Por cada endpoint nuevo

1. **Auth check** — `getUser()` para endpoints de usuario, `requireAdmin()` para admin, `timingSafeEqual` con `x-service-key` para rutas de servicio (n8n, webhooks)
2. **Rate limiting** — `rateLimit(key, max, windowMs)` con key por user ID. Valores orientativos: upload 20/min, AI/LLM 30/min, auth 5/min
3. **Input validation** — Zod schema con `.safeParse()`. Para IDs de template o similar, usar whitelist (`Set`) no validación abierta
4. **Dynamic imports** — nunca `import(\`...-${userInput}\`)` sin whitelist. Crear `ALLOWED_X = new Set([...])` y validar antes
5. **Error responses** — nunca devolver `error.message`, `errBody`, `raw` de APIs externas. Solo mensajes genéricos al cliente. Loggear detalle server-side con `console.error`
6. **Magic number validation** — no confiar en `file.type` del cliente para uploads. Verificar primeros bytes del buffer contra firmas conocidas (PDF: `%PDF`, JPEG: `FF D8 FF`, PNG: `89 50 4E 47`)
7. **Timing-safe comparison** — siempre `timingSafeEqual(Buffer.from(a), Buffer.from(b))` para secrets. Nunca `===` o `!==`
8. **Middleware bypass** — al añadir ruta a `isServiceRoute`, verificar que la ruta tiene su propia auth. Sin esto, el endpoint queda completamente abierto
9. **Audit log** — para endpoints admin que ejecutan queries dinámicas (impersonate), loggear tabla, filtros y usuario
10. **Method whitelist** — si un endpoint acepta nombres de métodos dinámicos (ej: filtros Supabase), crear `ALLOWED_METHODS` Set
11. **Path traversal con prefix UUID** — al validar paths tipo `{orgId}/file.ext` no basta con `startsWith(orgId)`. Atacante puede pasar `{orgId}123/file` y bypass. Validar separador con `path.charAt(36) === '/'` después de `slice(0, 36)`. Aplica a cualquier endpoint que sirva archivos por path con prefix tenant.

## Rate limiter in-memory

```typescript
// src/lib/rate-limit.ts
const hits = new Map<string, { count: number; resetAt: number }>()
// Cleanup cada 60s, key por user+action, window configurable
rateLimit(`upload:${user.id}`, 20, 60_000)
```

Suficiente para single-instance. Para multi-instance (horizontal scaling), migrar a Redis.

## Bugs encontrados en FacturaIA (2026-04-25)

- `/api/render-pdf` — sin auth, sin whitelist de template ID → RESUELTO 2026-04-27: acepta `x-service-key` (server-to-server) O sesión Supabase (browser). Patrón: if key → timingSafeEqual, else → getUser()
- `/api/generate-pdfs` — `!==` en vez de `timingSafeEqual`
- `/api/admin/impersonate/query` — aceptaba cualquier método Supabase sin whitelist, sin audit log
- `/api/upload` — confiaba solo en MIME type del cliente
- `/api/voice/extract` y `/api/voice/generate` — exponían errores internos de OpenAI y Supabase en respuestas
