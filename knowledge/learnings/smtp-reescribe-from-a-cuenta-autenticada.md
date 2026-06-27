---
title: el smtp del proveedor reescribe el From a la cuenta autenticada
date: 2026-06-27
source: claude-code-session
tags: [email, smtp, resend, deliverability]
---
El `from` que pones en el código (`hola@tufacturaia.com`) NO llega si envías por
SMTP autenticado con otra cuenta/dominio (`info@agentesia.madrid`): el servidor
**reescribe el From a la cuenta autenticada** (anti-spoofing). El código está
bien; lo cambia el relay.

Para enviar desde tu propio dominio: **API con dominio verificado** (Resend/SES
con `tufacturaia.com` verificado), no el SMTP de otro dominio.

Gotcha de QA local: si `.env.local` no tiene `RESEND_API_KEY`, el wrapper cae al
SMTP fallback → remitente "equivocado" en local aunque en prod (Resend) salga
bien. Añadir la key en local para reproducir prod antes de dar por bueno un bug
de remitente.
