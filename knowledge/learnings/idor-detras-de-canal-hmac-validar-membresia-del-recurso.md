---
title: un canal interno firmado (hmac) no exime de autorizar al dueño del recurso
date: 2026-06-26
source: claude-code-session
tags: [seguridad, idor, multitenant, hmac, n8n]
---

Un endpoint interno protegido por HMAC (service-key) autentica al **llamante** (p.ej.
n8n), no autoriza el **recurso**. Si el `org_id` (o cualquier id de tenant) viene en el
body firmado y se usa directo para escribir/leer, una n8n comprometida, un secret
filtrado o un payload malformado puede operar sobre una org ajena → IDOR cross-tenant,
aunque el HMAC sea válido.

Regla: aunque el canal sea de confianza, **valida igualmente que el actor es dueño del
recurso** (defensa en profundidad). Resolver el user (p.ej. por teléfono) y exigir
membresía activa en ese `org_id` antes de actuar; 403/404 si no.

Pista de inconsistencia interna: si un endpoint hermano del mismo canal SÍ valida
membresía (con un comentario tipo "defensa contra n8n comprometida") y otro no, el que
no la valida es el bug. Caso FacturaIA: `whatsapp/pending-action/execute` y
`whatsapp/copiloto` no validaban (los read tools no llevan `required_role`); `select-org`
sí → se alinearon. El `payload.org_id === body.org_id` no es defensa (el atacante
controla ambos).
