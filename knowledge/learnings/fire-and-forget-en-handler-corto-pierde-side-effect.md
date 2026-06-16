---
title: void async() en un handler que retorna enseguida abandona el side-effect
date: 2026-06-17
source: claude-code-session
tags: [nextjs, async, email, crons]
---

`void asyncFn()` (fire-and-forget) dentro de un route/cron handler que retorna
justo después: la promesa queda colgada y el runtime puede destruir el contexto
de la request antes de que termine → el side-effect no ocurre.

Caso TuFacturaIA: `emitSystemAlert` hacía `void sendEmail(...)`. Llamado desde
un cron que retornaba acto seguido, el `sendEmail` **ni siquiera insertaba** su
fila en el outbox (`email_log`) — 0 emails en toda la historia. (Dentro de un
request largo que sigue trabajando a veces sí completa, por eso pasaba
desapercibido.)

Fix: `await` el side-effect dentro de la función. El caller que NO quiera
bloquear hace el `void` a SU nivel (wrapper `...FireAndForget`). Aplica a
cualquier async no esperado (email, audit, webhook, log) en handler corto.
