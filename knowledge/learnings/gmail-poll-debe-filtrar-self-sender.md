---
title: gmail-poll debe filtrar self-sender para no ingerir tickets falsos
date: 2026-05-09
source: claude-code-session
tags: [email, ticketing, anti-pattern]
---

Si el sistema (bot n8n, scheduler, cron) envía emails de notificación a
una bandeja monitorizada por el propio panel y la cuenta SMTP saliente
es la misma que la cuenta OAuth del gmail-poll, el ingestor crea
**tickets falsos** con `contact = la propia cuenta`.

Patrón obligatorio: en el processor del poller, **antes** del lookup de
contact / idempotencia:

```ts
const selfSender = (cfg["oauth_email"] ?? "").toLowerCase()
if (selfSender && fromEmail.toLowerCase() === selfSender) {
  await markAsRead(...); skipped++; continue
}
```

Replicar en TODAS las rutas de ingestión Gmail (poll worker + push
Pub/Sub via gmail-message.service). La idempotencia por messageId NO
salva: cada email tiene messageId distinto.

Caso real Tecnocloud: `dansanchez@tecnocloud` falsificaba contacto en
todos los tickets de voz porque n8n enviaba notificación a
`incidencias@` desde la misma cuenta conectada al panel.
