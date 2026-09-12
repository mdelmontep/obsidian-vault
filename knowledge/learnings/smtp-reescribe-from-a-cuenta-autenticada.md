---
title: el smtp del proveedor reescribe el From a la cuenta autenticada
date: 2026-06-27
source: facturaia, simarro
tags: [email, smtp, resend, deliverability, spf]
---
El `from` que pones en el código NO llega si envías por SMTP autenticado con otra
cuenta/dominio: el servidor **reescribe el From a la cuenta autenticada** (anti-spoofing).
El código está bien; lo cambia el relay.

**Antes de "arreglarlo" dando de alta el alias, mira el DNS del dominio** (`dig MX`,
`dig TXT` del SPF): si el correo del dominio vive en otro proveedor y su SPF no incluye
al relay y acaba en `-all`, **la reescritura es lo único que evita un SPF fail** — quitarla
manda todo a spam. Caso Simarro (13-sep-2026): dominio en Microsoft 365, SPF con
`include:spf.protection.outlook.com -all`, enviando por Gmail. Salida elegida: poner en los
nodos el From real (la cuenta que autentica) en vez de perseguir el alias.

Para enviar de verdad desde tu dominio: API con dominio verificado (Resend/SES) o el SMTP
del proveedor que ya está en su SPF. Gotcha QA: sin `RESEND_API_KEY` en `.env.local` el
wrapper cae al SMTP fallback y el remitente "falla" solo en local.
