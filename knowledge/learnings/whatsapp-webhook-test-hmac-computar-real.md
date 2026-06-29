---
title: webhook test hmac - computar firma real, no mockear la verificación
date: 2026-06-30
source: claude-code-session
tags: [vitest, testing, whatsapp, hmac, webhook, seguridad]
---

Si mockeas la función de verificación HMAC del webhook (ej. `verifyMetaSignature`), el handler
puede devolver 200 sin procesar ningún mensaje — y los tests pasan igualmente. Falso positivo
estructural: estás probando que el mock funciona, no el handler.

Fix: computar el HMAC real en el helper del test:

```ts
const sig = `sha256=${createHmac('sha256', APP_SECRET).update(body, 'utf8').digest('hex')}`
new Request(url, { headers: { 'x-hub-signature-256': sig }, body })
```

Así el handler procesa el mensaje real y puedes verificar que los efectos ocurrieron
(`mockSendText` llamado, `mockFetch` llamado con la URL correcta, etc.).

Aplica a cualquier webhook con firma HMAC: Meta, Stripe, GitHub, Resend.

Caso real: `src/app/api/whatsapp/webhook/__tests__/route.test.ts`.
