---
title: timing-safe comparison obligatoria para service-key auth
date: 2026-04-24
source: claude-code-session
tags: [security, nodejs, auth]
---

Comparar `x-service-key` con `!==` es vulnerable a timing attacks — un atacante puede deducir la key caracter a caracter midiendo tiempos de respuesta. Usar siempre `crypto.timingSafeEqual`.

## Patron

```typescript
import { timingSafeEqual } from 'node:crypto'

const serviceKey = headers.get('x-service-key') || ''
const expected = process.env.SUPABASE_SERVICE_ROLE_KEY || ''

const isValid = serviceKey.length > 0 &&
  serviceKey.length === expected.length &&
  timingSafeEqual(Buffer.from(serviceKey), Buffer.from(expected))
```

## Gotchas

- `timingSafeEqual` lanza error si los buffers tienen longitud diferente — verificar `.length ===` antes
- Verificar que la key no esta vacia (`.length > 0`) para evitar que dos strings vacias pasen
- Aplica a cualquier endpoint interno protegido con header secreto (poll, webhooks, admin internal)
