---
title: imap attachment selectivo via bodyStructure evita oom
date: 2026-05-26
source: claude-code-session
tags: [imap, email, ocr, memoria, dokploy]
---

`imapflow.download(uid)` materializa el RFC822 completo del mensaje. Un mail con 5 PDFs de 9MB son ~50MB en RAM justo cuando `simpleParser` los parsea — vector OOM real en containers Dokploy pequeños (256-512MB) si coinciden varios polls.

**Patrón correcto**: `fetchOne(uid, {bodyStructure: true})` para inspeccionar partes (1 RTT) → filtrar por MIME allowlist + size ≤ max → `download(uid, partId, {uid: true})` solo de las que pasan. Se descarga exactamente lo que se va a usar.

**Cost**: 1 RTT extra al servidor IMAP. A cambio: memoria proporcional al **adjunto** más grande, no al **mensaje** entero. Mismo patrón que Gmail API (lista metadata → `messages.attachments.get` por attachmentId).

**Detalle del bodyStructure parsing**: cada parte trae `type/subtype` (MIME), `disposition` (`attachment|inline`), `parameters.name` o `dispositionParameters.filename`, `size`, `part` (partId tipo `1.2.3`). Excluir partes sin `filename` válido y sin disposition. Validar size ANTES de download.

Caso TuFacturaIA `src/lib/integrations/providers/icloud-mail/imap-client.ts` (commit `817aa8e`).
